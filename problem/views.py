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

    def get_queryset(self):
        request = self.get_serializer_context()['request']
        if request.query_params.get('problem', False):
            problem = int(request.query_params['problem'][0])
            return Submit.objects.filter(problem__id=problem)
        return Submit.objects.all()
