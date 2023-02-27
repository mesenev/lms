from rest_framework import viewsets, exceptions
from users.permissions import CourseStaffOrReadOnlyForStudents
from test.models import Test
from django.db.models import Q
from imcslms.default_settings import TEACHER
from test.serializers import TestSerializer
from model_bakery import baker
from rest_framework.request import Request
from rest_framework.views import APIView


class AddAttachmentToQuestion(APIView):

    def post(self, request: Request):
        pass


class TestViewSet(viewsets.ModelViewSet):
    serializer_class = TestSerializer
    permission_classes = [CourseStaffOrReadOnlyForStudents]

    def get_queryset(self):
        user = self.request.user
        return Test.objects.all().filter(
            (Q(lesson__course__in=user.student_for.all()))
            | Q(lesson__course__in=user.staff_for.all())
            | Q(lesson__course__in=user.author_for.all())
        )

    def create(self, request, *args, **kwargs):
        if request.user.groups.filter(name=TEACHER).exists():
            return super().create(request, *args, **kwargs)
        raise exceptions.PermissionDenied
