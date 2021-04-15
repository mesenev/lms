import random
import subprocess


def build_message(code):
    answer = ''
    if not code:
        answer += f'<b>npm run build</b> was successful! \
        {random.choice(["🚀🎉", "💅💃"])}\n Gj, gl and proceed.'
    else:
        answer += f'<b>npm run build</b> failed {random.choice(["🤦", "🤢"])}.\
         Go and fix it!'
    return answer


def build_frontend():
    print('installing frontend dependencies')
    exec_code = subprocess.run(["npm", "install", ]).returncode
    if exec_code:
        return exec_code, '<b>npm install</b> failed {random.choice(["🤦", "🤢"])}. Go and fix it!'
    print('`npm run build` on the run')
    exec_code = subprocess.run(["npm", "run", "build"]).returncode
    return exec_code, build_message(exec_code)

