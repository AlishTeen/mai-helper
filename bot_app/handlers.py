import re

from telebot import types

from bot_app import bot, db, df, temp_user_data, markups, utils, logger, register_proc
import bot_app.emojis as ej


# MIDDLEWARE

@bot.middleware_handler(update_types=['callback_query'])
def middle_callback_handler(bot_instance, call):
    if not db.user_exists(call.from_user.id):
        bot_instance.answer_callback_query(call.id, 'Вы не зарегистрированы в системе.')


# СТАРТ
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user = db.get_user(message.from_user.id)
    temp = bot.send_message(message.chat.id, f'{ej.LOAD_EMOJI}', reply_markup=markups.no_markup())
    bot.delete_message(temp.chat.id, temp.id)
    if user:
        msg = bot.send_message(message.chat.id, f'{ej.HOME_EMOJI} Главная',
                               reply_markup=markups.main_markup())
        db.edit_user(message.from_user.id, username=message.from_user.username,
                     first_name=message.from_user.first_name, menu_id=msg.id, state='REGULAR')
        if user.menu_id:
            bot.delete_message(message.chat.id, user.menu_id)
    else:
        bot.send_message(message.chat.id,
                         f'Здравствуйте, {message.from_user.first_name}.\n'
                         f'Вас приветствует официальный Telegram Bot приемной комиссии филиала "Восход" МАИ.\n'
                         f'Заполнив необходимые анкетные данные, '
                         f'Вы сможете получить доступ к информации о ходе приемной кампании.',
                         reply_markup=markups.login_markup())


# РЕГИСТРАЦИЯ
@bot.callback_query_handler(func=lambda call: call.data == 'register')
def register_call(call):
    register_proc.register(call)


# МЕНЮ

@bot.callback_query_handler(func=lambda call: call.data == 'main_menu')
def home_callback(call):
    if call.from_user.id in temp_user_data:
        temp_user_data.pop(call.from_user.id)

    bot.clear_step_handler(call.message)

    temp = bot.send_message(call.message.chat.id, f'{ej.LOAD_EMOJI}', reply_markup=markups.no_markup())
    bot.delete_message(temp.chat.id, temp.id)

    if db.user_exists(call.from_user.id):
        db.edit_user(call.from_user.id, state='REGULAR')
        bot.edit_message_text(f'{ej.HOME_EMOJI} Главная', call.message.chat.id, call.message.id,
                              reply_markup=markups.main_markup())
        bot.answer_callback_query(call.id)
    else:
        bot.edit_message_text(f'Здравствуйте, {call.message.from_user.first_name}.\n'
                              f'Вас приветствует официальный Telegram Bot приемной комиссии филиала "Восход" МАИ.\n'
                              f'Заполнив необходимые анкетные данные, '
                              f'Вы сможете получить доступ к информации о ходе приемной кампании.',
                              call.message.chat.id, call.message.id, reply_markup=markups.login_markup())


@bot.callback_query_handler(func=lambda call: call.data == 'contacts')
def contacts_callback(call):
    bot.answer_callback_query(call.id)
    bot.edit_message_text(ej.CONTACTS, call.message.chat.id, call.message.id, parse_mode='markdown',
                          disable_web_page_preview=True, reply_markup=markups.back_markup())


@bot.callback_query_handler(func=lambda call: call.data == 'settings')
def settings_callback(call):
    if db.user_exists(call.from_user.id):
        bot.answer_callback_query(call.id)
        bot.edit_message_text(f'{ej.SETTING_EMOJI} Настройки', call.message.chat.id, call.message.id,
                              reply_markup=markups.settings_markup())


# НАСТРОЙКИ

# УДАЛЕНИЕ ПОЛЬЗОВАТЕЛЯ

