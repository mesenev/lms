from django.shortcuts import render
from rest_framework import viewsets
from group.serializers import GroupSerializer, LinkSerializer
from group.models import Group, GroupLink
from rest_framework.decorators import action
from users.models import GroupAssignTeacher, GroupAssignStudent, User
from users.serializers import DefaultUserSerializer
from rest_framework.response import Response
from users.permissions import CourseStaffOrReadOnlyForStudents, CourseStaffOrAuthorReadOnly, CourseStaffOrAuthor
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, NotFound
from imcslms.default_settings import TEACHER


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
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
        if group not in request.user.staff_for.all():
            raise PermissionDenied()
        user = User.objects.get(id=request.data['id'])
        if not user:
            return Response(dict(code=1, message='User not exist'))
        exist = GroupAssignTeacher.objects.filter(group=group, user=user).exists()
        if exist:
            return Response(dict(code=1, message='User already assigned'))
        if not exist:
            assignment = GroupAssignTeacher(group=group, user=user)
            assignment.save()
            return Response(dict(code=0, message='User successfully assigned'))

    @action(
        detail=True, methods=['post'], url_path=r'assign-student', url_name='assign-student',
    )
    def assign_student(self, request, pk=None):
        group = self.get_object()
        if group not in request.user.staff_for.all():
            raise PermissionDenied()
        user = User.objects.get(id=request.data['id'])
        if not user:
            return Response(dict(code=1, message='User not exist'))
        exist = GroupAssignStudent.objects.filter(group=group, user=user).exists()
        if exist:
            return Response(dict(code=1, message='User already assigned'))
        if not exist:
            assigment = GroupAssignStudent(group=group, user=user)
            assigment.save()
            return Response(dict(code=0, message='User succesfully assigned'))


class LinkViewSet(viewsets.ModelViewSet):
    permission_classes = [CourseStaffOrAuthorReadOnly]
    queryset = GroupLink.objects.all()
    serializer_class = LinkSerializer

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
        instance = GroupLink.objects.select_related('group') \
            .prefetch_related('group__staff', 'group__students').get(link=link)
        answer['group'] = GroupSerializer(instance.group).data
        answer['usages_available'] = bool(instance.usages)
        if not answer['usages_available']:
            answer.update(dict(link_exists=False, is_possible=False))

    except GroupLink.DoesNotExist:
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
        link = GroupLink.objects.select_related('group').get(link=link)
        assignment = GroupAssignStudent(group=link.group, user=request.user)
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
        group_link = GroupLink.objects.get(link=link)
        group_link.delete()
        return Response(link)