#! coding: utf-8

import logging
import sqlite3
import os.path


class DataBase:

  DATABASE_FILENAME = 'languages.db'

  def get_user_language(user_id):
    logging.debug('Getting language for user {}'.format(user_id))

    PersubBot.DataBase.cdbidne()

    conn = sqlite3.connect(PersubBot.DataBase.DATABASE_FILENAME)
    cur = conn.cursor()
    query = 'SELECT language FROM languages WHERE user_id={}'
    query = query.format(user_id)

    try:
      result = cur.execute(query)
      language = result.fetchall()[-1][0]
      logging.debug('user language found: {}:{}'.format(user_id, language))
    except IndexError:
      language = ''
      logging.debug('No language data found for user: {}'.format(user_id))
    except Exception as error:
      language = None
      error_type = str(type(error)).split('\'')[-2]
      logging.error('{} during reading database: {}'.format(error_type, error))
    finally:
      conn.close()

    return language

  def set_user_language(user_id, language):
    logging.debug(
        'Setting language for user {} to {}'.format(user_id, language))

    PersubBot.DataBase.cdbidne()

    conn = sqlite3.connect(PersubBot.DataBase.DATABASE_FILENAME)
    cur = conn.cursor()
    query = "INSERT OR REPLACE INTO languages (user_id, language) VALUES ({},'{}')"
    query = query.format(user_id, language)
    success = True

    try:
      cur.execute(query)
      conn.commit()
      logging.debug('Language for user {} set to {}'.format(user_id, language))
    except Exception as error:
      success = False
      error_type = str(type(error)).split('\'')[-2]
      logging.error(
          '{} during writing to database: {}'.format(error_type, error))
    finally:
      conn.close()

    return success

  # create database if does not exist
  def cdbidne():
    if not os.path.isfile(PersubBot.DataBase.DATABASE_FILENAME):
      logging.debug('Database does not exist. creating.')
      conn = sqlite3.connect(DataBase.DATABASE_FILENAME)
      cur = conn.cursor()
      query = 'CREATE TABLE languages (user_id int, language text)'

      try:
        cur.execute(query)
        conn.commit()
      except Exception as error:
        error_type = str(type(error)).split('\'')[-2]
        logging.error(
            'Unable to create database due to {}: {}'.format(error_type, error))
      finally:
        conn.close()
