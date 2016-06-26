#! coding: utf-8

import logging
import telegram

import persubbot.commands.start
import persubbot.commands.sub
import persubbot.commands.helpp # 'help' is a built-in function
import persubbot.commands.about
import persubbot.commands.language
import persubbot.commands.talk

COMMANDS_LOOKUP = {
  'START': persubbot.commands.start,
  'SUB': persubbot.commands.sub,
  'HELP': persubbot.commands.helpp,
  'ABOUT': persubbot.commands.about,
  'LANG': persubbot.commands.language,
  'TALK': persubbot.commands.talk
}

class PersubBot:

  def __init__(self, token):
    self.LAST_UPDATE_ID = None
    self.bot = telegram.Bot(token=token)

    try:
      self.LAST_UPDATE_ID = self.bot.getUpdates()[-1].update_id
    except IndexError:
      self.LAST_UPDATE_ID = None

    while True:
      updates = self.bot.getUpdates(offset=self.LAST_UPDATE_ID, timeout=10)
      for update in updates:
        self.reply(update.message)
        self.LAST_UPDATE_ID = update.update_id + 1

  def reply(self, message):
    # detect message type
    if not (message.text is None):
      self.reply_text(message)
    elif not (message.audio is None):
      self.reply_audio(message)
    elif not (message.document is None):
      self.reply_document(message)
    elif not (message.photo is None):
      self.reply_photo(message)
    elif not (message.sticker is None):
      self.reply_sticker(message)
    elif not (message.video is None):
      self.reply_video(message)
    elif not (message.voice is None):
      self.reply_voice(message)
    elif not (message.caption is None):
      self.reply_caption(message)
    elif not (message.contact is None):
      self.reply_contact(message)
    elif not (message.location is None):
      self.reply_location(message)
    else:
      logging.warning('New message had no usable content!')

  def reply_text(self, message):
    logging.debug('Replying to a text message')
    # clear text
    text = message.text.strip()

    # if this is a command, run it; else say something to user
    if text.startswith('/') and text != '/':
      text = text[1:]  # remove '/'
      command = text.split(' ')[0]
      arguments = text[len(command) + 1:]
    else:
      command = 'talk'
      arguments = text

    command = command.upper()
    message.text = arguments

    logging.debug('Command: {}'.format(command))
    logging.debug('Arguments: {}'.format(arguments))

    try:
      result = COMMANDS_LOOKUP[command].Command(self.bot, message)
    except KeyError:
      self.bot.sendMessage(message.chat_id, 'Unknown command. see /help')
      logging.info('Undefined command called: {}'.format(command))

  def reply_audio(self, message):
    logging.debug('Replying to an audio')

  def reply_document(self, message):
    logging.debug('Replying to a document')

  def reply_photo(self, message):
    logging.debug('Replying to a photo')

  def reply_sticker(self, message):
    logging.debug('Replying to a sticker')

  def reply_video(self, message):
    logging.debug('Replying to a video')

  def reply_voice(self, message):
    logging.debug('Replying to a voice')

  def reply_caption(self, message):
    logging.debug('Replying to a caption')

  def reply_contact(self, message):
    logging.debug('Replying to a contact')

  def reply_location(self, message):
    logging.debug('Replying to a location')
