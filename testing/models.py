from django.db import models
from problem.models import Problem, Submit

class TestingProblem(Problem):
    """
    Расширяем модель Problem для задач, которые проверяются на сервере.
    """
    input_output = models.JSONField(default=list)  # Список пар входных/выходных данных
    time_limit = models.FloatField(default=1.0)  # Ограничение по времени (в секундах)
    memory_limit = models.IntegerField(default=128)  # Ограничение по памяти (в МБ)

    class Meta:
        verbose_name = 'Testing Problem'
        verbose_name_plural = 'Testing Problems'


class TestingSubmit(Submit):
    """
    Расширяем модель Submit для решений, которые проверяются на сервере.
    """
    testing_results = models.JSONField(null=True, blank=True)  # Результаты тестирования
    execution_time = models.FloatField(null=True, blank=True)  # Затраченное время
    memory_used = models.IntegerField(null=True, blank=True)  # Затраченная память

    class Meta:
        verbose_name = 'Testing Submit'
        verbose_name_plural = 'Testing Submits'


class TestingQueue(models.Model):
    """
    Очередь задач на проверку.
    """
    submit = models.OneToOneField(TestingSubmit, on_delete=models.CASCADE, primary_key=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Testing Queue'
        verbose_name_plural = 'Testing Queues'


class InProgressTesting(models.Model):
    """
    Задачи, которые сейчас проверяются.
    """
    submit = models.OneToOneField(TestingSubmit, on_delete=models.CASCADE, primary_key=True)
    started_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'In Progress Testing'
        verbose_name_plural = 'In Progress Testing'
