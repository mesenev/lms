from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from problem.models import Submit, ProblemStats


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
    stats.yellow = len(list((filter(lambda x: x.status == Submit.AWAITING_MANUAL, queryset))))
    stats.red = len(list((filter(lambda x: x.status not in [Submit.OK, Submit.AWAITING_MANUAL], queryset))))
    stats.save()


post_save.connect(update_problem_status, weak=False, sender=Submit)
