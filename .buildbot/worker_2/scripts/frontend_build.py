import subprocess
from typing import Tuple


def build_message(code) -> str:
    return f'<b>npm run build</b> failed.' if code else f'<b>npm run build</b> successful!'


def build_frontend(branch_name: str) -> Tuple[int, str]:
    print(f'installing frontend dependencies for branch: {branch_name}')
    exec_code = subprocess.run(["npm", "install", ]).returncode
    if exec_code:
        return exec_code, '<b>npm install</b> failed'
    print('`npm run build` on the run')
    exec_code = subprocess.run(["npm", "run", "build"]).returncode
    return exec_code, build_message(exec_code)
