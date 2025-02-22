import docker
import json
import time

def run_code_in_docker(code, language, input_output, time_limit, memory_limit):
    client = docker.from_env()

    # Подготовка входных данных
    input_data = [test_case['input'] for test_case in input_output]
    expected_output = [test_case['output'] for test_case in input_output]

    # Запуск контейнера
    container = client.containers.run(
        image=f'{language}-runner',  # Например, "python-runner"
        command=f'python3 /app/runner.py',  # Команда для запуска
        mem_limit=f'{memory_limit}m',  # Ограничение памяти
        cpu_period=100000,
        cpu_quota=int(time_limit * 100000),  # Ограничение CPU
        network_disabled=True,  # Отключаем сеть
        remove=True,  # Удаляем контейнер после завершения
        detach=True  # Запускаем в фоновом режиме
    )

    # Ожидание завершения
    container.wait()

    # Получение результатов
    logs = container.logs().decode('utf-8')
    results = json.loads(logs)

    return {
        'test_results': results['test_results'],
        'execution_time': results['execution_time'],
        'memory_used': results['memory_used'],
        'status': results['status']
    }