import json
import re

import requests
from django.conf import settings

from cathie.exceptions import CatsAnswerCodeException
from cathie import authorization


def cats_check_status():
    pass


@authorization.check_authorization_for_cats
def cats_submit_solution(source_text: str, problem_id: int, de_id: int, cats_account: str):
    # ToDo обработать повторную отправку решения
    url = f'{settings.CATS_URL}main.pl?f=api_submit_problem;json=1;'
    url += f'sid={authorization.cats_sid()}'
    data = {
        'de_id': de_id,
        'source_text': source_text,
        'problem_id': problem_id,
        'submit_as': cats_account,
    }
    r = requests.post(url, data=data)
    if r.status_code != 200:
        raise CatsAnswerCodeException(r)
    r_content = json.loads(r.content.decode('utf-8'))
    req_ids = None
    if r_content.get('href_run_details'):
        req_ids = re.search(r'(?<=rid=)\d+', r_content['href_run_details']).group()
        if req_ids.isdigit():
            req_ids = int(req_ids)
    return req_ids, r_content


def cats_submit_problem():
    pass


@authorization.check_authorization_for_cats
def cats_check_solution_status(req_ids: int):
    url = f'{settings.CATS_URL}main.pl?f=api_get_request_state;req_ids={req_ids};json=1;'
    url += f'sid={authorization.cats_sid()}'
    r = requests.get(url)
    if r.status_code != 200:
        raise CatsAnswerCodeException(r)
    data = r.json()
    if data:
        return data[0]['verdict'], data


@authorization.check_authorization_for_cats
def cats_get_problems_from_contest(contest_id):
    url = f'{settings.CATS_URL}?f=problems;json=1;cid={contest_id};'
    url += f'sid={authorization.cats_sid()}'
    answer = requests.get(url)
    if answer.status_code != 200:
        raise CatsAnswerCodeException(answer)
    data = json.loads(answer.content.decode('utf-8'))
    # course_problems = CatsProblemSerializer(data=data.problems, many=True)
    return data['problems']


def cats_get_problem_description_by_url(description_url):
    url = f'{settings.CATS_URL}{description_url.lstrip("./")}'
    # todo: remove it and use default headers instead
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/89.0.4356.6 Safari/537.36'
    }
    request = requests.request(method='get', url=url, headers=headers)
    if request.status_code != 200:
        raise CatsAnswerCodeException(request)
    data = request.content.decode('utf-8')
    return data

# def cats_get_problem_by_id(cats_id, user):
#     pass
