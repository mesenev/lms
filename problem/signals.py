from django.db.models.signals import post_save
from django.dispatch import receiver
from problem.models import Submit
from lesson.models import LessonProgress
from users.models import CourseAssignStudent


@receiver(post_save, sender=Submit)
def update_lesson_progress(sender, instance, **kwargs):
    status = instance.status
    user = instance.student
    lesson_id = instance.problem.lesson
    problem_id = instance.problem.id
    progress = instance.problem.lesson.progress.filter(user=user).first()
    if status != 'OK':
        st = progress.solved.replace((str(problem_id) + ','), '')
        create_or_update(user, lesson_id, problem_id, st, progress)
    else:
        st = progress.solved + problem_id + ','
        create_or_update(user, lesson_id, problem_id, st, progress)


def create_or_update(user, lesson, problem, result, progress):
    if progress:
        LessonProgress.objects.update(**{'solved': result})
    else:
        validated_data = {'user': user, 'lesson': lesson, 'solved': problem}
        LessonProgress.objects.create(**validated_data)

