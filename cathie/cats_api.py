import json
import re

import requests
from django.conf import settings
from rest_framework import status

from cathie.exceptions import CatsAnswerCodeException, CatsNormalErrorException
from cathie import authorization

ARCHIVE_CONTEST_ID = 500001  # magic constant for `Archive` contest
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/89.0.4356.6 Safari/537.36'
}

def cats_check_status():
    pass


@authorization.check_authorization_for_cats
def cats_submit_solution(
        source_text: str, contest_id: int, problem_id: int,
        de_id: int, cats_account: str
):
    # ToDo обработать повторную отправку решения
    url = f'{settings.CATS_URL}?f=api_submit_problem;'
    data = {
        'de_id': de_id,
        'source_text': source_text,
        'problem_id': problem_id,
        'submit_as': cats_account,
        'cid': contest_id,
        'json': 1,
        'lang': 'en',
        'sid': authorization.cats_sid(),
    }
    r = requests.post(url, data=data, headers=headers)
    if r.status_code != 200:
        raise CatsAnswerCodeException(r)
    r_content = r.json()
    if r_content['status'] == 'error':
        raise CatsNormalErrorException(r)
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
    url = f'{settings.CATS_URL}problems?'
    data = {
        'json': 1,
        'cid': contest_id,
        'lang': 'en',
        'sid': authorization.cats_sid(),
        'page': 0,
    }
    problems = list()
    cats_answer = requests.get(url, params=data, headers=headers)
    if cats_answer.status_code != 200:
        raise CatsAnswerCodeException(cats_answer)
    cats_problems = cats_answer.json()['problems']
    problems.extend(cats_problems)
    while len(cats_problems) == 20:
        data['page'] += 1
        cats_answer = requests.get(url, params=data, headers=headers)
        if cats_answer.status_code != 200:
            raise CatsAnswerCodeException(cats_answer)
        cats_problems = cats_answer.json()['problems']
        problems.extend(cats_problems)

    return problems


def cats_get_problem_description_by_url(description_url):
    url = f'{settings.CATS_URL}{description_url.lstrip("./")}'
    # todo: remove it and use default headers instead

    request = requests.request(method='get', url=url, headers=headers)
    if request.status_code != 200:
        raise CatsAnswerCodeException(request)
    data = request.content.decode('utf-8')
    return data


@authorization.check_authorization_for_cats
def get_contests_from_cats(cats_id: int):
    url = f'{settings.CATS_URL}contests?'
    data = {
        'json': 1,
        'search': f'has_user({cats_id})',
        'lang': 'en',
        'sid': authorization.cats_sid(),
        'page': 0,
        'filter': 'my'
    }
    get_my_contests = requests.get(url, params=data, headers=headers)
    if get_my_contests.status_code != status.HTTP_200_OK:
        raise CatsAnswerCodeException(get_my_contests)
    return list(filter(
        lambda x: x['id'] != ARCHIVE_CONTEST_ID,
        get_my_contests.json()['contests']
    ))


@authorization.check_authorization_for_cats
def add_users_to_contest(students: list, contest_id: int):
    params = {
        'logins_to_add': ','.join(students),
        'by_login': 1,
        'json': 1,
        'sid': authorization.cats_sid(),
        'cid': contest_id,
    }
    url = f'{settings.CATS_URL}users_add_participants?'
    answer = requests.post(url, params=params, headers=headers)
    if answer.status_code != 200:
        print(answer.json())
        raise CatsAnswerCodeException(answer)
    return answer.status_code


# def cats_get_problem_by_id(cats_id, user):
#     pass


def cats_user_login(username: str, password: str):
    auth = requests.post(
        f'{settings.CATS_URL}?f=login;json=1',
        {'login': username, 'passwd': password},
        headers=headers
    )
    if auth.status_code != 200:
        raise CatsAnswerCodeException(auth)
    return auth.json()


def get_user_id(sid: str):
    answer = requests.get(
        f'{settings.CATS_URL}profile?',
        params={'sid': sid, 'json': 1},
        headers=headers
    )
    if answer.status_code != 200:
        raise CatsAnswerCodeException(answer)
    return answer.json()['id']
