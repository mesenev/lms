from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
)
from rest_framework.viewsets import GenericViewSet

from course.models import Course, CourseSchedule
from course.serializers import CourseSerializer, ScheduleSerializer


class CourseViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class ScheduleViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin):
    serializer_class = ScheduleSerializer
    queryset = CourseSchedule.objects.all()
