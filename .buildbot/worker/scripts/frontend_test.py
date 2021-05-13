import random
import subprocess


def build_message(code):
    if code:
        return f'<b>npm run test:unit</b> failed'
    return f'<b>npm run test:unit</b> was successful!'


def test_frontend():
    exec_code = subprocess.run(["npm", "run", "test:unit"]).returncode
    return exec_code, build_message(exec_code)
