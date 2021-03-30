from itertools import chain

from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework.decorators import api_view, action
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from course.models import CourseSchedule, Course, CourseLink, CourseProgress
from course.serializers import CourseSerializer, ScheduleSerializer, LinkSerializer, CourseShortSerializer, \
    CourseProgressSerializer
from users.models import User, CourseAssignStudent


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.select_related('author').prefetch_related('staff', 'students').all()

    # # TODO: make it work
    # def get_queryset(self):
    #     request = self.get_serializer_context()['request']
    #     user: User = User.objects.get(pk=request.user.id)
    #     queryset = user.staff_for.all().union(user.student_for.all())
    #     return queryset

    @action(detail=False)
    def user_courses(self, request):
        queryset = chain(
            request.user.staff_for.all(),
            request.user.author_for.all(),
            self.request.user.student_for.all()
        )
        serializer = CourseShortSerializer(queryset, many=True)
        return Response(serializer.data)


class ScheduleViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin):
    serializer_class = ScheduleSerializer
    queryset = CourseSchedule.objects.all()


class LinkViewSet(viewsets.ModelViewSet):
    queryset = CourseLink.objects.all()
    serializer_class = LinkSerializer
    permission_classes = []

    def list(self, request: Request, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if 'course' in request.query_params:
            queryset = queryset.filter(course=request.query_params['course'])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CourseProgressViewSet(viewsets.ModelViewSet):
    serializer_class = CourseProgressSerializer
    queryset = CourseProgress.objects.all()
    filterset_fields = ['user_id', 'course_id']


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

    # TODO: if needed - prettify that expression

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


@login_required
@api_view(['GET'])
def check_link(request: Request, link):
    return Response(__check(link, request.user.id))


@login_required
@api_view(['GET'])
def course_registration(request, link):
    if not __check(link, request.user.id)['is_possible']:
        raise PermissionDenied()
    link = CourseLink.objects.select_related('course').get(link=link)
    assignment = CourseAssignStudent(course=link.course, user=request.user)
    assignment.save()
    if link.usages > 0:
        link.usages -= 1
        link.save()
        return Response(dict(user=assignment.user_id, courseId=assignment.course.id))
    else:
        raise NotFound()


@login_required
@api_view(['DELETE'])
def delete_link(request, link):
    courselinks = CourseLink.objects.all()
    courselinks.get(link=link).delete()
    return Response(link)
