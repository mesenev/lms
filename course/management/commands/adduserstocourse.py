import random

from django.core.management import BaseCommand, CommandError

from course.models import Course
from users.models import User, CourseAssignStudent

NAMES = [
    "Витя", "Петя", "Олег", "Света", "Маша", "Жора", "Артём", "Паша", "Андрей", "Тарас", "Таня", "Дима", "Боря", "Вова"
]


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('course_id', help='id курса', type=int)
        parser.add_argument('count_of_users', help='количество пользователей', type=int)

    def handle(self, *args, **options):
        course_id = options['course_id']
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            raise CommandError(f'Курса с id {course_id} не существует')

        count_of_users = options['count_of_users']
        count_of_exists_users = User.objects.count()

        for i in range(1, count_of_users + 1):
            user = User.objects.create_user(
                username=f'{count_of_exists_users + i}user',
                first_name=random.choice(NAMES),
                last_name=str(random.randint(1000000, 9999999))
            )
            user.set_password('1234')
            user.save()
            CourseAssignStudent.objects.create(course=course, user=user, )
            self.stdout.write(self.style.SUCCESS(f'login: {user.username}, password: 1234'))
            # course_assign.save()
        self.stdout.write(self.style.SUCCESS(f'На курс {course.name} добавлено {count_of_users}'))

    help = 'Регистрация пользователей на курс'
