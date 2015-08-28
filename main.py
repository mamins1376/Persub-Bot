#!/usr/bin/env python3
#! coding: utf-8

import zipfile
import os
import shutil
import uuid
import urllib.request
import subtitle
import telegram
import logging
import sys
import getopt


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

  def send_subtitle(self, chat_id, title):
    try:
      url = subtitle.get_film_url(title)
    except ValueError:
      return
    subtitles = subtitle.get_subtitles(url)
    sub_link = None
    for sub in subtitles:
      if 'Persian' in sub['language']:
        sub_link = sub['url']
        break
    if sub_link is None:
      return

    url = subtigle.get_subtitle_download_link(sub_link)
    logging.debug('subtitle download link is: {}'.format(url))

    directory = str(uuid.uuid4()) + '.temp'
    os.mkdir(directory)
    logging.debug('{} directory created.'.format(directory))

    zipped_subtitle_path = directory + '/subtitle.zip'

    self.download(url, zipped_subtitle_path)

    self.unzip(zipped_subtitle_path, directory)

    subtitle_path = self.find_srt(directory)

    self.bot.sendChatAction(chat_id, telegram.ChatAction.UPLOAD_DOCUMENT)
    self.bot.sendDocument(chat_id, document=open(subtitle_path, 'rb'))

    shutil.rmtree(directory, ignore_errors=True)

  def download(self, url, filename):
    zipped_subtitle = open(filename, 'wb')
    data = urllib.request.urlopen(url).read()
    zipped_subtitle.write(data)
    zipped_subtitle.close()
    logging.debug('download completed')

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
