from rest_framework import permissions
from course.models import Course
from lesson.models import LessonContent


def object_to_course(obj):
    from course.models import Course
    from lesson.models import Lesson
    from problem.models import Problem, Submit

    course = None
    if isinstance(obj, Course):
        course = obj
    if isinstance(obj, Lesson):
        course = obj.course
    if isinstance(obj, Problem):
        course = obj.lesson.course
    if isinstance(obj, Submit):
        course = obj.problem.lesson.course
    if isinstance(obj, LessonContent):
        course = obj.lesson.course
    if hasattr(obj, 'course'):
        course = obj.course
    if hasattr(obj, 'lesson'):
        course = obj.lesson.course
    if hasattr(obj, 'problem'):
        course = obj.problem.lesson.course
    if not course:
        raise Exception
    return course


class CourseStaffOrReadOnlyForStudents(permissions.BasePermission):
    message = 'Edit it without staff status not allowed.'

    def has_object_permission(self, request, view, obj):
        if not bool(request.user and request.user.is_authenticated):
            return False
        course = object_to_course(obj)

        if course in request.user.staff_for.all():
            return True
        if course in request.user.author_for.all():
            return True
        if course not in request.user.student_for.all():
            return False
        return request.method in permissions.SAFE_METHODS


class CourseStaffOrAuthorReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not bool(request.user and request.user.is_authenticated):
            return False
        if object_to_course(obj) in request.user.staff_for.all():
            return True
        if hasattr(obj, 'student') and obj.student == request.user:
            return request.method in permissions.SAFE_METHODS
        return False


class CourseStaffOrAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not bool(request.user and request.user.is_authenticated):
            return False
        if object_to_course(obj) in request.user.staff_for.all():
            return True
        if hasattr(obj, 'author') and obj.author == request.user:
            return True
        return False

    def has_permission(self, request, view):
        if not bool(request.user and request.user.is_authenticated):
            return False
        if 'course_id' in view.kwargs:
            queryset = Course.objects.filter(id=view.kwargs['course_id'])
            if queryset.exists() and queryset.first() in request.user.staff_for.all():
                return True
        if 'lesson_id' in view.kwargs:
            queryset = Course.objects.filter(lessons__id=view.kwargs['lesson_id'])
            if queryset.exists() and queryset.first() in request.user.staff_for.all():
                return True
        if 'problem_id' in view.kwargs:
            queryset = Course.objects.filter(lessons__problems__id=view.kwargs['problem_id'])
            if queryset.exists() and queryset.first() in request.user.staff_for.all():
                return True
        return False


class UserItselfOrReadonly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not bool(request.user and request.user.is_authenticated):
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user.id == obj
