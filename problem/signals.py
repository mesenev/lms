from django.db.models.signals import post_save, post_init
from django.dispatch import receiver
from problem.models import Submit
from lesson.models import Lesson
from lesson.models import LessonProgress
from users.models import CourseAssignStudent


@receiver(post_save, sender=Submit)
def update_lesson_progress(sender, instance, **kwargs):
    status = instance.status
    user = instance.student
    lesson_id = instance.problem.lesson
    problem_id = instance.problem.id
    progress = instance.problem.lesson.progress.filter(user=user).first()
    if progress:
        pr = instance.problem.lesson.progress.get(user=user,lesson=lesson_id)
        pr.solved[problem_id] = status
        LessonProgress.objects.filter(user=user,lesson=lesson_id).update(**{'solved': pr.solved})


@receiver(post_save, sender=CourseAssignStudent)
def add_student_to_rating(sender, instance, created, **kwargs):
    if not created:
        return
    user = instance.user
    course = instance.course.id
    a = {}
    for i in Lesson.objects.filter(course=course):
        validated_data = {'user': user, 'lesson': i, 'solved': a}
        LessonProgress.objects.create(**validated_data)


@receiver(post_save, sender=Lesson)
def add_student_to_rating_(sender, instance, created, **kwargs):
    if not created:
        return
    a = {}
    for i in CourseAssignStudent.objects.filter(course=instance.course.id):
        validated_data = {'user': i.user, 'lesson': instance, 'solved': a}
        LessonProgress.objects.create(**validated_data)
