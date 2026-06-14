from celery.utils.log import get_task_logger
from django.core.mail import send_mail
import re
from cathie.cats_api import cats_check_solution_status, cats_submit_solution
from cathie.exceptions import CatsAnswerCodeException, CatsNormalErrorException
from celery_app.celery_settings import app
from problem.models import Submit, CatsSubmit, LogEvent, Problem
from generate_study_materials.AiModel import AiModel
from lesson.models import Lesson, LessonContent
import json
from lesson.storages import gen_hash_name
from django.core.files.base import ContentFile
from users.models import User
from exam.models import ExaminationForm

logger = get_task_logger(__name__)

PROCESSED_STATUSES = [
    status for status, description in Submit.SUBMIT_STATUS
    if status not in ('NP', 'AW')
]


@app.task
def generate_exam_for_lesson(lessonId: int):

    lesson = Lesson.objects.filter(id=lessonId).first()
    aiModel = AiModel()

    exam = aiModel.generateExam(lessonName=lesson.name)
    clean_json = re.sub(r'^```json\s*|\s*```$', '', exam.text.strip())
    parsed_exam = json.loads(clean_json)
    questions = []

    i = 0

    for question in parsed_exam["questions"]:
        questions.append({
                "text": question["text"],
                "index": i,
                "points": question["points"],
                "all_answers": question["all_answers"],
                "answer_type": question["answer_type"],
                "description": question["description"],
                "attachment_url": "",
                "correct_answers": question["correct_answers"]
            })
        i+=1

    newExam = ExaminationForm(
            lesson=lesson,
            name=parsed_exam["name"],
            description=parsed_exam["description"],
            questions=questions,
            test_mode="manual",
            max_points=100
        )

    newExam.save()


@app.task
def generate_notes_for_lesson(lessonId: int, userId: int):

    lesson = Lesson.objects.select_related("course").filter(id=lessonId).first()
    user = User.objects.filter(id=userId).first()

    aiModel = AiModel()
    course = lesson.course
    response = aiModel.generateNote(
        courseName=course.name if course else "",
        courseDescription=course.description if course else "",
        lessonName=lesson.name,
        lessonDescription=lesson.description,
    )
    clean_json = re.sub(r'^```json\s*|\s*```$', '', response.text.strip())
    parsed_response = json.loads(clean_json)

    for topic in parsed_response["topics"]:
        newMaterial = LessonContent(name=topic["topicTitle"],
                                    lesson=lesson,
                                    content_type="text",
                                    author=user,
                                    is_teacher_only=False)
        newMaterial.content.save(gen_hash_name(topic["content"] + '.txt'),
                                 ContentFile(topic["content"]))
        newMaterial.save()


@app.task
def send_submit_to_cats():
    print('sending sol. tasks', end=' ')
    cats_submit: CatsSubmit = CatsSubmit.objects.filter(
        is_sent=False).order_by('id').first()
    print(len(list(CatsSubmit.objects.filter(is_sent=False))))
    if not cats_submit:
        return
    # TODO: check correctness of the response
    cats_account = cats_submit.submit.student.cats_account.username
    try:
        ids, response = cats_submit_solution(**cats_submit.data,
                                             cats_account=cats_account)
    except (CatsAnswerCodeException, CatsNormalErrorException) as exception:
        print('exception below')
        cats_submit.is_error = True
        cats_submit.is_sent = True
        cats_submit.sending_result = dict(
            data={
                **cats_submit.data,
                'submit_as': cats_account,
            },
            response=dict(
                headers=exception.response.headers.__dict__,
                content=exception.response.json(),
            ),
        )
        cats_submit.save()
        log_event = LogEvent(
            problem=cats_submit.submit.problem,
            student=cats_submit.submit.student,
            submit=cats_submit.submit,
            type=LogEvent.TYPE_CATS_ERROR,
            data=dict(message='Ошибка при отправке в cats',
                      content=exception.response.content.decode('utf-8'),
                      reason=exception.response.reason))
        log_event.save()
        return

    cats_submit.sending_result = response
    cats_submit.id_to_check = ids
    if ids:
        cats_submit.is_sent = True
        log_event = LogEvent(
            problem=cats_submit.submit.problem,
            student=cats_submit.submit.student,
            type=LogEvent.TYPE_CATS_SUBMIT,
            submit=cats_submit.submit,
            data=dict(message='Отправлено на проверку в cats'))
        log_event.save()
    cats_submit.save()

    return


@app.task
def update_submit_status():
    print('checking statuses tasks')
    query = CatsSubmit.objects \
        .select_related('submit') \
        .filter(is_sent=True, is_error=False, testing_result__isnull=True, id_to_check__isnull=False)
    if not query:
        print('nothing to update')
    for cats_submit in query:
        new_status, data = cats_check_solution_status(cats_submit.id_to_check)
        if not new_status or new_status in ['NP', 'T', 'P']:
            continue

        log_event = LogEvent(
            problem=cats_submit.submit.problem,
            student=cats_submit.submit.student,
            submit=cats_submit.submit,
            type=LogEvent.TYPE_CATS_ANSWER,
            data=dict(message='Результат тестирования получен'))
        log_event.save()
        if new_status == Submit.OK and \
                cats_submit.submit.problem.test_mode == Problem.TEST_MODE_TYPES[2][0]:
            cats_submit.submit.status = Submit.AWAITING_MANUAL
        else:
            cats_submit.submit.status = new_status

        cats_submit.submit.updated_by = None
        cats_submit.submit.save(update_fields=['status', 'updated_by'])
        cats_submit.testing_result = data[
            0]  # Todo: investigate why the hell its a list
        cats_submit.save()


@app.task
def send_email(token, email, hostname):
    email_plaintext_message = f"""
    Ссылка для восстановления пароля: 
    {hostname.strip('/')}/reset?token={token}"""

    send_mail("Password Reset for dvfu lms", email_plaintext_message,
              "learn@dvfu.ru", [email])
