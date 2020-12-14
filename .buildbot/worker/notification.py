import os
import random
import subprocess

import telegram
from env import *

try:
    os.chdir('frontend')
    c = subprocess.run(["npm", "run", "build"]).returncode
except:
    c = 1


def build_message(code):
    answer = f'Build branch: ' \
             f'{subprocess.check_output(["git", "branch", "--show-current"]).decode("utf-8")}'
    answer += subprocess.check_output(['git', 'log', '--pretty=format:%h - %an: %s', '-1']).decode('utf-8')
    if not code:
        answer += f'<b>npm run build</b> was successful! {random.choice(["🚀🎉", "💅💃"])}\n Gj, gl and proceed.'
    else:
        answer += '<b>npm run build</b> failed 🤦. Go and fix it!'

    return answer


bot = telegram.Bot(token=os.getenv(BOT_TOKEN))
bot.send_message(os.getenv(CHAT_ID), build_message(c), parse_mode='HTML')
bot.close()
