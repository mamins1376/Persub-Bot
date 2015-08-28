#! coding: utf-8
from bs4 import BeautifulSoup
import urllib.request as urllib
import re
import logging

SITE_DOMAIN = 'http://bbsub.ir'


def get_soup(url):
  html_doc = urllib.urlopen(url).read().decode("utf-8")
  soup = BeautifulSoup(html_doc, 'html.parser')
  logging.debug('soup object created for: {}'.format(url))
  return soup


def get_film_url(title):
  logging.debug('searching for {}'.format(title))
  title = title.replace(' ', '+')
  url = "{}/subtitles/title?q={}&l=".format(SITE_DOMAIN, title)
  soup = get_soup(url)
  exact_tag = soup.find(name='h2', text='Exact')
  if exact_tag is None:
    raise ValueError('Film Not Found in Database.')
    return None
  relative_url = exact_tag.find_next('a', href=True)['href']
  absolute_url = SITE_DOMAIN + relative_url
  return absolute_url


def get_subtitles(film_url):
  logging.debug('getting subtitles')
  soup = get_soup(film_url)
  subtitles_table = soup.find('div', 'content clearfix').table
  subtitles = []
  for tr in subtitles_table.find_all('tr'):
    if tr.td.a is None:
      continue

    subtitle = {}
    language = tr.find('td', 'a1').a.find_all('span')[0].text
    subtitle['language'] = re.sub(r'\s+', '', language)
    film_filename = tr.find('td', 'a1').a.find_all('span')[1].text
    subtitle['film_filename'] = film_filename
    url = SITE_DOMAIN + tr.find('td', 'a1').a['href']
    subtitle['url'] = url
    translator = {}
    translator_username = tr.find('td', 'a5').a.text
    translator['username'] = re.sub(r'\s+', '', translator_username)
    translator_url = tr.find('td', 'a5').a['href']
    translator['page_url'] = SITE_DOMAIN + translator_url
    subtitle['translator'] = translator
    description = tr.find('td', 'a6').div.text
    subtitle['description'] = description
    subtitles.append(subtitle)
  logging.debug('{} subtitles found'.format(len(subtitles)))
  return tuple(subtitles)


def get_subtitle_download_link(subtitle_url):
  logging.debug('extracting download link')
  soup = get_soup(subtitle_url)
  download_url = SITE_DOMAIN + soup.find('div', 'download').a['href']
  return download_url
