import os
import subprocess
import sys

import telegram
from env import BOT_TOKEN, CHAT_ID

sys.dont_write_bytecode = True

def chdir(directory):
    return lambda: [0, '', os.chdir(directory)][:2]


if __name__ == '__main__':
    branch_name = subprocess.check_output(
        ["git", "branch", "--show-current"]
    ).decode("utf-8")
    result_message = f'Build branch: {branch_name}'
    result_message += subprocess.check_output(
        ['git', 'log', '--pretty=format:%h - %an: %s', '-1']
    ).decode('utf-8')

    steps = [
        chdir('frontend'),
        build_frontend,
        chdir('..'),
        build_backend,
        test_backend,
        deploy_backend,
    ]
    step_result = 0
    for step in steps:
        step_result, message = step()
        if message:
            result_message += '\n' + message
        if step_result:
            break
    if not step_result:
        result_message += '\n' + 'Well done. All systems operational. 🚀'
    print(result_message)
    bot = telegram.Bot(token=BOT_TOKEN)
    bot.send_message(CHAT_ID, result_message)
    exit(step_result)