@bot.callback_query_handler(func=lambda call: call.data == 'settings-delete_acc')
def settings_delete_user_callback(call):
    if db.user_exists(call.from_user.id):
        bot.answer_callback_query(call.id)
        query = {'yes': f'DELETE-{utils.random_string(6)}'}
        bot.edit_message_text('Вы действительно хотите удалить свои анкетные данные?',
                              call.message.chat.id, call.message.id,
                              reply_markup=markups.confirm_markup_inline(query['yes']))
        db.edit_user(call.from_user.id, state=query['yes'])


@bot.callback_query_handler(func=lambda call: 'DELETE' in call.data)
def settings_delete_user_confirm_callback(call):
    user = db.get_user(call.from_user.id)
    if user:
        if user.state == call.data:
            db.delete_user(user.user_id)
            bot.answer_callback_query(call.id, 'Ваши анкетные данные были удалёны из базы.\n'
                                               'Очистите историю чата.',
                                      show_alert=True)
            bot.delete_message(call.message.chat.id, call.message.id)
        else:
            db.edit_user(call.from_user.id, state='REGULAR')
            home_callback(call)


# РЕДАКТИРОВАНИЕ ПОЛЬЗОВАТЕЛЯ

@bot.callback_query_handler(func=lambda call: call.data == 'settings-edit_acc')
def settings_edit_user(call):
    register_proc.register(call, query='edit')


# ЗАДАТЬ ВОПРОС

@bot.callback_query_handler(func=lambda call: call.data == 'popular')
def popular_callback(call):
    if db.user_exists(call.from_user.id):
        bot.answer_callback_query(call.id)
        bot.edit_message_text(ej.STAR_EMOJI, call.message.chat.id,
                              call.message.id, reply_markup=markups.back_markup(text=f'{ej.BACK_EMOJI} Назад'))
        db.edit_user(call.from_user.id, state='DIALOGFLOW')
        bot.send_message(call.message.chat.id,
                         'Вы можете получить интересующую информацию нажав на одну из кнопок ниже, '
                         'или задав вопрос в произвольной форме.',
                         reply_markup=markups.popular_markup())


# ВОПРОС ПК

@bot.callback_query_handler(func=lambda call: call.data == 'new_question')
def new_question_callback(call):
    user = db.get_user(call.from_user.id)
    if user:
        msg = bot.edit_message_text('Введите свой вопрос', call.message.chat.id, call.message.id,
                                    reply_markup=markups.back_markup(text=f'{ej.DENY1_EMOJI} Отмена'))
        bot.register_next_step_handler(msg, new_question_apply, user, call)


def new_question_apply(message, user, call):
    if user and message.text:
        msg_text = message.text.strip()
        msg_text = re.sub(r'\s+', ' ', msg_text)
        if len(msg_text) > 10:
            qid = db.add_question(message.from_user.id, msg_text)
            if qid:
                bot.send_message(message.from_user.id,
                                 f'Вопрос адресован сотруднику приемной комиссии, в ближайшее время с Вами свяжутся.\n'
                                 f'ID вопроса: _{qid}_', parse_mode='Markdown')
            else:
                bot.send_message(message.from_user.id, 'Возникла ошибка, попробуйте позже.')
        bot.delete_message(message.chat.id, call.message.id)
        send_welcome(message)


# DIALOGFLOW

@bot.message_handler(func=lambda message: True)
def dialogflow(message):
    user = db.get_user(message.from_user.id)
    if user and user.state == 'DIALOGFLOW':
        bot.send_chat_action(message.chat.id, 'typing')
        answer, intent, images = df.get_answer(message.text, message.chat.id)
        markup = markups.question_markup() if intent == 'Default Fallback Intent' else None
        db.stat_dialogflow_inc()
        if answer:
            bot.reply_to(message, answer, reply_markup=markup, parse_mode='Markdown')
        if images:
            bot.send_media_group(message.chat.id, [types.InputMediaPhoto(image) for image in images])
    else:
        logger.info(f'Message from {message.from_user.username}: {message.text}')
