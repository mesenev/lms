from celery.utils.log import get_task_logger

from cathie.cats_api import cats_check_solution_status
from celery_app.celery_settings import app
from problem.models import Submit


logger = get_task_logger(__name__)


@app.task
def update_submit_status():
    for submit in Submit.objects.filter(cats_request_id__isnull=False):
        new_status = cats_check_solution_status(submit.cats_request_id)
        if new_status is not None:
            submit.status = new_status
        submit.save()
