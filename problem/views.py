from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
)
from rest_framework.viewsets import GenericViewSet

from problem.models import Problem, Submit
from problem.serializers import ProblemSerializer, SubmitSerializer


class ProblemViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin):
    serializer_class = ProblemSerializer
    queryset = Problem.objects.all()


class SubmitViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin):
    serializer_class = SubmitSerializer
    queryset = Submit.objects.all()
