import django_filters
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
)
from rest_framework.viewsets import GenericViewSet
from users.models import StudyGroup
from users.permissions import UserItselfOrReadonly
from users.serializers import DefaultUserSerializer, StudyGroupsSerializer
from users.utils import *


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
