import re

from pyisemail import is_email
from geocoder import geonames

from bot_app import bot, db, markups, temp_user_data, emojis, handlers, utils
from bot_app.models import User


def register(call, query='register'):
    if call.from_user.id not in temp_user_data:
        if db.user_exists(call.from_user.id) and query == 'register':
            bot.answer_callback_query(call.id, 'Вы уже авторизованы в системе.')
        else:
            temp_user_data[call.from_user.id] = User(user_id=call.from_user.id,
                                                     username=call.from_user.username,
                                                     first_name=call.from_user.first_name)
            bot.delete_message(call.message.chat.id, call.message.id)
            msg = bot.send_message(call.message.chat.id,
                                   'Продолжая регистрацию, Вы даёте согласие на обработку и хранение '
                                   'персональных данных.')
            bot.send_message(call.message.chat.id, 'Введите ваше имя:',
                             reply_markup=markups.back_markup(text=f'{emojis.DENY1_EMOJI} Отмена'))
            bot.register_next_step_handler(msg, register_name, msg_id=msg.id)


def register_name(message, msg_id):
    cyrillic = re.compile('^[А-Яа-я]+$')
    name = message.text
    if cyrillic.match(name):
        temp_user_data[message.from_user.id].real_name = name.capitalize()
        msg = bot.send_message(message.chat.id, 'Предоставьте свой номер телефона.',
                               reply_markup=markups.number_markup())
        bot.register_next_step_handler(msg, register_number, msg_id=msg_id)
    else:
        msg = bot.send_message(message.chat.id, 'Введите имя кириллицей:')
        bot.register_next_step_handler(msg, register_name, msg_id=msg_id)


def register_number(message, msg_id):
    if message.content_type == 'contact':
        temp_user_data[message.from_user.id].phone_number = message.contact.phone_number
        msg = bot.send_message(message.chat.id, 'Теперь введите ваш e-mail адрес:', reply_markup=markups.no_markup())
        bot.register_next_step_handler(msg, register_email, msg_id=msg_id)
    else:
        msg = bot.send_message(message.chat.id, 'Предоставьте доступ к номеру телефона, нажав на кнопку ниже.')
        bot.register_next_step_handler(msg, register_number, msg_id=msg_id)


def register_email(message, msg_id):
    email = message.text
    if is_email(email):
        temp_user_data[message.from_user.id].email_address = email
        msg = bot.send_message(message.chat.id, 'Ваше гражданство:', reply_markup=markups.nation_markup())
        bot.register_next_step_handler(msg, register_nation, msg_id=msg_id)
    else:
        msg = bot.send_message(message.chat.id, 'Неверный e-mail адрес. Попробуйте ещё раз:')
        bot.register_next_step_handler(msg, register_email, msg_id=msg_id)


def register_nation(message, msg_id):
    nation = message.text
    if nation in ['🇷🇺 РФ', '🇰🇿 РК']:
        temp_user_data[message.from_user.id].nation = nation
        msg = bot.send_message(message.chat.id, 'Введите город проживания:',
                               reply_markup=markups.no_markup())
        bot.register_next_step_handler(msg, register_geo, msg_id=msg_id)
    else:
        msg = bot.send_message(message.chat.id, 'Выберите Ваше гражданство из списка ниже:',
                               reply_markup=markups.nation_markup())
        bot.register_next_step_handler(msg, register_nation, msg_id=msg_id)


def register_geo(message, msg_id):
    geo = geonames(message.text, fuzzy=0.8, key='cobalt')
    if geo.address:
        temp_user_data[message.from_user.id].geo = geo.address
        temp_user_data[message.from_user.id].avatar_b64 = utils.thumbnail_from_id(message.from_user.id)
        complete_register(message, msg_id)
    else:
        msg = bot.send_message(message.chat.id, 'Не удалось найти город, проверьте название города.')
        bot.register_next_step_handler(msg, register_geo, msg_id=msg_id)


def complete_register(message, msg_id):
    if not db.user_exists(message.from_user.id):
        if db.add_user(temp_user_data[message.from_user.id]):
            bot.send_message(message.chat.id, 'Вы успешно зарегистрировались.')
        else:
            bot.send_message(message.chat.id, 'Возникла ошибка.')
    else:
        if db.edit_user(user_id=message.from_user.id, user_obj=temp_user_data[message.from_user.id]):
            bot.send_message(message.chat.id, 'Сохранено!')
        else:
            bot.send_message(message.chat.id, 'Возникла ошибка.')
    for i in range(int(msg_id), int(message.id + 1)):
        bot.delete_message(message.from_user.id, i)
    temp_user_data.pop(message.chat.id)
    handlers.send_welcome(message)
