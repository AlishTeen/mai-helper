from bot_app import bot, logger

if __name__ == '__main__':
    logger.info('Started!')
    bot.infinity_polling()


