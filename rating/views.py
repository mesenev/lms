from rest_framework import viewsets

from rating.models import LessonProgress, CourseProgress
from rating.serializers import LessonProgressSerializer, CourseProgressSerializer


class CourseProgressViewSet(viewsets.ModelViewSet):
    serializer_class = CourseProgressSerializer
    queryset = CourseProgress.objects.all()
    filterset_fields = ['user_id', 'course_id']


class LessonProgressViewSet(viewsets.ModelViewSet):
    serializer_class = LessonProgressSerializer
    queryset = LessonProgress.objects.all()
    filterset_fields = ['lesson_id', ]
