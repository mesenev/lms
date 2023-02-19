from datetime import timedelta

import django_filters
from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
)
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from users.models import ResetPasswordToken
from users.permissions import UserItselfOrReadonly
from users.serializers import DefaultUserSerializer, StudyGroupsSerializer, \
    TokenValidationSerializer, PasswordTokenSerializer, EmailSerializer
from users.utils import *
from rest_framework.request import Request


def index(request, *args, **kwargs):
    return render(request, 'index.html')


class UserFilter(FilterSet):
    group = django_filters.CharFilter(field_name='group', label='group in', method='group_filter')

    def group_filter(self, queryset, name, value):
        return queryset.filter(groups__name__in=[value])

    class Meta:
        model = User
        fields = {
            'email': ['exact', 'icontains'],
        }


class changeAvatar(APIView):
    def post(self, request: Request):
        new_avatar = request.data.get('avatar_url')
        user = request.user
        user.avatar_url = new_avatar
        user.save()
        return Response({'code': 0, 'message': str(user.avatar_url.url)})


class UsersViewSet(
    GenericViewSet, CreateModelMixin,
    RetrieveModelMixin, UpdateModelMixin, ListModelMixin
):
    permission_classes = [UserItselfOrReadonly]
    serializer_class = DefaultUserSerializer
    queryset = User.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = UserFilter


class RequestTokenAPIView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = EmailSerializer

    def post(self, request, *args, **kwargs):
        data = self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)
        email = data.validated_data["email"]
        expiry_time = timezone.now() - timedelta(hours=getattr(settings, "TOKEN_EXPIRY_TIME", 24))
        ResetPasswordToken.objects.filter(created_at__lte=expiry_time).delete()
        user = User.objects.filter(email__iexact=email).first()
        if user is None:
            return Response(status=404, data={"message": "There is no user with the email provided."})
        if len(user.password_reset_tokens.all()):
            token = user.password_reset_tokens.all().first()
        else:
            token = ResetPasswordToken(user=user)
        token.request = request
        token.save()
        return Response(status=200, data={"status": "OK"})


class ChangePasswordWithTokenAPIView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = PasswordTokenSerializer

    def post(self, request, *args, **kwargs):
        data = self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)
        password = data.validated_data["password"]
        user_token = data.validated_data["token"] \
            if data.validated_data["token"] \
            else request.query_params.get("token")
        if user_token:
            user_token = ResetPasswordToken.objects.filter(key=user_token).first()

        else:
            return Response(status=404, data={"message": "Bad token"})
        try:
            validate_password(password, user=user_token.user)
        except ValidationError:
            return Response(status=400, data={"message": "Bad password"})
        user_token.user.set_password(password)
        user_token.user.save()
        ResetPasswordToken.objects.filter(user=user_token.user).delete()
        return Response(status=200, data={"status": "OK"})


class VerifyTokenExists(APIView):
    permission_classes = (AllowAny, )
    serializer_class = TokenValidationSerializer

    def get(self, request, *args, **kwargs):
        data = self.serializer_class(data={"token": request.query_params.get('token')})
        data.is_valid(raise_exception=True)
        return Response(data={"status": "OK"})

# class StudyGroupsViewSet(
#     GenericViewSet, CreateModelMixin,
#     RetrieveModelMixin, UpdateModelMixin, ListModelMixin
# ):
#     queryset = StudyGroup.objects.all()
#     serializer_class = StudyGroupsSerializer
