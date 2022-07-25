from django.db.models import Q
from rest_framework import viewsets, exceptions
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from imcslms.default_settings import TEACHER
from lesson.models import Lesson, LessonContent
from lesson.serializers import LessonSerializer, MaterialSerializer, LessonShortSerializer
from users.permissions import CourseStaffOrReadOnlyForStudents


class LessonViewSet(viewsets.ModelViewSet):
    permission_classes = [CourseStaffOrReadOnlyForStudents]
    serializer_class = LessonSerializer
    filterset_fields = ['course_id', ]

    def get_queryset(self):
        user = self.request.user
        return Lesson.objects.prefetch_related('problems', 'progress', 'materials').filter(
            (Q(is_hidden=False) & Q(course__in=user.student_for.all()))
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

    def create(self, request, *args, **kwargs):
        if request.user.groups.filter(name=TEACHER).exists():
            return super().create(request, *args, **kwargs)
        raise exceptions.PermissionDenied


@api_view(['DELETE'])
def delete_lesson(request, _id):
    to_delete = Lesson.objects.all()
    to_delete.get(id=_id).delete()
    return Response(_id)


class MaterialViewSet(viewsets.ModelViewSet):
    permission_classes = [CourseStaffOrReadOnlyForStudents]
    serializer_class = MaterialSerializer
    queryset = LessonContent.objects.all()
    filterset_fields = ['lesson_id', ]
