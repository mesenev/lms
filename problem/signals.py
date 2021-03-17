from django.db.models.signals import post_save
from django.dispatch import receiver

from course.models import CourseProgress
from lesson.models import Lesson
from lesson.models import LessonProgress
from problem.models import Submit, Problem
from users.models import CourseAssignStudent


@receiver(post_save, sender=Submit)
def update_lesson_progress(sender, instance, **kwargs):
    status = instance.status
    user = instance.student.id
    problem_id = instance.problem.id
    progress = LessonProgress.objects.get(user=user, lesson=Problem.objects.get(id=problem_id).lesson.id)
    if progress:
        progress.solved[problem_id] = (status, instance.id)
        LessonProgress.objects.filter(user=user, lesson=Problem.objects.get(id=problem_id).lesson.id).update(
            **{'solved': progress.solved})


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
    if not created or instance.course is None:
        return
    for i in CourseAssignStudent.objects.filter(course=instance.course.id):
        validated_data = {'user': i.user, 'lesson': instance, 'solved': {}}
        LessonProgress.objects.create(**validated_data)


@receiver(post_save, sender=CourseAssignStudent)
def add_student_to_rating(sender, instance, created, **kwargs):
    if not created:
        return
    validated_data = {'course': instance.course, 'user': instance.user, 'lessons': {}, 'attendance': {}}
    CourseProgress.objects.create(**validated_data)


@receiver(post_save, sender=Lesson)
def add_lessons_to_course_rating(sender, instance, created, **kwargs):
    if not created and not instance.course:
        return
    for i in CourseProgress.objects.filter(course=instance.course):
        i.lessons[instance.id] = {}
        i.attendance[instance.id] = False
        i.save()
