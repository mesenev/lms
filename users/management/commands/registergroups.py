from django.contrib.auth.models import Group
from django.core.management import BaseCommand

TEACHER = 'teacher'
STUDENT = 'student'
ANONYMOUS = 'anonymous'


class Command(BaseCommand):
    help = 'Creating necessary groups for an lms'

    def handle(self, *args, **options):
        GROUPS = [TEACHER, STUDENT, ANONYMOUS]

        for group in GROUPS:
            new_group, created = Group.objects.get_or_create(name=group)
            if 'verbosity' not in options and options['verbosity'] != 0:
                self.stdout.write(self.style.SUCCESS(f'Group {new_group.name} exists now'))
