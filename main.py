#!/usr/bin/env python3
#! coding: utf-8

import subscene_api, zipfile, os, telegram, time, shutil
import urllib.request as urllib
from uuid import uuid4 as random

class PersubBot:
    def getUpdates(self):
        while True:
            print('Checking for Updates... ', end='')
            update_id = self.last_update_id + 1
            updates = self.bot.getUpdates(offset=update_id)
            if len(updates) == 0:
                print('No New Messages.')
                time.sleep(10)
                continue
            print('New Message Found!')
            for update in updates:
                chat_id = update.message.chat_id
                message = update.message.text
                self.send_subtitle(chat_id, message)
            self.last_update_id = updates[-1].update_id
            time.sleep(10)

    def send_subtitle(self, chat_id, title):
        self.bot.sendMessage(chat_id, text='دارم دنبالش می‌گردم')
        self.bot.sendMessage(chat_id, text='یه دیقه صبر کن...')
        self.bot.sendChatAction(chat_id, telegram.ChatAction.TYPING)
        print('Finding Subtitle for {}'.format(title))
        try:
            url = subscene_api.get_film_url(title)
            self.bot.sendMessage(chat_id, text='این لینک فیلم: ' + url)
        except ValueError:
            self.bot.sendMessage(chat_id, text='چیزی براش پیدا نشد.')
            self.bot.sendMessage(chat_id, text=telegram.Emoji.CRYING_FACE)
            return None
        subtitles = subscene_api.get_subtitles(url)
        sub_link = None
        for sub in subtitles:
            if 'Persian' in sub['language']:
                sub_link = sub['url']
                print('Subtitle found. Fetching...')
                self.bot.sendMessage(chat_id, text='پیدا شد!')
                self.bot.sendMessage(chat_id, text='الآن می‌فرستم')
                break
        if sub_link is None:
            self.bot.sendMessage(chat_id, text='چیزی براش پیدا نشد.')
            self.bot.sendMessage(chat_id, text=telegram.Emoji.CRYING_FACE)
            return None
        url = subscene_api.get_subtitle_download_link(sub_link)
        data = urllib.urlopen(url).read()
        print('subtitle Downloaded. sending...')
        directory = str(random())
        os.mkdir(directory)
        f = open(directory + '/subtitle.zip', 'wb')
        f.write(data)
        f.close()
        z = zipfile.ZipFile(directory + '/subtitle.zip')
        z.extractall(directory)
        os.remove(directory + '/subtitle.zip')
        files = os.listdir(directory)
        for file in files:
            if file.endswith('.srt'):
                subtitle_path = directory + '/' + file
                break
        self.bot.sendChatAction(chat_id, telegram.ChatAction.UPLOAD_DOCUMENT)
        self.bot.sendDocument(chat_id, document=open(subtitle_path, 'rb'))
        shutil.rmtree(directory, ignore_errors=True)
        print('sending complated.\n')

    def __init__(self):
        with open('token.txt') as token_file:
            bot_token = token_file.read().split('\n')[0]
            print(bot_token)
        self.bot = telegram.Bot(token=bot_token)
        self.last_update_id = 0
        self.getUpdates()

if __name__ == '__main__':
    PersubBot()
