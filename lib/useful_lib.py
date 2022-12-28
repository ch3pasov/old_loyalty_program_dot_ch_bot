# import server.server_vars
from datetime import datetime, timezone, timedelta

# import lib.screen as screen


def now():
    return datetime.now(timezone.utc)


def dt_plus_n_minutes(dt, n):
    return dt + timedelta(minutes=n)


def now_plus_n_minutes(n):
    return dt_plus_n_minutes(datetime.now(timezone.utc), n)


def datetime_to_text(dt):
    return dt.strftime('%T')


def now_text():
    return datetime_to_text(now())


def timestamp_now():
    return now().timestamp()


def timestamp_to_datetime(timestamp):
    return datetime.fromtimestamp(timestamp, timezone.utc)


def timestamp_to_datetime_text_long(timestamp):
    return timestamp_to_datetime(timestamp).strftime('%F %T.%f')


def timestamp_to_time_text(timestamp):
    return datetime_to_text(datetime.fromtimestamp(timestamp, timezone.utc))


def seconds_between_timestamps(timestamp_after, timestamp_before):
    return (datetime.fromtimestamp(timestamp_after) - datetime.fromtimestamp(timestamp_before)).total_seconds()


def seconds_from_timestamp(timestamp):
    return seconds_between_timestamps(timestamp_now(), timestamp)
    # return (now() - datetime.fromtimestamp(timestamp, timezone.utc)).total_seconds()


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
    message_text = ''.join((i if i not in r'\`/*_|~@.' else '') for i in message_text)
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
