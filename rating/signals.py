from django.db.models.signals import post_save
from django.dispatch import receiver
from lesson.models import Lesson
from problem.models import Submit, Problem
from rating.models import CourseProgress, LessonProgress
from users.models import CourseGroupAssignStudent


@receiver(post_save, sender=Submit)
def update_lesson_progress(sender, instance, **kwargs):
    """
    Обновляет LessonProgress при отправке задачи на проверку.
    """
    status = instance.status
    user = instance.student
    problem = instance.problem
    lesson = problem.lesson

    # Получаем или создаем LessonProgress
    lesson_progress, created = LessonProgress.objects.get_or_create(
        user=user,
        lesson=lesson,
        defaults={'solved': {'CW': {}, 'HW': {}, 'EX': {}}}
    )

    # Обновляем поле solved
    if not lesson_progress.solved:
        lesson_progress.solved = {'CW': {}, 'HW': {}, 'EX': {}}

    lesson_progress.solved[problem.type][str(problem.id)] = (status, instance.id)
    lesson_progress.save()

    # Обновляем прогресс курса
    calc_lesson_stat(lesson, lesson_progress.solved, user)


def calc_lesson_stat(lesson, solved: dict, user):
    """
    Вычисляет статистику урока и обновляет CourseProgress.
    """
    def calc(problem_type: str) -> int:
        problems_amount = Problem.objects.filter(lesson_id=lesson.id, type=problem_type).count()
        problems_ok = len([v for v in solved[problem_type].values() if v[0] == 'OK'])
        try:
            return (lesson.scores[problem_type] / problems_amount) * problems_ok
        except ArithmeticError:
            return 0

    count_of_cw = calc('CW')
    count_of_hw = calc('HW')
    count_of_ex = calc('EX')

    for course_progress in CourseProgress.objects.filter(course=lesson.course, user=user):
        if course_progress.progress is None:
            course_progress.progress = {}

        course_progress.progress[lesson.id] = {"CW": count_of_cw, "HW": count_of_hw, "EX": count_of_ex}
        course_progress.save()


@receiver(post_save, sender=CourseGroupAssignStudent)
def add_student_to_rating_of_lesson(sender, instance, created, **kwargs):
    """
    Создает LessonProgress для каждого урока курса, когда студент добавляется в группу.
    """
    if not created:
        return

    for lesson in Lesson.objects.filter(course=instance.group.course):
        LessonProgress.objects.create(
            user=instance.user,
            lesson=lesson,
            solved={'CW': {}, 'HW': {}, 'EX': {}},
            attendance=False
        )


@receiver(post_save, sender=CourseGroupAssignStudent)
def add_student_to_rating_course(sender, instance, created, **kwargs):
    """
    Создает CourseProgress для студента, когда он добавляется в группу курса.
    """
    if not created:
        return

    # Инициализируем прогресс для всех уроков курса
    exist_lessons = {}
    for lesson in Lesson.objects.filter(course=instance.group.course):
        exist_lessons[lesson.id] = {'CW': 0, 'HW': 0, 'EX': 0}

    # Создаем запись CourseProgress
    CourseProgress.objects.create(
        course=instance.group.course,
        user=instance.user,
        progress=exist_lessons
    )


@receiver(post_save, sender=Lesson)
def add_lessons_to_course_rating(sender, instance, created, **kwargs):
    """
    Добавляет новый урок в прогресс всех студентов курса.
    """
    if not created or not instance.course:
        return

    # Обновляем CourseProgress для всех студентов курса
    for course_progress in CourseProgress.objects.filter(course=instance.course):
        if course_progress.progress is None:
            course_progress.progress = {}

        # Добавляем новый урок в прогресс
        course_progress.progress[instance.id] = {'CW': 0, 'HW': 0, 'EX': 0}
        course_progress.save()

    # Создаем LessonProgress для всех студентов курса
    for student in instance.course.students.all():
        LessonProgress.objects.create(
            user=student,
            lesson=instance,
            solved={'CW': {}, 'HW': {}, 'EX': {}},
            attendance=False
        )
