import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core import exceptions

from django.forms import Form, CharField, PasswordInput, ValidationError
from django.core.validators import EmailValidator
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
)
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from course.models import Course
from users.models import User, CourseAssignTeacher
from users.serializers import DefaultUserSerializer

import re


@login_required(login_url=reverse_lazy('account_login'))
def index(request, *args, **kwargs):
    user = User.objects.prefetch_related('staff_for', 'student_for').get(pk=request.user.id)
    user_data = json.dumps(DefaultUserSerializer(instance=user, exclude_staff=False).data)
    return render(request, 'index.html', context=dict(user_data=user_data))


class LoginForm(Form):
    username = CharField()
    password = CharField(widget=PasswordInput)


class RegistrationForm(Form):
    email = CharField()
    username = CharField()
    first_name = CharField()
    last_name = CharField()
    password = CharField(label='Password', widget=PasswordInput)
    repeat_password = CharField(label='Repeat password', widget=PasswordInput)

    def clean_email(self):
        try:
            User.objects.get(email=self.get_email())
            raise ValidationError('Email уже используется')
        except User.DoesNotExist:
            validate_email = EmailValidator(message='Некорректный email')
            validate_email(self.get_email())

    def clean_username(self):
        try:
            User.objects.get(username=self.get_username())
            raise ValidationError('Логин уже занят')
        except User.DoesNotExist:
            if re.search("[^A-Za-z0-9_-]$", self.get_username()):
                raise ValidationError('Недопустимые символы')
            return

    def clean_first_name(self):
        if re.search("[^A-Za-zА-Яа-я]$", self.get_first_name()):
            raise ValidationError('Недопустимые символы')

    def clean_last_name(self):
        if re.search("[^A-Za-zА-Яа-я]$", self.get_last_name()):
            raise ValidationError('Недопустимые символы')

    def clean_password(self):
        if re.search("[^A-Za-z0-9_-]$", self.get_password()):
            raise ValidationError('Недопустимые символы')

        if len(self.get_password()) < 6:
            raise ValidationError('Недостаточная длина')

    def clean_repeat_password(self):
        if self.get_password() != self.data['repeat_password']:
            raise ValidationError('Пароли не совпадают')

    def get_password(self):
        return self.data['password']

    def get_username(self):
        return self.data['username']

    def get_email(self):
        return self.data['email']

    def get_first_name(self):
        return self.data['first_name']

    def get_last_name(self):
        return self.data['last_name']


def user_registration(request):
    if request.method == 'GET':
        return render(request, 'registration.html', {'form': RegistrationForm()})
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if not form.is_valid():
            return render(request, 'registration.html', {'form': form})
        new_user = User()
        new_user.set_password(form.get_password())
        new_user.username = form.get_username()
        new_user.email = form.get_email()
        new_user.first_name = form.get_first_name()
        new_user.last_name = form.get_last_name()
        new_user.save()
        return redirect('index')


def user_login(request):
    if request.method == 'GET':
        return render(request, 'login.html', {'form': LoginForm()})

    form = LoginForm(request.POST)
    ctx = dict(error=True, form=form)
    if not form.is_valid():
        return render(request, 'login.html', dict(**ctx, message='Ошибка чтения формы (ง’̀-‘́)ง'))
    user = authenticate(**form.cleaned_data)
    if user and user.is_active:
        login(request, user)
        return redirect('index')
    if user and not user.is_active:
        return render(request, 'login.html', dict(
            **ctx, error_message='Аккаунт заблокирован. Обратитесь к системному администратору.'
        ))
    try:
        User.objects.get(username=form.cleaned_data['username'])
    except User.DoesNotExist:
        return render(request, 'login.html', dict(**ctx, error_message='Указанный пользователь не существует.'))
    return render(request, 'login.html', dict(**ctx, error_message='Логин и пароль не совпадают'))


class UsersViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin):
    serializer_class = DefaultUserSerializer
    queryset = User.objects.all()


class Logout(APIView):
    def get(self, request):
        logout(request)
        return redirect('index')


@login_required
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
    queryset = User.objects.filter(email__icontains=email).exclude(staff_for__id=course_id).all()
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
