import json

import requests
from django.conf import settings

from cathie.exceptions import CatsAnswerCodeException
from cathie.serializers import CatsProblemSerializer


def cats_check_status():
    pass


def cats_submit_solution():
    pass


def cats_submit_problem():
    pass


def cats_check_solution_status():
    pass


def cats_get_problems_from_contest(contest_id, cats_user_id):
    url = f'{settings.CATS_URL}?f=problems;json=1;cid={contest_id};sid={cats_user_id}'
    answer = requests.get(url)
    if answer.status_code != 200:
        raise CatsAnswerCodeException(answer.reason)
    data = json.loads(answer.content.decode('utf-8'))
    course_problems = CatsProblemSerializer(data=data, many=True)
    return course_problems



