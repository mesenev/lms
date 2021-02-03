from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from course.models import CourseSchedule, Course, CourseLink
from course.serializers import CourseSerializer, ScheduleSerializer, LinkSerializer, CourseShortSerializer


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


@login_required
@api_view(['GET'])
def check_link(request, link):
    try:
        instance = CourseLink.objects.select_related('course').get(link=link)
    except CourseLink.DoesNotExist:
        return Response(dict(is_possible=False, already_registered=False, course=None))
    course = CourseShortSerializer(instance.course).data
    return Response(dict(is_possible=True, already_registered=False, course=course))


@login_required
@api_view(['GET'])
def course_registration(request, link):
    return Response(dict(is_possible=True, already_registered=False, course=None))
