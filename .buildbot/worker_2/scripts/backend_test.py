import subprocess
from typing import Tuple


def build_message(code) -> str:
    return 'Backend tests failed.' if code else 'Backend tests succeed!'


def test_backend(*args) -> Tuple[int, str]:
    exec_code = subprocess.run(
        [
            'docker-compose',
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
