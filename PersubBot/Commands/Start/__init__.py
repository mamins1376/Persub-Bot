#! coding: utf-8

import telegram


class Command:

  def __init__(self, bot, message):
    chat_id = message.chat_id

    bot.sendMessage(chat_id, 'Hi!')
    bot.sendMessage(chat_id, 'this bot is under heavy development right now.')
    bot.sendMessage(chat_id, 'see you soon :D')
