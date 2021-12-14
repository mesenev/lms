from celery.utils.log import get_task_logger

from cathie.cats_api import cats_check_solution_status, cats_submit_solution
from celery_app.celery_settings import app
from problem.models import Submit, CatsSubmit, LogEvent

logger = get_task_logger(__name__)

PROCESSED_STATUSES = [
    status for status, description in Submit.SUBMIT_STATUS if status not in ('NP', 'AW')
]


@app.task
def update_submit_status():
    print('checking statuses tasks')
    query = CatsSubmit.objects \
        .select_related('submit') \
        .filter(is_sent=True, testing_result=None)
    for cats_submit in query:
        new_status, data = cats_check_solution_status(cats_submit.id_to_check)
        if not new_status:
            continue

        log_event = LogEvent(
            problem=cats_submit.submit.problem, student=cats_submit.submit.student,
            type=LogEvent.TYPE_CATS_ANSWER, data=dict(message='Результат тестирования получен')
        )
        log_event.save()

        cats_submit.submit.status = new_status
        cats_submit.submit.updated_by = None
        cats_submit.submit.save(update_fields=['status', 'updated_by'])
        cats_submit.testing_result = data
        cats_submit.save()


@app.task
def send_submit_to_cats():
    print('sending sol. tasks')
    submit = CatsSubmit.objects.filter(is_sent=False).order_by('id').first()
    if not submit:
        return
    # TODO: check correctness of the response
    ids, response = cats_submit_solution(**submit.data)
    submit.sending_result = response
    submit.id_to_check = ids
    if ids:
        submit.is_sent = True
        log_event = LogEvent(
            problem=submit.submit.problem, student=submit.submit.student, type=LogEvent.TYPE_CATS_SUBMIT,
            data=dict(message='Отправлено на проверку в cats')
        )
        log_event.save()
    submit.save()

    return
