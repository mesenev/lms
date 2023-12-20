from django.db.models import Q
from rest_framework import viewsets, exceptions, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from cathie.cats_api import cats_get_problem_description_by_url
from course.models import CourseSchedule, Course
from imcslms.default_settings import TEACHER
from lesson.models import Lesson, LessonContent, Attachment
from lesson.serializers import LessonSerializer, MaterialSerializer, LessonShortSerializer, AddCatsProblemSerializer, \
    AttachmentSerializer
from problem.models import Problem
from problem.serializers import ProblemSerializer
from users.permissions import CourseStaffOrReadOnlyForStudents
import base64
from django.core.files.base import ContentFile


class LessonViewSet(viewsets.ModelViewSet):
    permission_classes = [CourseStaffOrReadOnlyForStudents]
    serializer_class = LessonSerializer
    filterset_fields = ['course_id', ]

    def get_queryset(self):

        user = self.request.user
        user_courses_as_author = user.author_for.all()

        user_courses_as_student = []
        for group in user.student_for.all():
            user_courses_as_student += Course.objects.filter(source_for=group)

        user_courses_as_staff = []
        for group in user.staff_for.all():
            user_courses_as_staff += Course.objects.filter(source_for=group)

        return Lesson.objects.prefetch_related('problems', 'progress', 'materials', 'exams').filter(
            (Q(is_hidden=False) & Q(course__in=user_courses_as_student) | Q(course__in=user_courses_as_author)
             |Q(course__in=user_courses_as_staff))
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
            materials = cats_get_problem_description_by_url('https://imcs.dvfu.ru/cats/'+cats_problem["text_url"])
            problem = Problem.objects.create(
                lesson=lesson, author=request.user, name=cats_problem['name'],
                cats_id=cats_problem['id'], cats_material_url='https://imcs.dvfu.ru/cats/'+cats_problem["text_url"],
                description=materials, test_mode=cats_problem['test_mode'],
                type=Problem.PROBLEM_TYPES[problem_type][0]
            )
            answer.append(problem)
        return Response(ProblemSerializer(answer, many=True).data)

    def destroy(self, request, *args, **kwargs):
        instance: Lesson = self.get_object()
        schedule = CourseSchedule.objects.get(course=instance.course)
        schedule.lessons = list(filter(lambda x: x['lesson_id'] != instance.id, schedule.lessons))
        schedule.save()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class MaterialViewSet(viewsets.ModelViewSet):
    permission_classes = [CourseStaffOrReadOnlyForStudents]
    serializer_class = MaterialSerializer
    filterset_fields = ['lesson_id', ]

    def get_queryset(self):
        user = self.request.user
        student_course = []
        staff_course = []

        for group in user.student_for.all():
            student_course.append(group.course)

        for group in user.staff_for.all():
            staff_course.append(group.course)

        return LessonContent.objects.all().filter(
            (Q(is_teacher_only=False) & Q(lesson__course__in=student_course))
            | Q(lesson__course__in=staff_course)
            | Q(lesson__course__in=user.author_for.all())
        )

    def create(self, request, *args, **kwargs):
        if request.user.groups.filter(name=TEACHER).exists():
            return super().create(request, *args, **kwargs)
        raise exceptions.PermissionDenied


class AttachmentViewSet(viewsets.ModelViewSet):
    permission_classes = [CourseStaffOrReadOnlyForStudents]
    serializer_class = AttachmentSerializer
    filterset_fields = ['material_id', ]

    def get_queryset(self):
        user = self.request.user
        return Attachment.objects.all().filter(
            (Q(material__is_teacher_only=False)
             & Q(material__lesson__course__in=user.student_for.all())
             )
            | Q(material__lesson__course__in=user.staff_for.all())
            | Q(material__lesson__course__in=user.author_for.all())
        )

    def create(self, request, *args, **kwargs):
        if request.user.groups.filter(name=TEACHER).exists():
            request.data['file_url'] = ContentFile(base64.b64decode(request.data['file_url']),
                                                   name=request.data['name'])
            return super().create(request, *args, **kwargs)
        raise exceptions.PermissionDenied

    def filter_queryset(self, queryset):
        return super().filter_queryset(queryset)
