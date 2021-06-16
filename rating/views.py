from rest_framework import viewsets

from rating.models import LessonProgress, CourseProgress, Attendance
from rating.serializers import LessonProgressSerializer, CourseProgressSerializer, AttendanceSerializer


class CourseProgressViewSet(viewsets.ModelViewSet):
    serializer_class = CourseProgressSerializer
    queryset = CourseProgress.objects.all()
    filterset_fields = ['user_id', 'course_id']


class LessonProgressViewSet(viewsets.ModelViewSet):
    serializer_class = LessonProgressSerializer
    queryset = LessonProgress.objects.all()
    filterset_fields = ['lesson_id' ]


class AttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceSerializer
    queryset = Attendance.objects.all()
    filterset_fields = ['lesson_id','course_id']
