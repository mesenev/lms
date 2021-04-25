from django.db.models import Q
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from lesson.models import Lesson, LessonContent
from lesson.serializers import LessonSerializer, MaterialSerializer, LessonProgressSerializer, LessonShortSerializer


class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    filterset_fields = ['course_id', ]

    def get_queryset(self):
        user = self.request.user
        return Lesson.objects.prefetch_related('problems', 'progress', 'materials').filter(
            (Q(is_hidden=False) & Q(course__in=user.assigns.all()))
            | Q(course__in=user.staff_for.all())
            | Q(course__in=user.author_for.all())
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = LessonShortSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, **kwargs):
        queryset = self.get_queryset()
        user = get_object_or_404(queryset, pk=pk)
        serializer = LessonSerializer(user)
        return Response(serializer.data)


class MaterialViewSet(viewsets.ModelViewSet):
    serializer_class = MaterialSerializer
    queryset = LessonContent.objects.all()
    filterset_fields = ['lesson_id', ]


