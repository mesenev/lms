from django.shortcuts import get_object_or_404
from rest_framework import viewsets, exceptions
from rest_framework.decorators import api_view, action
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from cathie import cats_api
from course.models import CourseSchedule, Course, CourseLink
from course.serializers import CourseSerializer, ScheduleSerializer, LinkSerializer, CourseShortSerializer
from imcslms.default_settings import TEACHER
from users.models import User, CourseAssignStudent
from users.permissions import CourseStaffOrReadOnlyForStudents, CourseStaffOrAuthorReadOnly


class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = [CourseStaffOrReadOnlyForStudents]
    serializer_class = CourseSerializer
    queryset = Course.objects.select_related(
        'author'
    ).prefetch_related(
        'staff', 'students', 'lessons', 'lessons__problems'
    ).all()

    def list(self, request: Request, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = CourseShortSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if request.user.groups.filter(name=TEACHER).exists():
            return super().create(request, *args, **kwargs)
        raise exceptions.PermissionDenied

    @action(detail=False)
    def user_courses(self, request):
        queryset = request.user.author_for.all()
        queryset = queryset.union(request.user.staff_for.all())
        queryset = queryset.union(request.user.student_for.all())
        serializer = CourseShortSerializer(queryset, many=True)
        return Response(serializer.data)


class ScheduleViewSet(
    GenericViewSet, CreateModelMixin, RetrieveModelMixin,
    UpdateModelMixin, DestroyModelMixin, ListModelMixin
):
    permission_classes = [CourseStaffOrAuthorReadOnly]
    serializer_class = ScheduleSerializer
    queryset = CourseSchedule.objects.all()

    def create(self, request, *args, **kwargs):
        if not getattr(request.data, 'start_date', ''):
            del request.data['start_date']
        return super().create(request, *args, **kwargs)

    @action(detail=False, url_path=r'by-course/(?P<course_id>\d+)')  # hate regexes
    def by_course(self, request, course_id):
        queryset = CourseSchedule.objects.all()
        instance = get_object_or_404(queryset, course__id=course_id)
        serializer = ScheduleSerializer(instance)
        return Response(serializer.data)


class LinkViewSet(viewsets.ModelViewSet):
    permission_classes = [CourseStaffOrAuthorReadOnly]
    queryset = CourseLink.objects.all()
    serializer_class = LinkSerializer

    def list(self, request: Request, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if 'course' in request.query_params:
            queryset = queryset.filter(course=request.query_params['course'])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


def __check(link, user_id):
    answer = dict(
        link_exists=True, student_registered=False, teacher_registered=False,
        is_possible=True, course=None, usages_available=True,
    )
    try:
        instance = CourseLink.objects.select_related('course') \
            .prefetch_related('course__staff', 'course__students').get(link=link)
        answer['course'] = CourseShortSerializer(instance.course).data
        answer['usages_available'] = bool(instance.usages)
        if not answer['usages_available']:
            answer.update(dict(link_exists=False, is_possible=False))

    except CourseLink.DoesNotExist:
        answer.update(dict(link_exists=False, is_possible=False))
        return Response(answer)
    try:
        instance.course.students.get(id=user_id)
        answer.update(dict(student_registered=True, is_possible=False))
    except User.DoesNotExist:
        pass
    try:
        instance.course.staff.get(id=user_id)
        answer.update(dict(teacher_registered=True, is_possible=False))
    except User.DoesNotExist:
        pass
    return answer


@api_view(['GET'])
def check_link(request: Request, link):
    return Response(__check(link, request.user.id))


@api_view(['GET'])
def course_registration(request, link):
    if not __check(link, request.user.id)['is_possible']:
        raise PermissionDenied()
    link = CourseLink.objects.select_related('course').get(link=link)
    assignment = CourseAssignStudent(course=link.course, user=request.user)
    cats_api.add_users_to_contest([request.user], link.course_id)
    assignment.save()
    if link.usages > 0:
        link.usages -= 1
        link.save()
        return Response(dict(user=assignment.user_id, courseId=assignment.course.id))
    else:
        raise NotFound()


@api_view(['DELETE'])
def delete_link(request, link):
    courselinks = CourseLink.objects.all()
    courselinks.get(link=link).delete()
    return Response(link)
