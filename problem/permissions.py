from rest_framework import permissions
from problem.models import LogEvent
from users.permissions import object_to_course


class LogEventPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj: LogEvent):
        if not bool(request.user and request.user.is_authenticated):
            return False
        course = object_to_course(obj)

        if course in request.user.staff_for.all():
            return True
        if course in request.user.author_for.all():
            return True
        if course not in request.user.student_for.all():
            return False
        if obj.student == request.student and obj.type == obj.TYPE_MESSAGE:
            return True
        if obj.student == request.student:
            return request.method in permissions.SAFE_METHODS
