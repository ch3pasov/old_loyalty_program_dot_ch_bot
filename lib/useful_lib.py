# import server.server_vars
from datetime import datetime, timezone

from pyrogram import errors

# import lib.screen as screen


def is_member(app, chat_id, user_id):
    try:
        is_member = app.get_chat_member(chat_id, user_id).is_member
        if is_member is None:
            return True
        else:
            return is_member
    except errors.exceptions.bad_request_400.UserNotParticipant:
        return False


def is_registered(user_id, users):
    if user_id not in users:
        return False
    if users[user_id]["loyality_programm"]["subscribed_since"] is None:
        return False
    return True


def timestamp():
    return datetime.now().timestamp()


def timestamp_to_datetime(timestamp):
    return datetime.fromtimestamp(timestamp, timezone.utc).strftime('%Y-%m-%d %H:%M')


def seconds_from_timestamp(timestamp):
    return (datetime.now() - datetime.fromtimestamp(timestamp)).total_seconds()


def random_datetime(up_timedelta):
    from random import random
    return datetime.now(timezone.utc)+up_timedelta*random()
