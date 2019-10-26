# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler
import requests
import re
import random
from datetime import datetime
import configparser

fortunes = []
daily_fortunes = {}

last_date = None

def get_daily_fortune(bot, update):
    global last_date
    global fortunes

    date = datetime.today().date()
    if last_date is None or last_date != date:
        print("Date = %s, last_date = %s, clearing fortunes" % (date, last_date))
        daily_fortunes.clear()

    last_date = date

    user = update.message.from_user.username
    if user is None:
        update.message.reply_text("Чтобы получить совет на сегодня, установите username в Telegram.",
                                  quote=True)
    else:
        is_new = False

        fortune = daily_fortunes.get(user)
        if not fortune:
            fortune = random.choice(fortunes)
            daily_fortunes[user] = fortune
            is_new = True

        print("Selected fortune \"%s\" for %s at %s" % (fortune,
                                                        update.message.from_user.username,
                                                        date))

        if is_new:
            message = "Совет для вас на сегодня: \"%s\"" % fortune
        else:
            message = "Совет для вас на сегодня остается прежним: \"%s\"" % fortune

        update.message.reply_text(message, quote=True)

def main():
    config = configparser.ConfigParser()
    config.read('.config')

    token = config['main-config']['token']

    f = open('.fortunes', 'r')
    lines = f.readlines()
    f.close()

    for l in lines:
        fortunes.append(l.strip('\n'))

    updater = Updater(token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('daily_fortune', get_daily_fortune))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
