# import server.server_vars
from datetime import datetime, timezone

# import lib.screen as screen


def now():
    return datetime.now(timezone.utc)


def now_text():
    return now().strftime('%T')


def timestamp():
    return now().timestamp()


def timestamp_to_datetime(timestamp):
    return datetime.fromtimestamp(timestamp, timezone.utc).strftime('%F %T.%f')


def seconds_from_timestamp(timestamp):
    return (now() - datetime.fromtimestamp(timestamp, timezone.utc)).total_seconds()


def random_datetime(up_timedelta):
    from random import random
    return datetime.now(timezone.utc)+up_timedelta*random()


def sanitize_comment_message(message):
    if message.text:
        message_text = message.text
    elif message.caption:
        message_text = message.caption
    else:
        return ""

    if message_text == "":
        return ""

    # удаляем плохие символы, что могут сломать разметку
    message_text = ''.join(i for i in message_text if i not in r'\`*_|~')
    # обрезаем коммент до приемлимых 30 символов
    message_text = message_text[:30]
    # наклоним италиком
    message_text = "__"+message_text+"__"
    return message_text


def emoji_fingerprint():
    from random import choice
    emoji_list = [
        '💟', '☮️', '✝️', '☪️', '🕉', '☸️', '✡️', '🔯', '🕎',
        '☯️', '☦️', '🛐', '⛎', '♈️', '♉️', '♊️', '♋️',
        '♌️', '♍️', '♎️', '♏️', '♐️', '♑️', '♒️', '♓️',
        '🆔', '⚛️', '📴', '📳', '🈶', '🈚️', '🈸', '🈺',
        '🈷️', '✴️', '🆚', '🈴', '🈵', '🈹', '🈲', '🅰️',
        '🅱️', '🆎', '🆑', '🅾️', '🆘']

    return choice(emoji_list)
