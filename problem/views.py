from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from cathie.cats_api import cats_get_problem_description_by_url
from lesson.models import Lesson
from problem.models import Problem, Submit, CatsSubmit
from problem.serializers import ProblemSerializer, SubmitSerializer
from users.models import User


class ProblemViewSet(viewsets.ModelViewSet):
    serializer_class = ProblemSerializer
    queryset = Problem.objects.all()
    filterset_fields = ['lesson_id', ]


class SubmitViewSet(viewsets.ModelViewSet):
    serializer_class = SubmitSerializer
    queryset = Submit.objects.prefetch_related('cats_submit').all()

    def perform_create(self, serializer):
        request = serializer.context["request"]
        validated_data = serializer.validated_data
        cats = CatsSubmit(data=dict(
            source_text=validated_data.get('content'),
            problem_id=validated_data.get('cats_problem_id'),
            de_id=validated_data.get('cats_de_id'),
            source=validated_data.get('source'),
        ))
        model = serializer.save(student=request.user, status=Submit.DEFAULT_STATUS)
        cats.submit = model
        cats.save()

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
