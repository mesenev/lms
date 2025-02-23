from celery import shared_task
from testing.models import TestingQueue, InProgressTesting, TestingSubmit
from testing.utils.docker_utils import run_code_in_docker

@shared_task
def check_solutions():
    # Берём первое решение из очереди
    queue_item = TestingQueue.objects.first()
    if not queue_item:
        return

    submit = queue_item.submit

    # Перемещаем решение в "проверяемые"
    InProgressTesting.objects.create(submit=submit)
    queue_item.delete()

    # Запускаем проверку в Docker-контейнере
    problem = submit.problem
    results = run_code_in_docker(
        code=submit.content.read().decode('utf-8'),
        language=problem.language,
        input_output=problem.input_output,
        time_limit=problem.time_limit,
        memory_limit=problem.memory_limit
    )

    # Обновляем статус и результаты
    submit.testing_results = results['test_results']
    submit.execution_time = results['execution_time']
    submit.memory_used = results['memory_used']
    submit.status = results['status']
    submit.save()

    # Удаляем из "проверяемых"
    InProgressTesting.objects.filter(submit=submit).delete()
