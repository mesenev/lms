import json

import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from cathie import authorization
from cathie.cats_api import cats_get_problems_from_contest, cats_get_problem_description_by_url
from cathie.exceptions import CatsAnswerCodeException, CatsAuthorizationException
from course.models import Course
from problem.models import Problem

from django.shortcuts import render
from cathie.authorization import *


def check_authorization_for_cats(function_to_decorate):
    def wrapper(*args, **kwargs):
        url = f'{settings.CATS_URL}?sid={authorization.cats_sid()};json=1'
        r = requests.get(url)
        if r.status_code != 200:
            raise CatsAnswerCodeException(r.reason)
        if 'error' in json.loads(r.content.decode('utf-8')):
            auth = requests.post(
                f'{settings.CATS_URL}?f=login;json=1',
                {'login': settings.CATS_LOGIN, 'passwd': settings.CATS_PASSWD}
            )
            if auth.status_code != 200:
                raise CatsAnswerCodeException(r.reason)
            try:
                content = json.loads(auth.content.decode('utf-8'))
            except:
                raise CatsAuthorizationException('Invalid json from cats')
            authorization.cats_sid_setter(content['sid'])
        return function_to_decorate(*args, **kwargs)

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
@check_authorization_for_cats
def cats_admin(request):
    if request.method == 'POST':
        new_cats_seed = request.POST["input_cats_seed"]
        cats_sid_setter(new_cats_seed)

    data = {"cats_seed": cats_sid()}
    return render(request, 'cats_admin_page.html', context=data)
