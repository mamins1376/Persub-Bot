#! coding: utf-8

import telegram


class Command:

  def __init__(self, bot, message):
    chat_id = message.chat_id

    text = 'Command me! see /help'

    bot.sendMessage(chat_id, text)
