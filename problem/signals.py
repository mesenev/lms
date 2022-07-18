from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from problem.models import Submit, ProblemStats, LogEvent
from problem.serializers import LogEventSerializer


@receiver(post_save, sender=Submit)
def update_problem_status(sender, instance, **kwargs):
    try:
        stats: ProblemStats = ProblemStats.objects.get(problem=instance.problem)
    except ProblemStats.DoesNotExist:
        stats: ProblemStats = ProblemStats(problem=instance.problem)
    queryset = Submit.objects.annotate(
        ordering=models.Case(
            models.When(status="OK", then=models.Value(0)),
            models.When(status="AW", then=models.Value(1)),
            default=models.Value(2),
            output_field=models.IntegerField()
        )
    ).filter(problem=instance.problem).order_by('student', 'ordering', '-id').distinct('student')
    stats.green = len(list((filter(lambda x: x.status == Submit.OK, queryset))))
    stats.yellow = len(list((filter(lambda x: x.status in [Submit.AWAITING_MANUAL, Submit.DEFAULT_STATUS], queryset))))
    stats.red = len(list((filter(
        lambda x: x.status not in [Submit.OK, Submit.AWAITING_MANUAL, Submit.DEFAULT_STATUS],
        queryset
    ))))
    stats.save()


@receiver(post_save, sender=Submit)
def create_log_event(sender, instance: Submit, created, **kwargs):
    log_event = LogEvent(problem=instance.problem, student=instance.student)
    if created:
        log_event.type = LogEvent.TYPE_SUBMIT
        log_event.submit = instance
        log_event.author = instance.student
        log_event.data = dict(message=instance.id)
        log_event.save()
        return
    if kwargs['update_fields'] and 'status' in kwargs['update_fields']:
        log_event.type = LogEvent.TYPE_STATUS_CHANGE
        log_event.submit = instance
        if log_event.submit.updated_by:
            log_event.author = log_event.submit.updated_by
        log_event.data = dict(message=f'Статус изменён на {instance.status}')
        log_event.save()
        return


@receiver(post_save, sender=LogEvent)
def send_log_event_via_ws(sender, instance: LogEvent, created, **kwargs):
    if not created:
        return
    channels = get_channel_layer()
    async_to_sync(channels.group_send)(
        f'{instance.student.id}-{instance.problem.id}',
        {'type': 'log_event', 'log_event': LogEventSerializer(instance).data}
    )
    return


post_save.connect(update_problem_status, weak=False, sender=Submit)
post_save.connect(create_log_event, weak=False, sender=Submit)
post_save.connect(send_log_event_via_ws, weak=False, sender=LogEvent)
