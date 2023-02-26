import random
import subprocess


def build_message(code):
    answer = ''
    if not code:
        answer += f'npm run build successful!'
    else:
        answer += f'npm run build failed.'
    return answer


def build_frontend():
    print('installing frontend dependencies')
    exec_code = subprocess.run(["npm", "install", ]).returncode
    if exec_code:
        return exec_code, 'npm install failed'
    print('`npm run build` on the run')
    exec_code = subprocess.run(["npm", "run", "build"]).returncode
    return exec_code, build_message(exec_code)
