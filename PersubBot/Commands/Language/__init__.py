#! coding: utf-8

import PersubBot
import PersubBot.DataBase

class Command:

  LANGUAGES_LOOKUP = {
      'persian': 'Persian', 'farsi': 'Persian', 'فارسی': 'Persian',
      'arabic': 'Arabic', 'عربی': 'Arabic', 'عربي': 'Arabic',
      'english': 'English',
  }

  def __init__(self, bot, message):
    chat_id = message.chat_id
    text = message.text
    user_id = message.from_user.id

    if text == '':
      bot.sendMessage(chat_id, 'Usage: /language <YOUR LANGUAGE>')
      return

    language = ''
    table = PersubBot.Commands.Language.Command.LANGUAGES_LOOKUP

    for lang in table:
      if lang in text.lower():
        language = table[lang]

    if language == '':
      bot.sendMessage(
        chat_id, 'I can\'t find {} subtitles. sorry'.format(text))
      return

    PersubBot.DataBase.set_user_language(user_id, language)

    bot.sendMessage(
        chat_id, 'I\'ll give you subtitles in {} from now.'.format(text))
