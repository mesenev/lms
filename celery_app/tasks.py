from celery.utils.log import get_task_logger

from cathie.cats_api import cats_check_solution_status
from celery_app.celery_settings import app
from problem.models import Submit


logger = get_task_logger(__name__)

PROCESSED_STATUSES = [status for status, description in Submit.SUBMIT_STATUS if status not in ('NP', 'AW')]


@app.task
def update_submit_status():
    query = Submit.objects.filter(cats_request_id__isnull=False).exclude(status__in=PROCESSED_STATUSES)
    for submit in query:
        new_status = cats_check_solution_status(submit.cats_request_id)
        if new_status is not None:
            submit.status = new_status
        submit.save()
        print(submit.status)
