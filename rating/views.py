from django.db.models import Prefetch, F
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from course.models import Course
from rating.models import LessonProgress, CourseProgress
from rating.serializers import LessonProgressSerializer, CourseProgressSerializer, AttendanceSerializer
from users import permissions
from users.permissions import CourseStaffOrAuthor


class CourseProgressViewSet(viewsets.ModelViewSet):
    #TODO: Fix permission
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CourseProgressSerializer
    queryset = CourseProgress.objects.all()
    filterset_fields = ['user_id', 'course_id']


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
