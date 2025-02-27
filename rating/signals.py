from django.db.models.signals import post_save
from django.dispatch import receiver

from lesson.models import Lesson
from problem.models import Submit, Problem
from rating.models import CourseProgress, LessonProgress
from users.models import CourseGroupAssignStudent


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
    if not progress:
        return
    progress.solved[instance.problem.type][str(problem_id)] = (status, instance.id)
    LessonProgress.objects.filter(
        user=user, lesson=Problem.objects.get(id=problem_id).lesson.id
    ).update(**{'solved': progress.solved})
    calc_lesson_stat(lesson, progress.solved, user)


post_save.connect(update_lesson_progress, sender=Submit)


def calc_lesson_stat(lesson, solved: dict, user):
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

    for i in CourseProgress.objects.filter(course=lesson.course, user=user):
        i.progress[lesson.id] = {"CW": count_of_cw, "HW": count_of_hw, "EX": count_of_ex}
        i.save()


# @receiver(post_save, sender=GroupAssignStudent)
# def add_student_to_rating_of_lesson(sender, instance, created, **kwargs):
#     if not created:
#         return
#     for lesson in Lesson.objects.filter(course=instance.course):
#         validated_data = {
#             'user': instance.user, 'lesson': lesson, 'solved': {'CW': {}, 'HW': {}, 'EX': {}}, 'attendance': False
#         }
#         LessonProgress.objects.create(**validated_data)


#post_save.connect(add_student_to_rating_of_lesson, sender=GroupAssignStudent)


# @receiver(post_save, sender=GroupAssignStudent)
# def add_student_to_rating_course(sender, instance, created, **kwargs):
#     if not created:
#         return
#     exist_lessons, attendance, at = {}, {}, None
#     for i in Lesson.objects.filter(course=instance.course):
#         exist_lessons[i.id] = {'CW': 0, 'HW': 0, 'EX': 0}
#     validated_data = {'course': instance.course, 'user': instance.user, 'progress': exist_lessons}
#     course_progress = CourseProgress.objects.create(**validated_data)


#post_save.connect(add_student_to_rating_course, sender=GroupAssignStudent)


@receiver(post_save, sender=Lesson)
def add_student_to_rating_lesson(sender, instance, created, **kwargs):
    if not created or instance.course is None:
        return
    for i in CourseGroupAssignStudent.objects.filter(group__course=instance.course):
        LessonProgress.objects.create(
            user=i.user, lesson=instance, solved={'CW': {}, 'HW': {}, 'EX': {}}, attendance=False
        )


@receiver(post_save, sender=Lesson)
def add_lessons_to_course_rating(sender, instance, created, **kwargs):
    if not created and not instance.course:
        return

    for i in CourseProgress.objects.filter(course=instance.course):
        # Инициализируем progress, если он равен None
        if i.progress is None:
            i.progress = {}
        
        # Обновляем progress
        i.progress.update({instance.id: {'CW': 0, 'HW': 0, 'EX': 0}})
        i.save()


'''@receiver(post_save, sender=Attendance)
def update_attendance(sender, instance, updated, **kwargs):
    if not updated and not instance.course:
        return
    for i in CourseProgress.objects.filter(course=instance.course):
        i.progress[instance.id] = {'CW': 0, 'HW': 0, 'EX': 0}
        #print(Attendance.objects.filter(user=instance.user, course=instance.course))
        i.attendance.add(*(Attendance.objects.filter(user=instance.user, course=instance.course)))
        print(i.attendance)
        i.save()'''
