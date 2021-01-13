from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
)
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
)
from rest_framework.viewsets import GenericViewSet

from course.models import CourseSchedule, Course
from course.serializers import CourseSerializer, ScheduleSerializer
from users.models import User


class CourseViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin):

    serializer_class = CourseSerializer
    queryset = Course.objects.prefetch_related('staff', 'students').all()

    # # TODO: make it work
    # def get_queryset(self):
    #     request = self.get_serializer_context()['request']
    #     user: User = User.objects.get(pk=request.user.id)
    #     queryset = user.staff_for.all().union(user.student_for.all())
    #     return queryset


class ScheduleViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin):
    serializer_class = ScheduleSerializer
    queryset = CourseSchedule.objects.all()
