from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from cathie.cats_api import cats_get_problems_from_contest, cats_get_problem_description_by_url
from course.models import Course
from problem.models import Problem

from django.shortcuts import render
from cathie.authorization import *


@login_required
@api_view(['GET'])
@renderer_classes([JSONRenderer])
def get_cats_problems(request, course_id):
    course = Course.objects.get(pk=course_id)
    cats_problems = cats_get_problems_from_contest(course.cats_id, request.user)
    return Response(cats_problems)


@login_required
@api_view(['GET'])
def get_cats_problem_description(request, problem_id):
    problem = Problem.objects.get(pk=problem_id)
    problem_description = cats_get_problem_description_by_url(problem.cats_material_url)
    problem.description = problem_description
    problem.save()
    return Response(problem_description)


@login_required
@api_view(['GET', 'POST'])
def show_custom_admin_page(request):
    if request.method == 'POST':
        new_cats_seed = request.POST["input_cats_seed"]
        cats_sid_setter(new_cats_seed)

    data = {"cats_seed": cats_sid()}
    return render(request, 'custom_page.html', context=data )

