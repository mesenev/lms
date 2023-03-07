import subprocess


def build_message(code):
    if not code:
        return 'Backend tests succeed!'
    return 'Backend tests failed.'


def test_backend():
    exec_code = subprocess.run(
        [
            "docker", "compose",
            '-f',
            ".docker/docker-compose.prod.yml",
            'run',
            'backend',
            'python',
            'manage.py',
            'test',
            '--noinput'
        ]
    ).returncode
    return exec_code, build_message(exec_code)
