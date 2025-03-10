from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from lesson.models import Lesson
from problem.models import Submit, Problem
from rating.models import CourseProgress, LessonProgress
from users.models import CourseGroupAssignStudent


#Прогресс для нового урока
@receiver(post_save, sender=Lesson)
def add_student_to_rating_lesson(sender, instance, created, **kwargs):
    """
    Создаёт LessonProgress для всех студентов курса при создании нового урока.
    Также добавляет урок в CourseProgress для всех студентов.
    """
    if not created or instance.course is None:
        return

    # Создаём LessonProgress для каждого студента курса
    for assignment in CourseGroupAssignStudent.objects.filter(group__course=instance.course):
        LessonProgress.objects.get_or_create(
            user=assignment.user,
            lesson=instance,
            defaults={'solved': {'CW': {}, 'HW': {}, 'EX': {}}}
        )

    # Добавляем урок в CourseProgress для каждого студента курса
    for progress in CourseProgress.objects.filter(course=instance.course):
        if progress.progress is None:
            progress.progress = {}

        if str(instance.id) not in progress.progress:
            progress.progress[str(instance.id)] = {'CW': 0, 'HW': 0, 'EX': 0}
            progress.save()

#Обновление прогресса урока при сабмите
@receiver(post_save, sender=Submit)
def update_lesson_progress(sender, instance, **kwargs):
    """
    Обновляет LessonProgress при создании или изменении сабмита.
    Также пересчитывает баллы в CourseProgress.
    """
    status = instance.status
    user = instance.student
    problem = instance.problem
    lesson = problem.lesson

    # Создаём или получаем LessonProgress
    progress, created = LessonProgress.objects.get_or_create(
        user=user,
        lesson=lesson,
        defaults={'solved': {'CW': {}, 'HW': {}, 'EX': {}}}
    )

    # Получаем текущий статус задачи (если есть)
    problem_type = problem.type
    current_status = progress.solved[problem_type].get(str(problem.id), (None, None))[0]

    # Обновляем только если:
    # 1. Задача еще не была решена
    # 2. Или текущий статус не OK (сохраняем лучший результат)
    if current_status != 'OK':
        progress.solved[problem_type][str(problem.id)] = (status, instance.id)
        progress.save()

    # Всегда пересчитываем статистику, даже если статус не изменился
    # (на случай изменения весов задач или структуры курса)
    calc_lesson_stat(lesson, progress.solved, user)


def calc_lesson_stat(lesson, solved: dict, user):
    """
    Пересчитывает баллы для урока и обновляет CourseProgress.
    """
    def calc(problem_type: str) -> int:
        problems_amount = Problem.objects.filter(lesson_id=lesson.id, type=problem_type).count()
        problems_ok = len(dict((k, v) for (k, v) in solved[problem_type].items() if v[0] == 'OK'))
        try:
            return (lesson.scores[problem_type] / problems_amount) * problems_ok
        except ArithmeticError:
            return 0

    count_of_cw = calc('CW')
    count_of_hw = calc('HW')
    count_of_ex = calc('EX')

    # Обновляем CourseProgress
    for i in CourseProgress.objects.filter(course=lesson.course, user=user):
        if i.progress is None:
            i.progress = {}
        
        i.progress[str(lesson.id)] = {"CW": count_of_cw, "HW": count_of_hw, "EX": count_of_ex}
        i.save()


#Создание прогресса для нового студента
@receiver(post_save, sender=CourseGroupAssignStudent)
def add_student_to_rating_of_lesson(sender, instance, created, **kwargs):
    """
    Создаёт LessonProgress и CourseProgress для нового студента.
    """
    if not created:
        return

    # Создаём LessonProgress для каждого урока курса
    for lesson in Lesson.objects.filter(course=instance.group.course):
        LessonProgress.objects.get_or_create(
            user=instance.user,
            lesson=lesson,
            defaults={'solved': {'CW': {}, 'HW': {}, 'EX': {}}}
        )

    # Создаём CourseProgress
    exist_lessons = {}
    for lesson in Lesson.objects.filter(course=instance.group.course):
        exist_lessons[str(lesson.id)] = {'CW': 0, 'HW': 0, 'EX': 0}

    CourseProgress.objects.get_or_create(
        course=instance.group.course,
        user=instance.user,
        defaults={'progress': exist_lessons}
    )

#Удаление урока
@receiver(post_delete, sender=Lesson)
def delete_lesson_progress(sender, instance, **kwargs):
    """
    Удаляет LessonProgress и обновляет CourseProgress при удалении урока.
    """
    # Удаляем LessonProgress для этого урока
    LessonProgress.objects.filter(lesson=instance).delete()

    # Удаляем урок из CourseProgress
    for progress in CourseProgress.objects.filter(course=instance.course):
        if progress.progress is not None and str(instance.id) in progress.progress:
            del progress.progress[str(instance.id)]
            progress.save()

#Удаление задачи
@receiver(post_delete, sender=Problem)
def delete_problem_from_progress(sender, instance, **kwargs):
    """
    Удаляет задачу из поля solved в LessonProgress.
    """
    lesson = instance.lesson
    problem_type = instance.type
    problem_id = str(instance.id)

    # Удаляем задачу из всех LessonProgress
    for progress in LessonProgress.objects.filter(lesson=lesson):
        if problem_id in progress.solved.get(problem_type, {}):
            del progress.solved[problem_type][problem_id]
            progress.save()

#Удаление студента из курса
@receiver(post_delete, sender=CourseGroupAssignStudent)
def delete_student_progress(sender, instance, **kwargs):
    """
    Удаляет LessonProgress и CourseProgress при удалении студента из курса.
    """
    # Удаляем LessonProgress для этого студента
    LessonProgress.objects.filter(user=instance.user, lesson__course=instance.group.course).delete()

    # Удаляем CourseProgress для этого студента
    CourseProgress.objects.filter(course=instance.group.course, user=instance.user).delete()

#Пересчет прогресса при изменении структуры курса
def recalculate_course_progress(course):
    """
    Пересчитывает прогресс для всех студентов курса.
    """
    for progress in CourseProgress.objects.filter(course=course):
        for lesson in Lesson.objects.filter(course=course):
            lesson_progress = LessonProgress.objects.filter(user=progress.user, lesson=lesson).first()
            if lesson_progress:
                calc_lesson_stat(lesson, lesson_progress.solved, progress.user)

#При изменении scores
@receiver(post_save, sender=Lesson)
def update_scores_in_progress(sender, instance, **kwargs):
    """
    Пересчитывает прогресс для всех студентов при изменении баллов за задачи.
    """
    if instance.course:
        recalculate_course_progress(instance.course)
