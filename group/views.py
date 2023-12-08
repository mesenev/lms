from django.shortcuts import render
from rest_framework import viewsets
from group.serializers import GroupSerializer
from group.models import Group
from rest_framework.decorators import action
from users.models import GroupAssignTeacher, GroupAssignStudent, User
from users.serializers import DefaultUserSerializer
from rest_framework.response import Response


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()

    @action(
        detail=True, methods=['post'], url_path=r'assign-teacher', url_name='assign-teacher',
    )
    def assign_teacher(self, request, pk=None):
        group = self.get_object()
        user = User.objects.get(id=request.data['id'])
        if not user:
            return Response(dict(code=1, message='User not exist'))
        exist = GroupAssignTeacher.objects.filter(group=group, user=user).exists()
        if exist:
            return Response(dict(code=1, message='User already assigned'))
        if not exist:
            assignment = GroupAssignTeacher(group=group, user=user)
            assignment.save()
            return Response(dict(code=0, message='User successfully assigned'))

    @action(
        detail=True, methods=['post'], url_path=r'assign-student', url_name='assign-student',
    )
    def assign_student(self, request, pk=None):
        group = self.get_object()
        user = User.objects.get(id=request.data['id'])
        if not user:
            return Response(dict(code=1, message='User not exist'))
        exist = GroupAssignStudent.objects.filter(group=group, user=user).exists()
        if exist:
            return Response(dict(code=1, message='User already assigned'))
        if not exist:
            assigment = GroupAssignStudent(group=group, user=user)
            assigment.save()
            return Response(dict(code=0, message='User succesfully assigned'))