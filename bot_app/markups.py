from telebot import types
import bot_app.emojis as ej


def login_markup():
    markup = types.InlineKeyboardMarkup()
    buttons = [types.InlineKeyboardButton(f'{ej.KEY_EMOJI} Заполнить анкету', callback_data='register'),
               types.InlineKeyboardButton(f'{ej.TEL_EMOJI} Контакты', callback_data='contacts')]
    for button in buttons:
        markup.row(button)
    return markup


def main_markup():
    markup = types.InlineKeyboardMarkup()
    buttons = [types.InlineKeyboardButton(f'{ej.SEARCH_EMOJI} Получить информацию', callback_data='popular'),
               types.InlineKeyboardButton(f'{ej.TEL_EMOJI} Контакты', callback_data='contacts'),
               types.InlineKeyboardButton(f'{ej.SETTING_EMOJI} Настройки', callback_data='settings')]
    for button in buttons:
        markup.row(button)
    return markup


def settings_markup():
    markup = types.InlineKeyboardMarkup()
    buttons = [types.InlineKeyboardButton(f'{ej.EDIT_EMOJI} Редактировать анкету',
                                          callback_data='settings-edit_acc'),
               types.InlineKeyboardButton(f'{ej.DENY2_EMOJI} Удалить анкету',
                                          callback_data='settings-delete_acc'),
               types.InlineKeyboardButton(f'{ej.HOME_EMOJI} Главная',
                                          callback_data='main_menu')]
    for button in buttons:
        markup.row(button)

    return markup


def confirm_markup_inline(*args):
    markup = types.InlineKeyboardMarkup()
    buttons = [types.InlineKeyboardButton(f'{ej.CONFIRM_EMOJI}', callback_data=args[0]),
               types.InlineKeyboardButton(f'{ej.DENY1_EMOJI}', callback_data='DELETE-NO')]
    for button in buttons:
        markup.add(button)
    return markup


def back_markup(text=f'{ej.HOME_EMOJI} Главная'):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text, callback_data='main_menu'))
    return markup


def popular_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    questions = [types.KeyboardButton('Институт'), types.KeyboardButton('Специальности'),
                 types.KeyboardButton('Поступление'), types.KeyboardButton('Документы для поступления'),
                 types.KeyboardButton('Общежитие')]
    markup.add(*questions, row_width=2)
    return markup


def question_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(f'{ej.WRITE_EMOJI} Написать вопрос ПК', callback_data='new_question'))
    return markup


def number_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(f'{ej.TEL_EMOJI} Предоставить номер телефона', request_contact=True))
    return markup


def nation_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton('🇷🇺 РФ'),
               types.KeyboardButton('🇰🇿 РК'))
    return markup


def no_markup():
    markup = types.ReplyKeyboardRemove()
    return markup
