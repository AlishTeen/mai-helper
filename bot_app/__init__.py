import logging

import telebot
from telebot import apihelper

import config
from bot_app.database import DataBaseClass
from bot_app.dialogflow import DialogflowClass

logger = logging.getLogger('MaiBot')
logger.level = logging.DEBUG
logger.addHandler(logging.StreamHandler())

apihelper.ENABLE_MIDDLEWARE = True
bot = telebot.TeleBot(config.TOKEN, threaded=True)
db = DataBaseClass(**config.DB_CREDENTIALS)
df = DialogflowClass(config.GOOGLE_APP_CREDENTIALS)

temp_user_data = {}

from bot_app import handlers
