import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'imcslms.settings')

import django

django.setup()
from django.contrib.auth.models import Group

GROUPS = ['teacher', 'student', 'anonymous']
MODELS = ['user']


def main():
    for group in GROUPS:
        new_group, created = Group.objects.get_or_create(name=group)


if __name__ == '__main__':
    main()
