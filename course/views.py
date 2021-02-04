from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from course.models import CourseSchedule, Course, CourseLink
from course.serializers import CourseSerializer, ScheduleSerializer, LinkSerializer, CourseShortSerializer
from users.models import User, CourseAssignStudent


class CourseViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin):
    serializer_class = CourseSerializer
    queryset = Course.objects.select_related('author').prefetch_related('staff', 'students').all()

    # # TODO: make it work
    # def get_queryset(self):
    #     request = self.get_serializer_context()['request']
    #     user: User = User.objects.get(pk=request.user.id)
    #     queryset = user.staff_for.all().union(user.student_for.all())
    #     return queryset


class ScheduleViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin):
    serializer_class = ScheduleSerializer
    queryset = CourseSchedule.objects.all()


class LinkViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin):
    serializer_class = LinkSerializer
    queryset = CourseLink.objects.all()


def __check(link, user_id):
    answer = dict(
        link_exists=True, student_registered=False, teacher_registered=False,
        is_possible=True, course=None, usages_available=True,
    )
    try:
        instance = CourseLink.objects.select_related('course').get(link=link) \
            .prefetch_related('course__staff', 'course__students')
        answer['course'] = CourseShortSerializer(instance.course).data
        answer['usages_available'] = bool(instance.usages)
    except CourseLink.DoesNotExist:
        answer.update(dict(link_exists=False, is_possible=False))
        return Response(answer)
    try:
        instance.student.get(id=user_id)
        answer.update(dict(student_registered=True, is_possible=False))
    except User.DoesNotExist:
        pass
    try:
        instance.staff.get(id=user_id)
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
    link = CourseLink.objects.get(link=link).select_related('course')
    assignment = CourseAssignStudent(course=link.course, user=request.user)
    assignment.save()
    link.usages -= 1
    link.save()
    return Response(dict(status=200, ))
