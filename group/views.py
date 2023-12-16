from django.shortcuts import render
from rest_framework import viewsets
from group.serializers import CourseGroupSerializer, CourseGroupLinkSerializer
from group.models import CourseGroup, CourseGroupLink
from rest_framework.decorators import action
from users.models import CourseGroupAssignTeacher, CourseGroupAssignStudent, User
from users.serializers import DefaultUserSerializer
from rest_framework.response import Response
from rest_framework import status
from users.permissions import CourseStaffOrReadOnlyForStudents, CourseStaffOrAuthorReadOnly, CourseStaffOrAuthor
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, NotFound
from imcslms.default_settings import TEACHER


class CourseGroupViewSet(viewsets.ModelViewSet):
    serializer_class = CourseGroupSerializer
    queryset = CourseGroup.objects.all()
    permission_classes = [CourseStaffOrReadOnlyForStudents]
    filterset_fields = ['course_id']

    def create(self, request, *args, **kwargs):
        if not request.user.groups.filter(name=TEACHER).exists():
            raise PermissionDenied
        return super().create(request, *args, **kwargs)

    @action(
        detail=True, methods=['post'], url_path=r'assign-teacher', url_name='assign-teacher',
    )
    def assign_teacher(self, request, pk=None):
        group = self.get_object()
        if group not in request.user.staff_for.all() and group.course not in request.user.author_for.all():
            raise PermissionDenied()
        user = User.objects.get(id=request.data['id'])
        if not user:
            return Response(dict(code=1, message='User not exist'), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        exist = CourseGroupAssignTeacher.objects.filter(group=group, user=user).exists()
        if exist:
            return Response(dict(code=1, message='User already assigned'), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if not exist:
            assignment = CourseGroupAssignTeacher(group=group, user=user)
            assignment.save()
            return Response(dict(code=0, message='User successfully assigned'))

    @action(
        detail=True, methods=['post'], url_path=r'assign-student', url_name='assign-student',
    )
    def assign_student(self, request, pk=None):
        group = self.get_object()
        if group not in request.user.staff_for.all() and group.course not in request.user.author_for:
            raise PermissionDenied()
        user = User.objects.get(id=request.data['id'])
        if not user:
            return Response(dict(code=1, message='User not exist'), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        exist = CourseGroupAssignStudent.objects.filter(group=group, user=user).exists()
        if exist:
            return Response(dict(code=1, message='User already assigned'), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if not exist:
            assigment = CourseGroupAssignStudent(group=group, user=user)
            assigment.save()
            return Response(dict(code=0, message='User succesfully assigned'))

    @action(
        detail=True, methods=['delete'], url_path=r'delete-teacher', url_name='delete-teacher'
    )
    def delete_teacher(self, request, pk=None):
        group = self.get_object()
        if group not in request.user.staff_for.all() and group.course not in request.user.author_for:
            raise PermissionDenied()
        teacher = User.objects.get(id=request.data['id'])
        if not teacher:
            return Response(dict(code=1, message='Teacher not exist'), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        exist = CourseGroupAssignTeacher.objects.filter(group=group, user=teacher)
        if not exist:
            return Response(dict(code=1, message='Teacher not assigned to group'), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if exist:
            exist.delete()
            return Response(dict(code=0, message='Teacher succesfully deleted from group'))

    @action(
        detail=True, methods=['delete'], url_path=r'delete-student', url_name='delete-student'
    )
    def delete_student(self, request, pk=None):
        group = self.get_object()
        if group not in request.user.staff_for.all() and group.course not in request.user.author_for:
            raise PermissionDenied()
        student = User.objects.get(id=request.data['id'])
        if not student:
            return Response(dict(code=1, message='Student not exist'), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        exist = CourseGroupAssignStudent.objects.filter(group=group, user=student)
        if not exist:
            return Response(dict(code=1, message='Student not assigned to group'), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if exist:
            exist.delete()
            return Response(dict(code=0, message='Student succesfully deleted'))


class CourseGroupLinkViewSet(viewsets.ModelViewSet):
    permission_classes = [CourseStaffOrAuthorReadOnly]
    queryset = CourseGroupLink.objects.all()
    serializer_class = CourseGroupLinkSerializer

    def list(self, request: Request, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if 'course' in request.query_params:
            queryset = queryset.filter(group=request.query_params['group'])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


def link_check(link, user_id):
    answer = dict(
        link_exists=True, student_registered=False, teacher_registered=False,
        is_possible=True, group=None, usages_available=True,
    )
    try:
        instance = CourseGroupLink.objects.select_related('group') \
            .prefetch_related('group__staff', 'group__students').get(link=link)
        answer['group'] = CourseGroupSerializer(instance.group).data
        answer['usages_available'] = bool(instance.usages)
        if not answer['usages_available']:
            answer.update(dict(link_exists=False, is_possible=False))

    except CourseGroupLink.DoesNotExist:
        answer.update(dict(link_exists=False, is_possible=False))
        return answer
    try:
        instance.group.students.get(id=user_id)
        answer.update(dict(student_registered=True, is_possible=False))
    except User.DoesNotExist:
        pass
    try:
        instance.group.staff.get(id=user_id)
        answer.update(dict(teacher_registered=True, is_possible=False))
    except User.DoesNotExist:
        pass
    return answer


class CheckLinkApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, link):
        return Response(link_check(link, request.user.id))


class GroupRegistrationApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, link):
        if not link_check(link, request.user.id)['is_possible']:
            raise PermissionDenied()
        link = CourseGroupLink.objects.select_related('group').get(link=link)
        assignment = CourseGroupAssignStudent(group=link.group, user=request.user)
        assignment.save()
        if link.usages > 0:
            link.usages -= 1
            link.save()
            return Response(dict(user=assignment.user_id, courseId=link.group.course.id))
        else:
            raise NotFound()


class LinkDeletionAPi(APIView):
    permission_classes = [CourseStaffOrAuthor]

    def delete(self, request, link):
        group_link = CourseGroupLink.objects.get(link=link)
        group_link.delete()
        return Response(link)