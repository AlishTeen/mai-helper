import os
import time
from telebot import apihelper, types
from sweater import app
from bot_app import bot


def send_message(user_id, qid, text, question):
    response_text = f'*Ваш вопрос #{qid} с текстом:*\n_{question}_\n\n*получил ответ от приёмной комиссии:*\n_{text}_'
    try:
        bot.send_message(user_id, response_text, parse_mode='Markdown')
        return True
    except apihelper.ApiTelegramException:
        return False


def mailing(users_id, text):
    t0 = time.time()
    success = 0
    message = f'*Сообщение от приёмной комиссии*:\n_{text}_'
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    filenames = [os.path.join(app.config['UPLOAD_FOLDER'], file) for file in files]
    for i, uid in enumerate(users_id):
        try:
            bot.send_message(uid, message, parse_mode='Markdown')
            if len(files):
                print(f'Files-{i} before: {time.time() - t0}')
                files_group = [types.InputMediaDocument(open(filepath, 'rb')) for filepath in filenames]
                bot.send_media_group(uid, files_group)
                print(f'Files-{i} after: {time.time() - t0}')
            success += 1
        except apihelper.ApiTelegramException as e:
            pass
    return success
