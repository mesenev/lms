from rest_framework import viewsets

from lesson.models import Lesson, LessonContent, LessonProgress
from lesson.serializers import LessonSerializer, MaterialSerializer, LessonProgressSerializer


class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    filterset_fields = ['course_id', ]


class MaterialViewSet(viewsets.ModelViewSet):
    serializer_class = MaterialSerializer
    queryset = LessonContent.objects.all()


class LessonProgressViewSet(viewsets.ModelViewSet):
    serializer_class = LessonProgressSerializer
    queryset = LessonProgress.objects.all()
