from pyrogram import errors

from global_vars import app, users, queue_users
import lib.screen as screen


def is_member(chat_id, user_id):
    # print('🔥')
    # print(chat_id, user_id)
    # print(type(chat_id), type(user_id))
    # print('🔥')

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


def is_queue_user(user_id):
    if user_id in queue_users:
        return True
    return False


def is_user_in_queue_or_cabinet(user_id):
    if not is_queue_user(user_id):
        return False

    queue_user = queue_users[user_id]
    if not queue_user["in"]:
        return False

    return queue_user["in"]["type"]


def check_if_banned_before_money(user_id, text="💸"):
    # если он меня забанил — то я его тоже 🔫🔫🔫
    try:
        screen.create(app, user_id, screen.money_hidden_block_check(text))
        return True
    except (
        errors.exceptions.bad_request_400.UserIsBlocked,
        errors.exceptions.bad_request_400.InputUserDeactivated,
        errors.exceptions.bad_request_400.PeerIdInvalid
    ) as e:
        print(f"{user_id} IS BLOCKED ME or something wtf: {e}")
        users[user_id]["loyalty_program"]["subscribed_since"] = None
        return False


emojies_special = ["👤", "🧌", "🧟‍♀️", "🧟", "🧟‍♂️", "🧞‍♀️", "🧞", "🧞‍♂️"]
emojies_uncolored = [
    '👶', '👧', '🧒', '👦', '👩', '🧑', '👨', '👩\u200d🦱', '🧑\u200d🦱', '👨\u200d🦱', '👩\u200d🦰',
    '🧑\u200d🦰', '👨\u200d🦰', '👱\u200d♀️', '👱', '👱\u200d♂️', '👩\u200d🦳', '🧑\u200d🦳', '👨\u200d🦳',
    '👩\u200d🦲', '🧑\u200d🦲', '👨\u200d🦲', '🧔\u200d♀️', '🧔', '🧔\u200d♂️', '👵', '🧓', '👴', '👲',
    '👳\u200d♀️', '👳', '👳\u200d♂️', '🧕', '👮\u200d♀️', '👮', '👮\u200d♂️', '👷\u200d♀️', '👷', '👷\u200d♂️',
    '💂\u200d♀️', '💂', '💂\u200d♂️', '🕵️\u200d♀️', '🕵️', '🕵️\u200d♂️', '👩\u200d⚕️', '🧑\u200d⚕️',
    '👨\u200d⚕️', '👩\u200d🌾', '🧑\u200d🌾', '👨\u200d🌾', '👩\u200d🍳', '🧑\u200d🍳', '👨\u200d🍳',
    '👩\u200d🎓', '🧑\u200d🎓', '👨\u200d🎓', '👩\u200d🎤', '🧑\u200d🎤', '👨\u200d🎤', '👩\u200d🏫',
    '🧑\u200d🏫', '👨\u200d🏫', '👩\u200d🏭', '🧑\u200d🏭', '👨\u200d🏭', '👩\u200d💻', '🧑\u200d💻',
    '👨\u200d💻', '👩\u200d💼', '🧑\u200d💼', '👨\u200d💼', '👩\u200d🔧', '🧑\u200d🔧', '👨\u200d🔧',
    '👩\u200d🔬', '🧑\u200d🔬', '👨\u200d🔬', '👩\u200d🎨', '🧑\u200d🎨', '👨\u200d🎨', '👩\u200d🚒',
    '🧑\u200d🚒', '👨\u200d🚒', '👩\u200d✈️', '🧑\u200d✈️', '👨\u200d✈️', '👩\u200d🚀', '🧑\u200d🚀',
    '👨\u200d🚀', '👩\u200d⚖️', '🧑\u200d⚖️', '👨\u200d⚖️', '👰\u200d♀️', '👰', '👰\u200d♂️', '🤵\u200d♀️',
    '🤵', '🤵\u200d♂️', '👸', '\U0001fac5', '🤴', '🥷', '🦸\u200d♀️', '🦸', '🦸\u200d♂️', '🦹\u200d♀️',
    '🦹', '🦹\u200d♂️', '🤶', '🧑\u200d🎄', '🎅', '🧙\u200d♀️', '🧙', '🧙\u200d♂️', '🧝\u200d♀️', '🧝',
    '🧝\u200d♂️', '🧛\u200d♀️', '🧛', '🧛\u200d♂️', '🧜\u200d♀️', '🧜', '🧜\u200d♂️', '🧚\u200d♀️', '🧚',
    '🧚\u200d♂️', '👼', '🤰', '\U0001fac4', '\U0001fac3', '🤱', '👩\u200d🍼', '🧑\u200d🍼', '👨\u200d🍼',
    '🙇\u200d♀️', '🙇', '🙇\u200d♂️', '💁\u200d♀️', '💁', '💁\u200d♂️', '🙅\u200d♀️', '🙅', '🙅\u200d♂️',
    '🙆\u200d♀️', '🙆', '🙆\u200d♂️', '🙋\u200d♀️', '🙋', '🙋\u200d♂️', '🧏\u200d♀️', '🧏', '🧏\u200d♂️',
    '🤦\u200d♀️', '🤦', '🤦\u200d♂️', '🤷\u200d♀️', '🤷', '🤷\u200d♂️', '🙎\u200d♀️', '🙎', '🙎\u200d♂️',
    '🙍\u200d♀️', '🙍', '🙍\u200d♂️', '💇\u200d♀️', '💇', '💇\u200d♂️', '💆\u200d♀️', '💆', '💆\u200d♂️',
    '🧖\u200d♀️', '🧖', '🧖\u200d♂️'
]

colors = [
    "",
    "🏻",
    "🏼",
    "🏽",
    "🏾",
    "🏿"
]

emojies_avatars = emojies_special + sum(
    [[f"{emoji[0]}{color}{emoji[1:]}" for emoji in emojies_uncolored] for color in colors],
    []
)


def get_emoji_avatar(user_id):
    return emojies_avatars[user_id % len(emojies_avatars)]


def get_user_name(user):
    emoji_avatar = get_emoji_avatar(user.id)
    if user.username:
        out = user.username
    elif user.first_name:
        out = user.first_name
    else:
        out = str(user.id)
    return emoji_avatar + "`" + out[:10] + "`"
