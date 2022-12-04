import global_vars
from global_vars import print
import lib.screen as screen
import server.server_vars
from lib.useful_lib import is_member, is_registered, seconds_from_timestamp, timestamp
from lib.dataclasses import LoyaltyLevel
from lib.money import send_money
from pyrogram import filters

users = global_vars.users
print(f"Я запустил interface и смотрю на users. Его id {id(users)}")
app_human = global_vars.app_human
app = global_vars.app


@app.on_message(filters.command(["start"]) & filters.private)
def my_handler(client, message):
    user_id = str(message.from_user.id)

    if is_registered(user_id, users):
        screen.create(client, message.chat.id, screen.home_exist(user_id))
    else:
        screen.create(client, message.chat.id, screen.home_new())


@app.on_callback_query(filters.regex('to_schema'))
def answer_schema(client, callback_query):
    screen.update(client, callback_query.message.chat.id, callback_query.message.id, screen.loyality_schema())


@app.on_callback_query(filters.regex('to_home'))
def answer_home(client, callback_query):
    user_id = str(callback_query.from_user.id)

    if is_registered(user_id, users):
        screen.update(client, callback_query.message.chat.id, callback_query.message.id, screen.home_exist(user_id))
    else:
        screen.update(client, callback_query.message.chat.id, callback_query.message.id, screen.home_new())


@app.on_callback_query(filters.regex('to_register'))
def answer_register(client, callback_query):
    global users

    screen.update(client, callback_query.message.chat.id, callback_query.message.id, screen.loading())
    user_id = str(callback_query.from_user.id)

    if is_registered(user_id, users):
        screen.update(client, callback_query.message.chat.id, callback_query.message.id, screen.register_already_register())
        return 0

    if not is_member(app, server.server_vars.dot_ch_id, user_id):
        screen.update(client, callback_query.message.chat.id, callback_query.message.id, screen.register_not_subscribed())
        return 0

    users.setdefault(
        user_id,
        {
            "registered_since": timestamp(),
            "loyalty_program": {
                "subscribed_since": None,
                "level": 0,
                "money_won": 0,
                "referer_id": None
            }
        }
    )
    users[user_id]["loyalty_program"]["subscribed_since"] = timestamp()
    # print(users[user_id])

    screen.update(client, callback_query.message.chat.id, callback_query.message.id, screen.register_successfully_emoji())

    # мгновенно выдать уровень, если норм
    user_line = users[user_id]["loyalty_program"]
    current_level = user_line["level"]
    schema_level: LoyaltyLevel = server.server_vars.loyalty_program[current_level]

    user_exp_days = seconds_from_timestamp(user_line["subscribed_since"])/86400
    level_need_days = schema_level.days
    if user_exp_days >= level_need_days:
        reward = schema_level.reward
        send_money(app, app_human, reward, user_id)
        users[user_id]["loyalty_program"]["level"] += 1
        users[user_id]["loyalty_program"]["money_won"] += reward
        screen.create(app, user_id, screen.level_up(
            congrats_text=schema_level.congrats_text,
            congrats_link=schema_level.congrats_link,
        ))

    screen.create(client, callback_query.message.chat.id, screen.register_successfully())


@app.on_callback_query(filters.regex('to_statistic'))
def answer(client, callback_query):
    screen.update(client, callback_query.message.chat.id, callback_query.message.id, screen.statistic())


@app.on_callback_query(filters.regex('to_profile'))
def answer_profile(client, callback_query):
    global users

    screen.update(client, callback_query.message.chat.id, callback_query.message.id, screen.loading())
    user_id = str(callback_query.from_user.id)
    screen.update(client, callback_query.message.chat.id, callback_query.message.id, screen.profile(user_id))


@app.on_chat_member_updated(group=server.server_vars.dot_ch_id)
def handler_channel_update(client, chat_member_updated):
    global users

    if not chat_member_updated.chat.id == server.server_vars.dot_ch_id:
        # действие происходит не в канале
        return
    if not chat_member_updated.old_chat_member:
        # это не отписка в канале
        return

    user_id = str(chat_member_updated.old_chat_member.user.id)
    if not is_registered(user_id, users):
        # отписавшийся от канала не в программе лояльности
        return

    users[user_id]["loyalty_program"]["subscribed_since"] = None
    screen.create(app, user_id, screen.unsubscribed_from_channel_gif())
    screen.create(app, user_id, screen.unsubscribed_from_channel())


# сообщения в личку
@app.on_message(filters.private & filters.text)
def answer_messages(client, message):
    screen.create(client, message.chat.id, screen.no_messages())


@app.on_message(filters.private & filters.voice)
def answer_voices(client, message):
    screen.create(client, message.chat.id, screen.no_voices())


@app.on_message(filters.private & filters.video_note)
def answer_video_notes(client, message):
    screen.create(client, message.chat.id, screen.no_video_notes())
