from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
)
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from cathie.cats_api import cats_get_problem_description_by_url, cats_submit_solution
from lesson.models import Lesson
from problem.models import Problem, Submit
from problem.serializers import ProblemSerializer, SubmitSerializer
from users.models import User


class ProblemViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin):
    serializer_class = ProblemSerializer
    queryset = Problem.objects.all()


class SubmitViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin):
    serializer_class = SubmitSerializer
    queryset = Submit.objects.all()

    def perform_create(self, serializer):
        request = serializer.context["request"]
        validated_data = serializer.validated_data
        cats_request_id = cats_submit_solution(
            validated_data.get('content'),
            validated_data.get('cats_problem_id'),
            validated_data.get('cats_de_id'),
            validated_data.get('source')
        )
        serializer.save(student=request.user, cats_request_id=cats_request_id, status=Submit.DEFAULT_STATUS)

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


@login_required
@api_view(['POST'])
@renderer_classes([JSONRenderer])
def add_cats_problems(request, lesson_id):
    lesson = Lesson.objects.get(pk=lesson_id)
    data = request.data
    answer = list()
    for cats_problem in data:
        materials = cats_get_problem_description_by_url(cats_problem["text_url"])
        problem = Problem.objects.create(
            lesson=lesson, author=request.user, name=cats_problem['name'],
            cats_id=cats_problem['id'], cats_material_url=cats_problem["text_url"],
            description=materials,
        )
        answer.append(ProblemSerializer(problem).data)
    return Response(answer)
