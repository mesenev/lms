import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'imcslms.settings')

app = Celery('imcslms')

app.conf.CELERY_ALWAYS_EAGER = False
app.conf.CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'check_submit_status': {
        'task': 'celery_app.tasks.update_submit_status',
        'schedule': 10.0,
    },
    'send_solution': {
        'task': 'celery_app.tasks.send_submit_to_cats',
        'schedule': 6.0,
    }
}
