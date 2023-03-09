import random
import telegram
from .env import BOT_TOKEN, CHAT_ID


def run(steps: list):
    step_result = 0
    result_message = ''
    for step in steps:
        step_result, message = step()
        if message:
            result_message += '\n' + message
        if step_result:
            result_message = '❌' + result_message
            break
    if not step_result:
        result_message = '✅' + result_message
        result_message += '\n' + f'Production deployed. Whooray!. {random.choice(["🚀🍻", "🥇👑"])}'
    print(result_message)
    bot = telegram.Bot(token=BOT_TOKEN)
    bot.send_message(CHAT_ID, result_message, parse_mode='html', disable_notification=True)
    exit(step_result)