import json

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core import exceptions
from django.forms import Form, CharField, PasswordInput
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from course.models import Course
from users.models import User, CourseAssignTeacher, StudyGroup
from users.serializers import DefaultUserSerializer, StudyGroupsSerializer


def index(request, *args, **kwargs):
    return render(request, 'index.html')


class LoginForm(Form):
    username = CharField()
    password = CharField(widget=PasswordInput)


class UsersViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin):
    serializer_class = DefaultUserSerializer
    queryset = User.objects.all()


class StudyGroupsViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin):
    queryset = StudyGroup.objects.all()
    serializer_class = StudyGroupsSerializer


class Logout(APIView):
    def get(self, request):
        logout(request)
        return redirect('index')


@permission_classes(IsAuthenticated)
@api_view(['GET'])
@renderer_classes([JSONRenderer])
def students_for_course(request: HttpRequest, course_id):
    queryset = User.objects.exclude(student_for__id=course_id).exclude(staff_for__id=course_id) \
        .all().values_list('id', 'username', 'first_name', 'middle_name', 'last_name', 'avatar_url')
    return Response(list(queryset))


@login_required
@api_view(['GET'])
@renderer_classes([JSONRenderer])
def find_teacher_by_email(request: HttpRequest, course_id, email):
    queryset = Group.objects.get(name='teacher').user_set.filter(email__icontains=email) \
        .exclude(staff_for__id=course_id).all()
    serializer = DefaultUserSerializer(queryset, many=True)
    if len(serializer.data) != 0:
        return Response(serializer.data)
    else:
        return HttpResponse("No match found :(")


@login_required
@api_view(['POST'])
@renderer_classes([JSONRenderer])
def assign_teacher(request, course_id):
    course = Course.objects.get(id=course_id)
    for user_data in request.data:
        user = User.objects.get(id=user_data['id'])
        not_exist = not CourseAssignTeacher.objects.filter(course=course, user=user).count()
        if not_exist:
            assignment = CourseAssignTeacher(course=course, user=user)
            assignment.save()
    return Response(status=201)


@login_required
@api_view(['GET'])
@renderer_classes([JSONRenderer])
def staff_for_course(request: HttpRequest, course_id):
    try:
        group = Group.objects.get(name='staff')
    except exceptions.ObjectDoesNotExist:
        return Response(list())
    queryset = User.objects \
        .filter(group=group) \
        .exclude(student_for__id=course_id) \
        .exclude(staff_for__id=course_id) \
        .values_list('id', 'username', 'first_name', 'middle_name', 'last_name', 'avatar_url')
    return Response(list(queryset))


@login_required
@api_view(['POST'])
@renderer_classes([JSONRenderer])
def change_password(request):
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    user = request.user
    if not user.check_password(old_password):
        return HttpResponse('Unauthorized', status=401)
    user.set_password(new_password)
    user.save()
    return Response({'code': 0, 'message': 'Password changed successfully'})


@login_required
@api_view(['POST'])
@renderer_classes([JSONRenderer])
def change_avatar(request):
    new_avatar = request.data.get('avatar_url')
    user = request.user
    user.avatar_url = new_avatar
    user.save()
    return Response({'code': 0, 'message': str(user.avatar_url.url)})


@login_required
@api_view(['POST'])
@renderer_classes([JSONRenderer])
def edit_profile(request):
    user = request.user
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    study_group = request.data.get('study_group')
    username = request.data.get('username')
    email = request.data.get('email')
    if first_name and first_name != user.first_name:
        user.first_name = first_name
    if last_name and last_name != user.last_name:
        user.last_name = last_name
    if username and username != user.username:
        user.username = username
    if study_group:
        study_group = StudyGroup.objects.get(study_group__exact=f'{study_group}')
        if study_group != user.study_group:
            user.study_group = study_group
    if email and email != user.email:
        user.email = email
    user.save()
    return Response({'code': 0, 'message': 'Profile edited successfully'})
