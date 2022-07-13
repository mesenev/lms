from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from cathie.authorization import *
from cathie.cats_api import cats_get_problems_from_contest, cats_get_problem_description_by_url
from cathie.models import CatsAccount
from cathie.serializers import CatsAccountSerializer
from course.models import Course
from problem.models import Problem

from django.shortcuts import render
from cathie.authorization import *
from users.permissions import CourseStaffOrAuthor


def check_authorization_for_cats(function_to_decorate):
    def wrapper():
        pass #геттер логина с кетса
        pass #геттер пароля с кетса
        # if login_from cats and password_from_cats:
        function_to_decorate()
        #else
        raise ValueError("Authorisation Error")
    return wrapper


@login_required
@api_view(['GET'])
@renderer_classes([JSONRenderer])
def get_cats_problems(request, course_id):
    course = Course.objects.get(pk=course_id)
    cats_problems = cats_get_problems_from_contest(course.cats_id)
    return Response(cats_problems)


@login_required
@api_view(['GET'])
def get_cats_problem_description(request, problem_id):
    problem = Problem.objects.get(pk=problem_id)
    problem_description = cats_get_problem_description_by_url(problem.cats_material_url)
    problem.description = problem_description
    problem.save()
    return Response(problem_description)


@api_view(['GET', 'POST'])
# @check_authorization_for_cats
def cats_admin(request):
    if request.method == 'POST':
        new_cats_seed = request.POST["input_cats_seed"]
        cats_sid_setter(new_cats_seed)

    data = {"cats_seed": cats_sid()}
    return render(request, 'cats_admin_page.html', context=data)



class CatsAccountViewSet(viewsets.ModelViewSet):
    permission_classes = [CourseStaffOrAuthor]
    queryset = CatsAccount.objects.all()
    serializer_class = CatsAccountSerializer
    filter_backends = (DjangoFilterBackend,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.initial_data['author'] = request.user.id
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

