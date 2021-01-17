import json

import requests
from django.conf import settings

from cathie.exceptions import CatsAnswerCodeException


def cats_check_status():
    pass


def cats_submit_solution():
    pass


def cats_submit_problem():
    pass


def cats_check_solution_status():
    pass


def cats_get_problems_from_contest(contest_id, user):
    url = f'{settings.CATS_URL}?f=problems;json=1;cid={contest_id};'
    if settings.CATS_SID and settings.CATS_TOKEN:
        url += f'sid={settings.CATS_SID}'
    answer = requests.get(url)
    if answer.status_code != 200:
        raise CatsAnswerCodeException(answer.reason)
    data = json.loads(answer.content.decode('utf-8'))
    # course_problems = CatsProblemSerializer(data=data.problems, many=True)
    return data['problems']



