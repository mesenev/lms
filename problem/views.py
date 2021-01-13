from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
)
from rest_framework.viewsets import GenericViewSet

from problem.models import Problem, Submit
from problem.serializers import ProblemSerializer, SubmitSerializer
from users.models import User


class ProblemViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin):
    serializer_class = ProblemSerializer
    queryset = Problem.objects.all()


class SubmitViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin):
    serializer_class = SubmitSerializer
    queryset = Submit.objects.all()

    def get_queryset(self):
        request = self.get_serializer_context()['request']
        problem_id = request.query_params.get('problem', None)
        user_id = request.query_params.get('user', None)

        if problem_id:
            user = User.objects.get(pk=user_id) if user_id else None
            is_staff = True if user and user.is_staff else False
            if is_staff:
                return Submit.objects.filter(problem__id=problem_id)
            elif user:
                return Submit.objects.filter(problem__id=problem_id, student__id=user_id)

        return Submit.objects.all()
