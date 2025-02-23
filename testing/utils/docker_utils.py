import docker
import json

def run_code_in_docker(code, language, input_output, time_limit, memory_limit):
    client = docker.from_env()

    input_data = '\n'.join([test_case['input'] for test_case in input_output])
    expected_output = [test_case['output'] for test_case in input_output]

    container = client.containers.run(
        image=f'{language}-runner',
        stdin_open=True,
        network_disabled=True,
        mem_limit=f'{memory_limit}m',
        cpu_period=100000,
        cpu_quota=int(time_limit * 100000),
        detach=True,
        remove=True,
        command=f"python3 /app/runner.py {language}",
    )

    # Передаем код и входные данные внутрь контейнера
    container.exec_run(cmd="sh -c 'cat > /dev/stdin'", stdin=True, socket=True).send(f"{code}\n{input_data}".encode())

    # Ждем завершения
    result = container.wait()
    logs = container.logs().decode('utf-8')
    results = json.loads(logs)

    # Проверяем результат
    test_results = []
    for i, (expected, actual) in enumerate(zip(expected_output, results['output'].split('\n'))):
        test_results.append({
            'test_case': i + 1,
            'expected': expected,
            'actual': actual,
            'passed': expected == actual
        })

    return {
        'test_results': test_results,
        'execution_time': results['execution_time'],
        'memory_used': results.get('memory_used', 0),
        'status': 'OK' if all(t['passed'] for t in test_results) else 'WA'
    }
