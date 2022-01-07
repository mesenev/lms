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
        url = f'{settings.CATS_URL}?f=profile;sid={cats_sid()};json=1'
        r = requests.get(url)
        if r.status_code != 200:
            raise CatsAnswerCodeException(r)
        if 'error' in json.loads(r.content.decode('utf-8')):
            print('authorizing...', end=' ')
            auth = requests.post(
                f'{settings.CATS_URL}?f=login;json=1',
                {'login': settings.CATS_LOGIN, 'passwd': settings.CATS_PASSWD}
            )
            if auth.status_code != 200:
                raise CatsAnswerCodeException(r)
            try:
                content = json.loads(auth.content.decode('utf-8'))
            except:
                raise CatsAuthorizationException('Invalid json from cats')
            print('new sid', content['sid'])
            cats_sid_setter(content['sid'])
        print('auth check passed.')
        return function_to_decorate(*args, **kwargs)

    return wrapper
