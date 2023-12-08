from django.shortcuts import render
from rest_framework import viewsets
from group.serializers import GroupSerializer
from group.models import Group
from rest_framework.decorators import action
from users.models import GroupAssignTeacher, GroupAssignStudent
from rest_framework.response import Response


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()

    @action(
        detail=True, methods=['post'], url_path=r'assign-teacher', url_name='assign-teacher',
    )
    def assign_teacher(self, request, pk=None):
        group = self.get_object()
        user = request.data
        exist = GroupAssignTeacher.objects.filter(group=group, user=user).exists()
        if exist:
            return Response(dict(code=1, message='User already assigned'))
        if not exist:
            assignment = GroupAssignTeacher(course=course, user=user)
            assignment.save()
            return Response(dict(code=0, message='User successfully assigned'))

    @action(
        detail=True, methods=['post'], url_path=r'assign-student', url_name='assign-student',
    )
    def assign_student(self, request, pk=None):
        group = self.get_object()
        user = request.data
        exist = GroupAssignStudent.objects.filter(group=group, user=user).exists()
        if exist:
            return Response(dict(code=1, message='User already assigned'))
        if not exist:
            assigment = GroupAssignStudent(course=course, user=user)
            assigment.save()
            return Response(dict(code=0, message='User succesfully assigned'))

        return Response(dict(code=0, message='url_allowed'))