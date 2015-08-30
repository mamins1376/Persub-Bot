#!/usr/bin/env python3
#! coding: utf-8

import sys
import os
import logging
import getopt

sys.path.append(os.path.abspath('lib'))

from PersubBot import PersubBot


def get_token():
  # get the bot's token from token.txt
  logging.debug('Reading bot token')
  token_file = open('token.txt')
  token = token_file.read().split('\n')[0]
  token_file.close()
  return token

if __name__ == '__main__':
  # read args from command line
  argv = sys.argv[1:]
  LOG_FILE = 'messages.log'
  LOG_LEVEL = 'warning'

  opts, args = getopt.getopt(
      argv, 'f:hl:', ['log-file=', 'help', 'log-level='])

  # process arguments
  for opt, arg in opts:
    if opt == '-h':
      print('main.py -f <LOG_FILE> -l <LOG_LEVEL>')
      sys.exit()
    elif opt in ("-f", "--log-file"):
      LOG_FILE = arg
    elif opt in ("-l", "--log-level"):
      LOG_LEVEL = arg

  # config logging parameters
  logging.basicConfig(
      format='%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s',
      filename=LOG_FILE,
      level=LOG_LEVEL.upper())

  logging.debug('Starting')

  token = get_token()

  # wake up!
  try:
    PersubBot(token)
  except KeyboardInterrupt:
    logging.info('exiting (KeyboardInterrupt)')
    sys.exit()
