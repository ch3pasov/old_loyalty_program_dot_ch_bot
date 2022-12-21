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
