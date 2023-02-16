from rest_framework import viewsets
from users.permissions import CourseStaffOrReadOnlyForStudents
from test.serializers import TestSerializer
from test.models import Test
from django.db.models import Q


class TestViewSet(viewsets.ModelViewSet):
    serializer_class = TestSerializer
    permission_classes = [CourseStaffOrReadOnlyForStudents]

    def get_queryset(self):
        user = self.request.user
        return Test.objects.filter(
            (Q(test__is_teacher_only=False)
             & Q(lesson__course__in=user.student_for.all())
             )
            | Q(lesson__course__in=user.staff_for.all())
            | Q(lesson__course__in=user.author_for.all())
        )
