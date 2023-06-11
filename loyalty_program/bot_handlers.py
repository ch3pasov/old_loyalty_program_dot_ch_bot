import global_vars
from global_vars import print, the_library
import lib.screen as screen
from lib.screen_library import screen_library
import server.server_vars
from lib.useful_lib import seconds_from_timestamp, timestamp_now
from lib.social_lib import is_member, is_registered
from lib.dataclasses_lib import LoyaltyLevel
from lib.money import send_money
from pyrogram import filters
import re

users = global_vars.users
user_referers = global_vars.user_referers

app_billing = global_vars.app_billing
app = global_vars.app


def start_bot_handlers():
    @app.on_message(filters.command(["start"]) & filters.private)
    async def my_handler(client, message):
        referer_id = None
        library_id = None
        if len(message.command) >= 2:
            command_text = message.command[1]
            re_search = re.search(r"^referer_id=(\d+)$", command_text)
            if re_search:
                referer_id = re_search.group(1)
            re_search = re.search(r"^to_library_id=([a-zA-Z\d_]+)$", command_text)
            if re_search:
                library_id = re_search.group(1)

        if library_id:
            if library_id in the_library:
                desired_screen = screen_library(library_id)
            else:
                desired_screen = screen.library_unknown()
            await screen.create(client, message.chat.id, desired_screen)
        elif referer_id:
            user_id = str(message.from_user.id)
            if is_registered(user_id):
                await screen.create(client, message.chat.id, screen.set_referer_confirm(referer_id=referer_id))
            else:
                await screen.create(client, message.chat.id, screen.lp_home_new())
                print(f"Незарегистрированный пользователь {user_id} зашёл по реферерке {referer_id}! Запомнил это.")
                user_referers[user_id] = referer_id
        else:
            await screen.create(client, message.chat.id, screen.home())

    @app.on_callback_query(filters.regex('to_home'))
    async def answer_home(client, callback_query):
        await screen.update(client, callback_query.message.chat.id, callback_query.message.id, screen.home())

    @app.on_callback_query(filters.regex('to_schema'))
    async def answer_schema(client, callback_query):
        user_id = str(callback_query.from_user.id)
        if user_id in users:
            user_level = users[user_id]['loyalty_program']['level']
        else:
            user_level = None
        await screen.update(client, callback_query.message.chat.id, callback_query.message.id, screen.schema(user_level))

    @app.on_callback_query(filters.regex('to_lp_home'))
    async def answer_lp_home(client, callback_query):
        user_id = str(callback_query.from_user.id)
        if is_registered(user_id):
            await screen.update(client, callback_query.message.chat.id, callback_query.message.id, screen.lp_home_exist(user_id))
        else:
            await screen.update(client, callback_query.message.chat.id, callback_query.message.id, screen.lp_home_new())

    @app.on_callback_query(filters.regex('to_register'))
    async def answer_register(client, callback_query):
        global users

        await screen.update(client, callback_query.message.chat.id, callback_query.message.id, screen.loading())
        user_id = str(callback_query.from_user.id)

        if is_registered(user_id):
            await screen.update(client, callback_query.message.chat.id, callback_query.message.id, screen.register_already_register())
            return 0

        if not is_member(server.server_vars.dot_ch_id, user_id):
            await screen.update(client, callback_query.message.chat.id, callback_query.message.id, screen.register_not_subscribed())
            return 0

        users.setdefault(
            user_id,
            {
                "registered_since": timestamp_now(),
                "loyalty_program": {
                    "subscribed_since": None,
                    "level": 0,
                    "money_won": 0,
                    "referer_id": None
                }
            }
        )
        users[user_id]["loyalty_program"]["subscribed_since"] = timestamp_now()
        print(f"Юзер {user_id} зарегистрировался!")

        await screen.update(client, callback_query.message.chat.id, callback_query.message.id, screen.congratulation_emoji())

        # мгновенно выдать уровень, если норм
        user_line = users[user_id]["loyalty_program"]
        current_level = user_line["level"]
        schema_level: LoyaltyLevel = server.server_vars.loyalty_program[current_level]

        user_exp_days = seconds_from_timestamp(user_line["subscribed_since"])/86400
        level_need_days = schema_level.days
        if user_exp_days >= level_need_days:
            await screen.create(client, user_id, screen.level_up(
                congrats_text=schema_level.congrats_text,
                congrats_link=schema_level.congrats_link,
            ))

            reward = schema_level.reward
            await send_money(reward, user_id, referer_enable=True)
            users[user_id]["loyalty_program"]["level"] += 1

        await screen.create(client, callback_query.message.chat.id, screen.register_successfully())
        if user_id in user_referers:
            await screen.create(client, callback_query.message.chat.id, screen.set_referer_confirm(referer_id=user_referers[user_id]))

    @app.on_callback_query(filters.regex('to_statistic'))
    async def answer_statistic(client, callback_query):
        await screen.update(client, callback_query.message.chat.id, callback_query.message.id, screen.statistic())

    @app.on_callback_query(filters.regex('to_referer_program'))
    async def answer_referer_program(client, callback_query):
        user_id = str(callback_query.from_user.id)
        await screen.update(client, callback_query.message.chat.id, callback_query.message.id, screen.referer_program(user_id))

    @app.on_callback_query(filters.regex('to_referals_list'))
    async def answer_referals_list(client, callback_query):
        user_id = str(callback_query.from_user.id)
        await screen.update(client, callback_query.message.chat.id, callback_query.message.id, screen.referals_list(user_id))

    @app.on_callback_query(filters.regex(r"to_set_referer\?referer_id=(\d+)"))
    async def answer(client, callback_query, **kwargs):
        global users

        user_id = str(callback_query.from_user.id)
        referer_id = re.search(r"^to_set_referer\?referer_id=(\d+)$", callback_query.data).group(1)

        wrong = None
        if referer_id not in users:
            wrong = "🤔 Не могу найти такого пользователя, проверь ещё раз."
        elif referer_id == user_id:
            wrong = "🧠 Ход гения, но не пройдёт — себя указывать нельзя!"
        elif referer_id == users[user_id]['loyalty_program']['referer_id']:
            wrong = "🤷🏻‍♀️ У тебя уже установлен этот реферер. Мб имелся в виду другой реферер?"
        elif users[referer_id]['loyalty_program']['subscribed_since'] is None:
            wrong = "👀 Этого человека сейчас нет в программе лояльности!"
        elif users[user_id]["registered_since"] <= users[referer_id]["registered_since"]:
            wrong = "👨🏻‍🍼 Твой реферер не может быть младше тебя!\nВремя регистрации можно проверить во вкладке с профилем."

        if wrong:
            await screen.update(client, callback_query.message.chat.id, callback_query.message.id, screen.set_referer_smth_wrong(wrong))
            return

        users[user_id]['loyalty_program']['referer_id'] = referer_id

        callback_query.answer(
            "🎈Талант и Успех!🎈",
            show_alert=False
        )

        await screen.update(client, callback_query.message.chat.id, callback_query.message.id, screen.congratulation_emoji())
        await screen.create(client, callback_query.message.chat.id, screen.set_referer_successfully())

    @app.on_callback_query(filters.regex('to_profile'))
    async def answer_profile(client, callback_query):
        global users

        await screen.update(client, callback_query.message.chat.id, callback_query.message.id, screen.loading())
        user_id = str(callback_query.from_user.id)
        await screen.update(client, callback_query.message.chat.id, callback_query.message.id, screen.profile(user_id))

    @app.on_chat_member_updated(group=server.server_vars.dot_ch_id)
    async def handler_channel_update(client, chat_member_updated):
        global users

        if not chat_member_updated.chat.id == server.server_vars.dot_ch_id:
            # действие происходит не в канале
            return
        if not chat_member_updated.old_chat_member:
            # это не отписка в канале
            return

        user_id = str(chat_member_updated.old_chat_member.user.id)
        if not is_registered(user_id):
            # отписавшийся от канала не в программе лояльности
            return

        users[user_id]["loyalty_program"]["subscribed_since"] = None
        await screen.create(client, user_id, screen.unsubscribed_from_channel_emoji())
        await screen.create(client, user_id, screen.unsubscribed_from_channel())

    # сообщения в личку
    @app.on_message(filters.private & filters.text & filters.incoming)
    async def answer_messages(client, message):
        import re

        message_text = message.text

        if re.search(r"^@[a-zA-Z0-9_]{1,20}bot", message_text):
            # команда
            search = re.search(r"^@[a-zA-Z0-9_]{1,20}bot добавить реферера с ID:[ ]{0,}([^\s]+)", message_text)
            if search:
                referer_id = search.group(1)
                if re.search(r"^[0-9]{1,}$", referer_id):
                    await screen.create(client, message.chat.id, screen.set_referer_confirm(referer_id=referer_id))
                else:
                    await screen.create(client, message.chat.id, screen.set_referer_not_number())
            else:
                await screen.create(client, message.chat.id, screen.unknown_command())
        else:
            # не команда
            await screen.create(client, message.chat.id, screen.no_messages())
