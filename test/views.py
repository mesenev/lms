from rest_framework import viewsets, exceptions
from users.permissions import CourseStaffOrReadOnlyForStudents
from test.models import Test, TestSolution
from django.db.models import Q
from imcslms.default_settings import TEACHER
from test.serializers import TestSerializer, TestSolutionSerializer
from model_bakery import baker
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response


class AddAttachmentToQuestion(APIView):

    def post(self, request: Request):
        pass


class TestViewSet(viewsets.ModelViewSet):
    serializer_class = TestSerializer
    permission_classes = [CourseStaffOrReadOnlyForStudents]
    filterset_fields = ['lesson_id', ]

    def get_queryset(self):
        user = self.request.user
        return Test.objects.all()\
            .filter(
            (Q(lesson__course__in=user.student_for.all()))
            | Q(lesson__course__in=user.staff_for.all())
            | Q(lesson__course__in=user.author_for.all())
        )

    def create(self, request, *args, **kwargs):
        if request.user.groups.filter(name=TEACHER).exists():
            return super().create(request, *args, **kwargs)
        raise exceptions.PermissionDenied


class TestSolutionViewSet(viewsets.ModelViewSet):
    serializer_class = TestSolutionSerializer
    permission_classes = [CourseStaffOrReadOnlyForStudents]
    filterset_fields = ['test', ]

    def get_queryset(self):
        user = self.request.user
        return TestSolution.objects.all().filter(
            (Q(test__is_hidden=False)
             & Q(test__lesson__course__in=user.student_for.all())
             )
            | Q(test__lesson__course__in=user.staff_for.all())
            | Q(test__lesson__course__in=user.author_for.all())
        )

    def create(self, request, *args, **kwargs):
        if request.user.groups.filter(name=TEACHER).exists():
            return super().create(request, *args, **kwargs)
        raise exceptions.PermissionDenied

    def filter_queryset(self, queryset):
        return super().filter_queryset(queryset)