import json

from celery.utils.log import get_task_logger

from cathie.cats_api import cats_check_solution_status, cats_submit_solution
from cathie.exceptions import CatsAnswerCodeException, CatsNormalErrorException
from celery_app.celery_settings import app
from problem.models import Submit, CatsSubmit, LogEvent

logger = get_task_logger(__name__)

PROCESSED_STATUSES = [
    status for status, description in Submit.SUBMIT_STATUS if status not in ('NP', 'AW')
]


@app.task
def send_submit_to_cats():
    print('sending sol. tasks', end=' ')
    cats_submit: CatsSubmit = CatsSubmit.objects.filter(is_sent=False).order_by('id').first()
    print(len(list(CatsSubmit.objects.filter(is_sent=False))))
    if not cats_submit:
        return
    # TODO: check correctness of the response
    cats_account = cats_submit.submit.student.cats_account.username
    try:
        ids, response = cats_submit_solution(**cats_submit.data, cats_account=cats_account)
    except (CatsAnswerCodeException, CatsNormalErrorException) as exception:
        print('exception below')
        cats_submit.is_error = True
        cats_submit.is_sent = True
        cats_submit.sending_result = dict(
            data={**cats_submit.data, 'submit_as': cats_account, },
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
            data=dict(
                message='Ошибка при отправке в cats',
                content=exception.response.content.decode('utf-8'),
                reason=exception.response.reason
            )
        )
        log_event.save()
        return

    cats_submit.sending_result = response
    cats_submit.id_to_check = ids
    if ids:
        cats_submit.is_sent = True
        log_event = LogEvent(
            problem=cats_submit.submit.problem, student=cats_submit.submit.student, type=LogEvent.TYPE_CATS_SUBMIT,
            submit=cats_submit.submit,
            data=dict(message='Отправлено на проверку в cats')
        )
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
            problem=cats_submit.submit.problem, student=cats_submit.submit.student,
            submit=cats_submit.submit,
            type=LogEvent.TYPE_CATS_ANSWER, data=dict(message='Результат тестирования получен')
        )
        log_event.save()

        cats_submit.submit.status = new_status
        cats_submit.submit.updated_by = None
        cats_submit.submit.save(update_fields=['status', 'updated_by'])
        cats_submit.testing_result = data[0]  # Todo: investigate why the hell its a list
        cats_submit.save()
