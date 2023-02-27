import django_filters
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework.response import Response
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
)
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from users.permissions import UserItselfOrReadonly
from users.serializers import DefaultUserSerializer, StudyGroupsSerializer
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



# class StudyGroupsViewSet(
#     GenericViewSet, CreateModelMixin,
#     RetrieveModelMixin, UpdateModelMixin, ListModelMixin
# ):
#     queryset = StudyGroup.objects.all()
#     serializer_class = StudyGroupsSerializer
