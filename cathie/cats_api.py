import json
import re

import requests
from django.conf import settings

from cathie.exceptions import CatsAnswerCodeException


def cats_check_status():
    pass


def cats_submit_solution(source_text: str, problem_id: int, de_id: int, source=None):
    # ToDo обработать повторную отправку решения
    url = f'{settings.CATS_URL}main.pl?f=api_submit_problem;'
    if settings.CATS_SID:  # and settings.CATS_TOKEN:
        url += f'sid={settings.CATS_SID}'
    data = {
        'source': source,
        'de_id': de_id,
        'source_text': source_text,
        'problem_id': problem_id
    }
    r = requests.post(url, data=data)
    if r.status_code != 200:
        raise CatsAnswerCodeException(r.reason)
    r_content = json.loads(r.content.decode('utf-8'))
    req_ids = None
    if r_content.get('href_run_details'):
        req_ids = re.search(r'(?<=rid=)\d+', r_content['href_run_details']).group()
        if req_ids.isdigit():
            req_ids = int(req_ids)
    return req_ids


def cats_submit_problem():
    pass


def cats_check_solution_status(req_ids: int) -> str:
    url = f'{settings.CATS_URL}main.pl?f=api_get_request_state;req_ids={req_ids};'
    if settings.CATS_SID:  # and settings.CATS_TOKEN:
        url += f'sid={settings.CATS_SID}'
    r = requests.get(url)
    if r.status_code != 200:
        raise CatsAnswerCodeException(r.reason)
    data = json.loads(r.content.decode('utf-8'))
    return data[0]['verdict']


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
