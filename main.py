#!/usr/bin/env python3
#! coding: utf-8

import zipfile
import os
import shutil
import sys
import uuid
import logging
import getopt
import urllib.request
import telegram

subscene_dir = os.path.abspath('lib/subscene-api')
sys.path.append(subscene_dir)
from subscene import Subscene

class PersubBot:

  def __init__(self):
    self.LAST_UPDATE_ID = None

    self.token = self.get_token()
    self.bot = telegram.Bot(token=self.token)

    try:
      self.LAST_UPDATE_ID = self.bot.getUpdates()[-1].update_id
    except IndexError:
      self.LAST_UPDATE_ID = None
    logging.debug('last update_id: {}'.format(self.LAST_UPDATE_ID))

    while True:
      updates = self.bot.getUpdates(offset=self.LAST_UPDATE_ID, timeout=10)
      for update in updates:
        chat_id = update.message.chat_id
        message = update.message.text
        self.send_subtitle(chat_id, message)
        self.LAST_UPDATE_ID = update.update_id + 1

  def get_token(self):
    logging.debug('Getting bot token from token.txt')
    token_file = open('token.txt')
    token = token_file.read().split('\n')[0]
    token_file.close()
    return token

  def send_subtitle(self, chat_id, term):
    logging.debug('searching for: {}'.format(term))

    try:
      film = Subscene().Search(term)
    except Exception as error:
      logging.error('error while searching: {}'.format(error))
      self.bot.sendMessage(chat_id, 'فیلم پیدا نشد.')
      return

    if film is None:
        self.bot.sendMessage(chat_id, 'فیلم پیدا نشد.')
        return

    subtitle_link = ''
    for subtitle in film.subtitles:
      if 'Persian' in subtitle.language:
        subtitle.getZipLink()
        subtitle_link = subtitle.zipped
        break

    if subtitle_link is '':
      logging.debug('no Persian subtitle found for {}'.format(term))
      self.bot.sendMessage(chat_id, 'این فیلم زیرنویس پارسی ندارد.')
      return

    logging.debug('subtitle download link is: {}'.format(subtitle_link))

    directory = str(uuid.uuid4()) + '.temp'
    os.mkdir(directory)
    logging.debug('{} directory created.'.format(directory))

    zipped_subtitle_path = directory + '/subtitle.zip'

    self.download(subtitle_link, zipped_subtitle_path)

    self.unzip(zipped_subtitle_path, directory)

    subtitle_path = self.find_srt(directory)

    self.bot.sendChatAction(chat_id, telegram.ChatAction.UPLOAD_DOCUMENT)
    self.bot.sendDocument(chat_id, document=open(subtitle_path, 'rb'))

    shutil.rmtree(directory, ignore_errors=True)

  def download(self, url, filename):
    zipped_subtitle = open(filename, 'wb')
    logging.debug('downloading: {}'.format(url))
    data = urllib.request.urlopen(url).read()
    zipped_subtitle.write(data)
    zipped_subtitle.close()
    logging.debug('download completed: {}'.format(filename))

  def unzip(self, zipped, directory):
    zipfile.ZipFile(zipped).extractall(directory)
    logging.debug('archive unzipped')

  def find_srt(self, directory):
    files = os.listdir(directory)
    srt_path = None
    for file in files:
      if file.endswith('.srt'):
        srt_path = directory + '/' + file
        logging.debug('subtitle found: {}'.format(srt_path))
        break
    if srt_path is None:
      logging.warning('no subtitle found in {} directory'.format(directory))
    return srt_path

if __name__ == '__main__':
  argv = sys.argv[1:]
  LOG_FILE = 'messages.log'
  LOG_LEVEL = 'warning'

  opts, args = getopt.getopt(
    argv, 'f:hl:', ['log-file=', 'help', 'log-level='])

  for opt, arg in opts:
    if opt == '-h':
      print('main.py -f <LOG_FILE> -l <LOG_LEVEL>')
      sys.exit()
    elif opt in ("-f", "--log-file"):
      LOG_FILE = arg
    elif opt in ("-l", "--log-level"):
      LOG_LEVEL = arg

  logging.basicConfig(
      format='%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s',
      filename=LOG_FILE,
      level=LOG_LEVEL.upper())

  logging.debug('starting')
  PersubBot()
