#!/usr/bin/env python3
#! coding: utf-8

import zipfile
import os
import shutil
import uuid
import urllib.request
import subtitle_api
import telegram
import logging


class PersubBot:

  def __init__(self):
    self.LAST_UPDATE_ID = None

    logging.basicConfig(
        format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename = 'messages.log',
        level = logging.DEBUG)

    self.token = self.get_token()
    self.bot = telegram.Bot(token = self.token)

    try:
      self.LAST_UPDATE_ID = self.bot.getUpdates()[-1].update_id
    except IndexError:
      self.LAST_UPDATE_ID = None

    while True:
      updates = self.bot.getUpdates(offset = self.LAST_UPDATE_ID, timeout = 10)
      for update in updates:
        chat_id = update.message.chat_id
        message = update.message.text
        self.send_subtitle(chat_id, message)
        self.LAST_UPDATE_ID = update.update_id + 1

  def get_token(self):
    token_file = open('token.txt')
    token = token_file.read().split('\n')[0]
    token_file.close()
    return token

  def send_subtitle(self, chat_id, title):
    try:
      url = subtitle_api.get_film_url(title)
    except ValueError:
      return
    subtitles = subtitle_api.get_subtitles(url)
    sub_link = None
    for sub in subtitles:
      if 'Persian' in sub['language']:
        sub_link = sub['url']
        break
    if sub_link is None:
      return

    url = subtitle_api.get_subtitle_download_link(sub_link)

    directory = str(uuid.uuid4()) + '.temp'
    os.mkdir(directory)

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

  def unzip(self, zipped, directory):
    zipfile.ZipFile(zipped).extractall(directory)

  def find_srt(self, directory):
    files = os.listdir(directory)
    for file in files:
      if file.endswith('.srt'):
        srt_path = directory + '/' + file
        break
    return srt_path

if __name__ == '__main__':
  PersubBot()
