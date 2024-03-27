from rest_framework import permissions
from course.models import Course
from lesson.models import LessonContent, Attachment
from exam.models import ExaminationForm, ExamSolution
from group.models import CourseGroup

from rest_framework.permissions import IsAuthenticated


def object_to_course(obj):
    from course.models import Course
    from lesson.models import Lesson
    from problem.models import Problem, Submit

    course = None
    if isinstance(obj, Course):
        course = obj
    if isinstance(obj, CourseGroup):
        course = obj.course
    if isinstance(obj, Lesson):
        course = obj.course
    if isinstance(obj, Problem):
        course = obj.lesson.course
    if isinstance(obj, Submit):
        course = obj.problem.lesson.course
    if isinstance(obj, LessonContent):
        course = obj.lesson.course
    if isinstance(obj, ExaminationForm):
        course = obj.lesson.course
    if isinstance(obj, ExamSolution):
        course = obj.exam.lesson.course
    if isinstance(obj, Attachment):
        course = obj.material.lesson.course
    if hasattr(obj, 'course'):
        course = obj.course
    if hasattr(obj, 'group'):
        course = obj.group.course
    if hasattr(obj, 'lesson'):
        course = obj.lesson.course
    if hasattr(obj, 'problem'):
        course = obj.problem.lesson.course
    if hasattr(obj, 'exam'):
        course = obj.exam.lesson.course
    if not course:
        raise Exception('No course found')
    return course


class CourseStaffOrReadOnlyForStudents(permissions.IsAuthenticated):
    message = 'Edit it without staff status not allowed.'

    def has_object_permission(self, request, view, obj):
        if not bool(request.user and request.user.is_authenticated):
            return False
        course = object_to_course(obj)

        if request.user.staff_for.filter(course=course):
            return True
        if course in request.user.author_for.all():
            return True
        if not request.user.student_for.filter(course=course):
            return False
        return request.method in permissions.SAFE_METHODS


class CourseStaffOrAuthorReadOnly(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if not bool(request.user and request.user.is_authenticated):
            return False

        course = object_to_course(obj)
        if request.user.staff_for.filter(course=course):
            return True
        if hasattr(obj, 'student') and obj.student == request.user:
            return request.method in permissions.SAFE_METHODS
        return False


class CourseStaffOrAuthor(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if not bool(request.user and request.user.is_authenticated):
            return False

        course = object_to_course(obj)

        if request.user.staff_for.filter(course=course):
            return True
        if hasattr(obj, 'author') and obj.author == request.user:
            return True
        return False

    def has_permission(self, request, view):
        if not bool(request.user and request.user.is_authenticated):
            return False
        if request.user.is_superuser:
            return True
        if request.method not in permissions.SAFE_METHODS:
            if request.data.get('lesson'):
                queryset = Course.objects.filter(lessons__id=request.data['lesson'])
                if queryset.exists() and request.user.staff_for.get(course=queryset.first):
                    return True
        params = {**view.kwargs, **{key: int(value) for key, value in request.query_params.items()}}
        if 'course_id' in params.keys():
            queryset = Course.objects.filter(id=params['course_id'])
            if queryset.exists() and request.user.staff_for.get(course=queryset.first):
                return True
        if 'lesson_id' in params.keys():
            queryset = Course.objects.filter(lessons__id=params['lesson_id'])
            if queryset.exists() and request.user.staff_for.get(course=queryset.first):
                return True
        if 'problem_id' in params.keys():
            queryset = Course.objects.filter(lessons__problems__id=params['problem_id'])
            if queryset.exists() and request.user.staff_for.get(course=queryset.first):
                return True
        return False


class UserItselfOrReadonly(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if not bool(request.user and request.user.is_authenticated):
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user.id == obj.id
