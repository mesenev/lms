from django.contrib.auth.decorators import login_required
from django_filters.rest_framework import DjangoFilterBackend
from requests.utils import default_headers
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from cathie import cats_api
from cathie.cats_api import cats_get_problems_from_contest, cats_get_problem_description_by_url, get_contests_from_cats
from cathie.models import CatsAccount
from cathie.serializers import CatsAccountSerializer
from course.models import Course
from problem.models import Problem

from django.shortcuts import render
from cathie.authorization import *
from users.permissions import CourseStaffOrAuthor
from django.utils import timezone


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


@login_required
@api_view(['GET'])
def get_cats_contests(request):
    contests = get_contests_from_cats()
    return Response(contests)


@login_required
@api_view(['POST'])
def add_users_to_contest(request):
    contest_id = request.data['contest_id']
    logins_to_add = request.data['logins_to_add']
    return Response(status=cats_api.add_users_to_contest(logins_to_add, contest_id))


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
    filterset_fields = ('user', 'username', 'last_check')

    def create(self, request, *args, **kwargs):
        auth = requests.post(
            f'{settings.CATS_URL}?f=login;json=1',
            {'login': request.data['login'], 'passwd': request.data['passwd']},
            headers=default_headers()
        )
        if auth.status_code != 200:
            raise CatsAuthorizationException()

        cats_account, is_created = CatsAccount.objects.get_or_create(user=request.user)
        _status = status.HTTP_201_CREATED if is_created else status.HTTP_202_ACCEPTED
        cats_account.username = request.data['login']
        cats_account.last_check = timezone.now()
        cats_account.save()
        serializer = self.get_serializer(cats_account)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=_status, headers=headers)
