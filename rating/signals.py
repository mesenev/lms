from django.db.models.signals import post_save
from django.dispatch import receiver

from lesson.models import Lesson
from problem.models import Submit, Problem
from rating.models import CourseProgress, LessonProgress, Attendance
from users.models import CourseAssignStudent


@receiver(post_save, sender=Submit)
def update_lesson_progress(sender, instance, **kwargs):
    status = instance.status
    user = instance.student.id
    problem_id = instance.problem.id
    lesson = Problem.objects.get(id=problem_id).lesson
    progress = None
    try:
        progress = LessonProgress.objects.get(user=user, lesson=lesson.id)
    except LessonProgress.DoesNotExist:
        pass
    if progress:
        progress.solved[instance.problem.type][str(problem_id)] = (status, instance.id)
        LessonProgress.objects.filter(
            user=user, lesson=Problem.objects.get(id=problem_id).lesson.id
        ).update(**{'solved': progress.solved})
        calc_lesson_stat(lesson, progress.solved, user)


post_save.connect(update_lesson_progress, sender=Submit)


def calc_lesson_stat(lesson, solved: dict, user):
    def calc(typeProblem: str) -> int:
        try:
            return (lesson.scores[typeProblem] / Problem.objects.filter(lesson_id=lesson.id, type=typeProblem).count()) \
                   * len(dict((k, v) for (k, v) in solved[typeProblem].items() if v[0] == 'OK'))
        except ArithmeticError:
            return 0

    count_of_CW = calc('CW')
    count_of_HW = calc('HW')
    count_of_EX = calc('EX')

    for i in CourseProgress.objects.filter(course=lesson.course, user=user):
        i.lessons[lesson.id] = {"CW": count_of_CW, "HW": count_of_HW, "EX": count_of_EX}
        i.save()


@receiver(post_save, sender=CourseAssignStudent)
def add_student_to_rating_of_lesson(sender, instance, created, **kwargs):
    if not created:
        return
    user = instance.user
    course = instance.course
    for i in Lesson.objects.filter(course=course):
        validated_data = {'course': course, 'lesson': i, 'user': user}
        at = Attendance.objects.create(**validated_data)
        validated_data = {'user': user, 'lesson': i, 'solved': {'CW': {}, 'HW': {}, 'EX': {}}, 'attendance': at}
        LessonProgress.objects.create(**validated_data)


post_save.connect(add_student_to_rating_of_lesson, sender=CourseAssignStudent)


@receiver(post_save, sender=Lesson)
def add_student_to_rating_lesson(sender, instance, created, **kwargs):
    if not created or instance.course is None:
        return
    for i in CourseAssignStudent.objects.filter(course=instance.course.id):
        validated_data = {'course': i.course, 'lesson': instance, 'user': i.user}
        at = Attendance.objects.create(**validated_data)
        validated_data = {'user': i.user, 'lesson': instance, 'solved': {'CW': {}, 'HW': {}, 'EX': {}},
                          'attendance': at}
        LessonProgress.objects.create(**validated_data)
        CourseProgress.objects.filter(user=i.user, course=i.course).update(
            **{'lessons': {'CW': 0, 'HW': 0, 'EX': 0}})


@receiver(post_save, sender=CourseAssignStudent)
def add_student_to_rating_course(sender, instance, created, **kwargs):
    if not created:
        return
    existLessons, attendance, at = {}, {}, None
    for i in Lesson.objects.filter(course=instance.course):
        existLessons[i.id] = {'CW': 0, 'HW': 0, 'EX': 0}
        validated_data = {'course': instance.course, 'user': instance.user, 'lesson': i}
        at = Attendance.objects.create(**validated_data)

    validated_data = {'course': instance.course, 'user': instance.user, 'progress': existLessons, 'attendance': at}
    CourseProgress.objects.create(**validated_data)


@receiver(post_save, sender=Lesson)
def add_lessons_to_course_rating(sender, instance, created, **kwargs):
    if not created and not instance.course:
        return
    for i in CourseProgress.objects.filter(course=instance.course):
        i.lessons[instance.id] = {'CW': 0, 'HW': 0, 'EX': 0}
        i.save()
