from django.db.models import Q
from rest_framework import viewsets

from lesson.models import Lesson, LessonContent, LessonProgress
from lesson.serializers import LessonSerializer, MaterialSerializer, LessonProgressSerializer


class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    filterset_fields = ['course_id', ]

    def get_queryset(self):
        """
        This view should return a list of all the lessons
        for the currently authenticated user.
        """
        user = self.request.user

        return Lesson.objects.filter(Q(is_hidden=False) | Q(course__in=user.staff_for.all()))


class MaterialViewSet(viewsets.ModelViewSet):
    serializer_class = MaterialSerializer
    queryset = LessonContent.objects.all()


class LessonProgressViewSet(viewsets.ModelViewSet):
    serializer_class = LessonProgressSerializer
    queryset = LessonProgress.objects.all()
