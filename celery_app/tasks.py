from celery.utils.log import get_task_logger

from cathie.cats_api import cats_check_solution_status, cats_submit_solution
from celery_app.celery_settings import app
from problem.models import Submit, CatsSubmit

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
        if new_status is not None:
            cats_submit.submit.status = new_status
            cats_submit.submit.save()
            cats_submit.testing_result = data
            cats_submit.save()
        print(cats_submit.status)


@app.task
def send_submit_to_cats():
    print('sending sol. tasks')
    submit = CatsSubmit.objects.filter(is_sent=False).order_by('id').first()
    if not submit:
        return
    ids, response = cats_submit_solution(**submit.data)
    submit.is_sent = True
    submit.sending_result = response
    submit.id_to_check = ids
    submit.save()
    return
