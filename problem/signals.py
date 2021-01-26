from django.db.models.signals import post_save
from django.dispatch import receiver
from problem.models import Submit
from lesson.models import LessonProgress


@receiver(post_save, sender=Submit)
def update_lesson_progress(sender, instance, **kwargs):
    user = instance.student
    lesson_id = instance.problem.lesson
    problem_id = instance.problem.id
    if instance.problem.lesson.progress.filter(user=user).first():
        progress = instance.problem.lesson.progress.get(user=user)
        status = instance.status
        solved = add_to_solved(str(progress.solved), status, str(problem_id))
        LessonProgress.objects.update(**{'solved': solved})
    else:
        validated_data = {'user': user, 'lesson': lesson_id, 'solved': problem_id}
        LessonProgress.objects.create(**validated_data)


def add_to_solved(solved, status, problem):
    if status == 'OK':
        return solved + problem + ','
    else:
        return solved.replace((str(problem) + ','), '')
