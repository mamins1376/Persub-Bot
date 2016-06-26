#! coding: utf-8

import persubbot
import persubbot.database

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
      bot.sendMessage(chat_id, 'Usage: /lang <YOUR LANGUAGE>')
      return

    language = ''

    for lang in self.LANGUAGES_LOOKUP.keys():
      if lang in text.lower():
        language = self.LANGUAGES_LOOKUP[lang]

    if language == '':
      bot.sendMessage(
        chat_id, 'I can\'t find {} subtitles. sorry'.format(text))
      return

    persubbot.database.set_user_language(user_id, language)

    bot.sendMessage(
        chat_id, 'I\'ll give you subtitles in {} from now.'.format(text))
