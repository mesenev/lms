import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from requests.utils import default_headers
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from cathie import cats_api
from cathie.authorization import cats_sid_setter, cats_sid
from cathie.cats_api import cats_get_problems_from_contest, cats_get_problem_description_by_url
from cathie.cats_api import get_contests_from_cats
from cathie.exceptions import CatsAuthorizationException
from cathie.models import CatsAccount
from cathie.serializers import CatsAccountSerializer
from course.models import Course
from problem.models import Problem
from users.permissions import CourseStaffOrAuthor, CourseStaffOrReadOnlyForStudents


class ListCatsProblems(APIView):
    permission_classes = [CourseStaffOrAuthor]

    def get(self, request, course_id):
        """Return list of problems from cats if cats_id specified"""
        course = Course.objects.get(pk=course_id)
        cats_problems = cats_get_problems_from_contest(course.cats_id)
        return Response(cats_problems)


class ProblemDescription(APIView):
    permission_classes = [CourseStaffOrAuthor]

    def get(self, request, problem_id):
        problem = Problem.objects.get(pk=problem_id)
        problem_description = cats_get_problem_description_by_url(problem.cats_material_url)
        problem.description = problem_description
        problem.save()
        return Response(problem_description)


@api_view(['GET', 'POST'])
@login_required
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


class CatsContest(APIView):
    permission_classes = [CourseStaffOrReadOnlyForStudents]

    def get(self, request):
        """Return list of CatsContents from cats"""
        return Response(get_contests_from_cats())

    def post(self, request):
        """Register user to the contest by [user id] and [logins to add]"""
        contest_id = request.data['contest_id']
        logins_to_add = request.data['logins_to_add']
        return Response(status=cats_api.add_users_to_contest(logins_to_add, contest_id))
