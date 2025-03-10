from django.shortcuts import get_object_or_404
from rest_framework import viewsets, exceptions, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from group.serializers import GroupAssignTeacherSerializer
from cathie import cats_api
from course.models import CourseSchedule, Course
from course.serializers import CourseSerializer, ScheduleSerializer, CourseShortSerializer
from imcslms.default_settings import TEACHER
from users.models import CourseGroupAssignTeacher
from users.permissions import CourseStaffOrReadOnlyForStudents, CourseStaffOrAuthorReadOnly, CourseStaffOrAuthor


class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = [CourseStaffOrReadOnlyForStudents]
    serializer_class = CourseSerializer
    queryset = Course.objects.select_related(
        'author'
    ).prefetch_related(
        'lessons', 'lessons__problems'
    ).all()

    def list(self, request: Request, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = CourseShortSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if not request.user.groups.filter(name=TEACHER).exists():
            raise exceptions.PermissionDenied
        return super().create(request, *args, **kwargs)



    @action(detail=False)
    def user_courses(self, request):
        queryset = request.user.author_for.all()

        staff_for_groups = request.user.staff_for.all()
        for group in staff_for_groups:
            queryset = queryset.union(Course.objects.filter(source_for=group))

        student_for_groups = request.user.student_for.all()
        for group in student_for_groups:
            queryset = queryset.union(Course.objects.filter(source_for=group))

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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        course = Course.objects.get(id=(serializer.data['id']))
        CourseGroupAssignTeacher.objects.create(course=course, user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, url_path=r'by-course/(?P<course_id>\d+)')  # hate regexes
    def by_course(self, request, course_id):
        queryset = CourseSchedule.objects.all()
        instance = get_object_or_404(queryset, course__id=course_id)
        serializer = ScheduleSerializer(instance)
        return Response(serializer.data)
