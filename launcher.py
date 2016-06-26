#!/usr/bin/env python3
#! coding: utf-8

import sys
import os
import logging
import getopt

from persubbot import PersubBot


def get_token(token_path):
  # get the bot's token from token.txt
  logging.debug('Reading bot token')
  token_file = open(token_path)
  token = token_file.read().split('\n')[0]
  token_file.close()
  return token

if __name__ == '__main__':
  # read args from command line
  argv = sys.argv[1:]
  LOG_FILE = 'messages.log'
  LOG_LEVEL = 'warning'
  LOOP_MODE = False
  TOKEN_FILE = 'token.txt'
  TOKEN_CODE = None

  opts, args = getopt.getopt(
      argv, 'f:hl:Lt:T:', ['log-file=', 'help', 'log-level=', 'loop', 'token=', 'token-file='])

  HELP_MESSAGE = '''
Usage: launcher.py [OPTION]...
Persub Bot Launcher Script

  -h, --help                 Show this message

  -f, --log-file <FILE>      Set the log file path. default: messages.log
  -l, --log-level <LEVEL>    Set the log level. default: warning
  -L, --loop                 Enable loop mode. default: no

  -t, --token <TOKEN>        Set the bot token directly
  -T, --token-file <FILE>    Set the token file path. default: token.txt

'''

  # process arguments
  for opt, arg in opts:
    if opt in ("-h","--help"):
      print(HELP_MESSAGE)
      sys.exit()
    elif opt in ("-f", "--log-file"):
      LOG_FILE = arg
    elif opt in ("-l", "--log-level"):
      LOG_LEVEL = arg
    elif opt in ("-L", "--loop"):
      LOOP_MODE = True
    elif opt in ("-t", "--token"):
      TOKEN_CODE = arg
    elif opt in ("-T", "--token-file"):
      TOKEN_FILE = arg


  # config logging parameters
  logging.basicConfig(
      format='%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s',
      filename=LOG_FILE,
      level=LOG_LEVEL.upper())

  logging.debug('Starting')

  if TOKEN_CODE is None:
    token = get_token(TOKEN_FILE)
  else:
    token = TOKEN_CODE

  # wake up!
  while True:
    try:
      PersubBot(token)
    except KeyboardInterrupt:
      logging.info('exiting (KeyboardInterrupt)')
      break
    except Exception as error:
      logging.exception('launcher level exception')

    if not LOOP_MODE:
      break
