#! coding: utf-8

import telegram


class Command:

  def __init__(self, bot, message):
    chat_id = message.chat_id

    text = '''About Persub Bot
Author: Mohammad Amin Sameti (@mamins1376)
Source Code on GitHub: https://github.com/mamins1376/Persub-Bot

The goal of Persub Bot is giving the user the best subtitles available for a movie or a tv show.
uses the python telegram bot api (see https://github.com/leandrotoledo/python-telegram-bot).

tell me your feedbacks! ;)'''

    bot.sendMessage(chat_id, text)
