import random
import subprocess


def build_message(code):
    if code:
        return f'npm run test:unit failed'
    return f'npm run test:unit was successful!'


def test_frontend():
    exec_code = subprocess.run(["npm", "run", "test:unit"]).returncode
    return exec_code, build_message(exec_code)
