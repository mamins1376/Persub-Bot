#! coding: utf-8

import telegram


class Command:

  def __init__(self, bot, message):
    chat_id = message.chat_id

    text = '''Available Commands:
/start - Start using Persub Bot
/sub <Title> - Find a subtitle for <Title> (e.g. /sub Mr. Robot S01E05)
/about - About this bot
/help - Show this help'''

    bot.sendMessage(chat_id, text)
