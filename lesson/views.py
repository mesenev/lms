from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
)
from rest_framework.viewsets import GenericViewSet

from lesson.models import Lesson, LessonContent, LessonProgress
from lesson.serializers import LessonSerializer, MaterialSerializer, LessonProgressSerializer


class LessonViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class MaterialViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin):
    serializer_class = MaterialSerializer
    queryset = LessonContent.objects.all()


class LessonProgressViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin):
    serializer_class = LessonProgressSerializer
    queryset = LessonProgress.objects.all()