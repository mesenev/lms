import subprocess


def build_message(code):
    if code:
        return 'Backend tests succeed!'
    return 'Database deploy failed.'


def test_backend():
    exec_code = subprocess.run(
        [
            'docker-compose',
            '-f',
            '.docker/docker-compose.dev.yml',
            'run',
            'backend',
            'python',
            'manage.py',
            'test',
        ]
    )
    return exec_code, build_message(exec_code)
