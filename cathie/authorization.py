import json
import os

import requests
from django.conf import settings

from cathie.exceptions import CatsAnswerCodeException, CatsAuthorizationException


def cats_sid():
    return os.getenv('cats_sid', '-1')


def cats_sid_setter(value):
    os.environ["cats_sid"] = value


def check_authorization_for_cats(function_to_decorate):
    def wrapper(*args, **kwargs):
        print('checking auth!', end=' ')
        r = None
        if cats_sid() != '-1':
            url = f'{settings.CATS_URL}?f=profile;sid={cats_sid()};json=1'
            r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            if r.status_code != 200:
                raise CatsAnswerCodeException(r)
        if not r or 'error' in json.loads(r.content.decode('utf-8')):
            print('authorizing...', end=' ')
            payload = {'login': 'mesenev', 'passwd': 'Pasha123lol'}
            auth = requests.get(
                url=f'{settings.CATS_URL}?f=login;json=1;',
                params=payload,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            if auth.status_code != 200:
                raise CatsAnswerCodeException(r)
            content = auth.json()
            if content['status'] == 'error':
                raise CatsAuthorizationException(content)
            print('new sid', content['sid'])
            cats_sid_setter(content['sid'])
        print('auth check passed.')
        return function_to_decorate(*args, **kwargs)

    return wrapper
