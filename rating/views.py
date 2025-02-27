from django.db.models import Prefetch, F, Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from course.models import Course
from rating.models import LessonProgress, CourseProgress
from rating.serializers import LessonProgressSerializer, CourseProgressSerializer, AttendanceSerializer
from users import permissions
from users.permissions import CourseStaffOrAuthor


class CourseProgressViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CourseProgressSerializer
    filterset_fields = ['user_id', 'course_id']

class CourseProgressViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CourseProgressSerializer
    filterset_fields = ['user_id', 'course_id']

    def get_queryset(self):
        user = self.request.user

        # Если пользователь является преподавателем
        if user.assigns_as_teacher.exists():  # Проверяем, есть ли у пользователя роль преподавателя
            # Получаем все группы, где пользователь является преподавателем
            groups_where_teacher = user.assigns_as_teacher.all()
            # Извлекаем только связанные CourseGroup
            course_groups = [assignment.group for assignment in groups_where_teacher]
            # Получаем все курсы, связанные с этими группами
            courses_where_teacher = Course.objects.filter(source_for__in=course_groups)
            # Фильтруем CourseProgress по этим курсам
            return CourseProgress.objects.filter(course__in=courses_where_teacher)

        # Если пользователь является студентом
        else:
            # Студент видит только свой прогресс
            return CourseProgress.objects.filter(user=user)

class LessonProgressViewSet(viewsets.ModelViewSet):
    permission_classes = [CourseStaffOrAuthor]
    serializer_class = LessonProgressSerializer
    queryset = LessonProgress.objects.all()
    filterset_fields = ['lesson_id']

    @action(detail=False, url_path='attendance-by-course/(?P<course_id>\d+)')
    def attendance_by_course(self, request, course_id):
        q = Course.objects.get(id=course_id).students.all().prefetch_related(
            Prefetch(
                'lessonprogress_set',
                queryset=self.queryset.filter(
                    user_id=F('user_id'), lesson__course_id=course_id
                ).order_by('id')
            )
        )
        answer = {
            user.id: AttendanceSerializer(list(user.lessonprogress_set.all()), many=True).data
            for user in q
        }
        return Response(answer)
