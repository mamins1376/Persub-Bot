#! coding: utf-8

import telegram


class Command:

  def __init__(self, bot, message):
    chat_id = message.chat_id

    bot.sendMessage(chat_id, "Hi!\nto get a list of commands, use /help.")
