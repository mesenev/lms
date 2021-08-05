from django.db.models import Q, Min
from rest_framework import viewsets, exceptions
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from lesson.models import Lesson, LessonContent, LessonInSchedule
from lesson.serializers import LessonSerializer, MaterialSerializer, LessonShortSerializer
from course.models import Course, CourseSchedule
from users.management.commands.registergroups import TEACHER
from users.permissions import CourseStaffOrReadOnlyForStudents


class LessonViewSet(viewsets.ModelViewSet):
    permission_classes = [CourseStaffOrReadOnlyForStudents]
    serializer_class = LessonSerializer
    filterset_fields = ['course_id', ]

    def get_queryset(self):
        user = self.request.user
        course_id = self.request.query_params.get('course_id')
        course_name = Course.objects.get(id=course_id)
        lessons = Lesson.objects.prefetch_related('problems', 'progress', 'materials').filter(
            ((Q(is_hidden=False) & Q(course__in=user.student_for.all()))
             | Q(course__in=user.staff_for.all())
             | Q(course__in=user.author_for.all()))
            & Q(course__name=course_name)
        )
        ordered_lessons = list()
        for lesson in lessons:
            try:
                for position in lesson.course.schedule.lessons:
                    ordered_lessons.append((position['lesson']['id'], position['lesson']['name']))
            except CourseSchedule.DoesNotExist:
                return Lesson.objects.none()
        ordered_lessons = sorted(list(set(ordered_lessons)), key=lambda x: x[0])
        bulk_lesson_in_schedule = [LessonInSchedule(lesson=Lesson.objects.get(name=name),
                                                    course=Course.objects.get(id=course_id),
                                                    order=schedule_id) for schedule_id, name in ordered_lessons]
        LessonInSchedule.objects.bulk_create(bulk_lesson_in_schedule)
        lessons = lessons.annotate(lesson_order=Min('lessoninschedule__order')).order_by('lesson_order')
        return lessons


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = LessonShortSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, **kwargs):
        queryset = self.get_queryset()
        user = get_object_or_404(queryset, pk=pk)
        serializer = LessonSerializer(user)
        print('='*50, 'and here too00')
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if request.user.groups.filter(name=TEACHER).exists():
            return super().create(request, *args, **kwargs)
        raise exceptions.PermissionDenied


@api_view(['DELETE'])
def delete_lesson(request, id):
    deletedLesson = Lesson.objects.all()
    deletedLesson.get(id=id).delete()
    return Response(id)


class MaterialViewSet(viewsets.ModelViewSet):
    permission_classes = [CourseStaffOrReadOnlyForStudents]
    serializer_class = MaterialSerializer
    queryset = LessonContent.objects.all()
    filterset_fields = ['lesson_id', ]
