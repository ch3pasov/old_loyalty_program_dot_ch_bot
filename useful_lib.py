from pyrogram import errors

import server.server_vars
from datetime import datetime, timezone

import screen


def is_member(app, chat_id, user_id):
    try:
        is_member = app.get_chat_member(chat_id, user_id).is_member
        if is_member is None:
            return True
        else:
            return is_member
    except errors.exceptions.bad_request_400.UserNotParticipant as e:
        # print(e)
        return False


def is_registered(user_id, users):
    if user_id not in users:
        return False
    if users[user_id]["loyality_programm"]["subscribed_since"] is None:
        return False
    return True


def send_money(app, app_human, amount, user_id):
    global users

    assert amount < 1, "МНОГО ДЕНЕГ"

    non_collision_amount = amount + int(user_id)%100000/10**10 

    r = app_human.get_inline_bot_results('@wallet', str(non_collision_amount))

    result = r.results[0]
    if "TON" in result.title and "BTC" not in result.title:
        app_human.send_inline_bot_result(server.server_vars.money_chat_id, r.query_id, result.id)
        app_human.send_message(server.server_vars.money_chat_id, f"отправил {amount} TON юзеру {user_id}")

        screen.create(app, user_id, screen.money(result.send_message))
    else:
        raise ValueError("BTC! СЛЕВА НАПРАВО")


def timestamp():
    return datetime.now().timestamp()

def timestamp_to_datetime(timestamp):
    return datetime.fromtimestamp(timestamp, timezone.utc).strftime('%Y-%m-%d %H:%M')

def seconds_from_timestamp(timestamp):
    return (datetime.now() - datetime.fromtimestamp(timestamp)).total_seconds()