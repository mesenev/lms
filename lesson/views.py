from django.db.models import Q
from rest_framework import viewsets, exceptions
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from cathie.cats_api import cats_get_problem_description_by_url
from imcslms.default_settings import TEACHER
from lesson.models import Lesson, LessonContent
from lesson.serializers import LessonSerializer, MaterialSerializer, LessonShortSerializer, AddCatsProblemSerializer
from problem.models import Problem
from problem.serializers import ProblemSerializer
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

    @action(detail=True, methods=['POST'], serializer_class=AddCatsProblemSerializer)
    def add_cats_problems(self, request, pk):
        lesson = get_object_or_404(self.get_queryset(), pk=pk)
        serializer: AddCatsProblemSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        problem_data = serializer.validated_data['problem_data']
        problem_type = serializer.validated_data['problem_type']
        answer = list()
        for cats_problem in problem_data:
            materials = cats_get_problem_description_by_url(cats_problem["text_url"])
            problem = Problem.objects.create(
                lesson=lesson, author=request.user, name=cats_problem['name'],
                cats_id=cats_problem['id'], cats_material_url=cats_problem["text_url"],
                description=materials, test_mode=cats_problem['test_mode'],
                type=Problem.PROBLEM_TYPES[problem_type][0]
            )
            answer.append(problem)
        return Response(ProblemSerializer(answer, many=True).data)


class MaterialViewSet(viewsets.ModelViewSet):
    permission_classes = [CourseStaffOrReadOnlyForStudents]
    serializer_class = MaterialSerializer
    queryset = LessonContent.objects.all()
    filterset_fields = ['lesson_id', ]
