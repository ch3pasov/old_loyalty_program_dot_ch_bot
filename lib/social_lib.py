from pyrogram import errors

from global_vars import app, users
import lib.screen as screen


def is_member(chat_id, user_id):
    try:
        is_member = app.get_chat_member(chat_id, user_id).is_member
        if is_member is None:
            return True
        else:
            return is_member
    except (errors.exceptions.bad_request_400.UserNotParticipant, errors.exceptions.bad_request_400.PeerIdInvalid):
        return False


def is_registered(user_id):
    if user_id not in users:
        return False
    if users[user_id]["loyalty_program"]["subscribed_since"] is None:
        return False
    return True


def check_if_banned_before_money(user_id, text="💸"):
    # если он меня забанил — то я его тоже 🔫🔫🔫
    try:
        screen.create(app, user_id, screen.money_hidden_block_check(text))
        return True
    except (errors.exceptions.bad_request_400.UserIsBlocked, errors.exceptions.bad_request_400.InputUserDeactivated) as e:
        print(f"{user_id} IS BLOCKED ME or something wtf: {e}")
        users[user_id]["loyalty_program"]["subscribed_since"] = None
        return False
