#! coding: utf-8

import zipfile
import os
import shutil
import uuid
import logging
import urllib.request
import telegram

from subscene import Subscene


class Command:

  def __init__(self, bot, message):
    self.bot = bot
    text = message.text
    chat_id = message.chat_id

    if text == '':
      self.bot.sendMessage(chat_id, telegram.Emoji.NEUTRAL_FACE)
      return

    logging.debug('searching for: {}'.format(text))
    # 'Typing...'
    self.bot.sendChatAction(chat_id, telegram.ChatAction.TYPING)

    # find the film
    try:
      film = Subscene().Search(text)
    except Exception as error:
      logging.error('error while searching: {}'.format(error))
      self.bot.sendMessage(chat_id, 'فیلم پیدا نشد.')
      return

    # if no film found, give up
    if film is None:
      self.bot.sendMessage(chat_id, 'فیلم پیدا نشد.')
      return

    # if film has a cover, send it
    # if film.cover != '':
    #  self.send_film_cover(chat_id, film.cover)

    # choose a subtitle
    subtitle_link = ''
    for subtitle in film.subtitles:
      if 'Persian' in subtitle.language:
        subtitle.getZipLink()
        subtitle_link = subtitle.zipped
        break

    # if no suitable subtitle found, give up
    if subtitle_link is '':
      logging.debug('no Persian subtitle found for {}'.format(text))
      self.bot.sendMessage(chat_id, 'این فیلم زیرنویس پارسی ندارد.')
    else:
      self.send_subtitle(chat_id, subtitle_link)

  def send_film_cover(self, chat_id, cover_link):
    logging.debug('downloading cover')

    # 'Sending Photo...'
    self.bot.sendChatAction(chat_id, telegram.ChatAction.UPLOAD_PHOTO)

    photo_path = str(uuid.uuid4()) + '.jpg'

    self.download(cover_link, photo_path)

    self.bot.sendPhoto(chat_id, photo=open(photo_path, 'rb'))

    os.remove(photo_path)
    logging.debug('cover sent')

  def send_subtitle(self, chat_id, subtitle_link):
    logging.debug('subtitle download link is: {}'.format(subtitle_link))

    # create a directory for works
    directory = str(uuid.uuid4()) + '.temp'
    os.mkdir(directory)
    logging.debug('{} directory created.'.format(directory))

    zipped_subtitle_path = directory + '/subtitle.zip'

    self.download(subtitle_link, zipped_subtitle_path)

    self.unzip(zipped_subtitle_path, directory)

    subtitle_path = self.find_srt(directory)

    self.bot.sendChatAction(chat_id, telegram.ChatAction.UPLOAD_DOCUMENT)
    self.bot.sendDocument(chat_id, document=open(subtitle_path, 'rb'))

    # remove directory
    shutil.rmtree(directory, ignore_errors=True)

  def download(self, url, filename):
    # download <url> and write it to <filename>
    zipped_subtitle = open(filename, 'wb')
    logging.debug('downloading: {}'.format(url))
    data = urllib.request.urlopen(url).read()
    zipped_subtitle.write(data)
    zipped_subtitle.close()
    logging.debug('download completed: {}'.format(filename))

  def unzip(self, zipped, directory):
    # unzip <zipped> file to <directory>
    zipfile.ZipFile(zipped).extractall(directory)
    logging.debug('archive unzipped')

  def find_srt(self, directory):
    # find any '.srt' file in <directory>

    # get list
    files = os.listdir(directory)
    srt_path = None
    for file in files:
      if file.endswith('.srt'):
        srt_path = directory + '/' + file
        logging.debug('subtitle found: {}'.format(srt_path))
        break

    # if no '.srt' file found...
    if srt_path is None:
      logging.warning('no subtitle found in {} directory'.format(directory))

    return srt_path
