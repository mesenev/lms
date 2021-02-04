from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from course.models import CourseSchedule, Course, CourseLink
from course.serializers import CourseSerializer, ScheduleSerializer, LinkSerializer, CourseShortSerializer
from users.models import User


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
    user = request.user
    student = None
    teacher = None
    try:
        instance = CourseLink.objects.prefetch_related('course').get(link=link)
        student = instance.course.students.get(id=user.id)
        teacher = instance.course.staff.get(id=user.id)
    except User.DoesNotExist:
        print('2')
    except CourseLink.DoesNotExist:
        return Response(dict(is_possible=False, already_registered=False, course=None))
    course = CourseShortSerializer(instance.course).data
    if student or teacher:
        return Response(dict(is_possible=False, already_registered=True, course=course))
    else:
        return Response(dict(is_possible=True, already_registered=False, course=course))


@login_required
@api_view(['GET'])
def course_registration(request, link):
    link.usages -= 1
    return render(request, 'login.html')
