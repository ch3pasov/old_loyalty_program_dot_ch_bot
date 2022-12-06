import global_vars
import server.server_vars
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from lib.useful_lib import seconds_from_timestamp, timestamp_to_datetime
from global_vars import users


bot_username = global_vars.bot_username

home_new_text = '''Привет! 🖖🏻
Я провожу ПРОГРАММУ ЛОЯЛЬНОСТИ 😳 телеграм-канала @dot_ch.

Правила такие:
1. Подписываешься на мой канал: 👉🏻 @dot_ch.
2. Регистрируешься у бота в ПРОГРАММЕ ЛОЯЛЬНОСТИ (чтобы потом не было вопросов чё это я тебе пишу 🤔).
3. Не отписываешься от канала и поднимаешь уровень. ☝🏻
4. За прохождение каждого уровеня ты получаешь монетки TON (через @wallet).

Увидеть нынешнюю сетку уровней и зарегистрироваться в ПРОГРАММЕ ЛОЯЛЬНОСТИ ты можешь по кнопкам ниже:'''

home_exist_text = '''Привет, юзер с ID `{user_id}`! 😳

Увидеть сетку уровней, проверить свой статус и поглядеть статистику ты можешь по кнопкам ниже:'''

loyality_schema_level = """**👤 уровень: {level}**
🗓 Дней, для левелапа: {days}
🪙 Награда при левелапе в TON: {reward}"""

loyality_schema_cooked = '\n\n'.join([loyality_schema_level.format(**line.__dict__) for line in server.server_vars.loyalty_program])

set_referer_not_number_text = '''Привет! Для добавления реферера нужно добавить его численный ID пользователя.
Попроси реферера прислать тебе сообщение с его 👤профилем👤 — его ID можно будет скопировать оттуда.'''

referal_program_invite = '''— бот 🧞 программы 💾 лояльности ⛓ канала 🗣 @dot_ch 🤑.

**TL;DR** подписываешься на канал, получаешь TON-награду за то, что не отписываешься.

Ты можешь добавить меня как реферала — зарегистрируйся в боте и открой мою ссылку: t.me/{bot_username}?start=referer_id={my_id}.
Спасибо!'''

profile_text = '''Твой ID: `{user_id}`
Твой нынешний уровень: {user_level}
Твой стаж на канале: {user_exp_days:.4f} дней!

Дата регистрации: {user_registration_time} (UTC)
Суммарный выигрыш в программе лояльности: {user_money_won:.4f}
ID твоего реферера: `{user_referer_id}`'''

button_to_schema = '''📈сетка уровней📈'''
button_to_home = '''🏘на главную🏘'''
button_to_register = '''❇️регистрация❇️'''
button_to_statistic = '''📊Глобальная статистика📊'''
button_to_profile = '''👤Мой профиль👤'''
button_to_profile_refresh = '''🔄Мой профиль🔄'''
button_to_referal_program = '''😳Реферальная программа😳'''


def home_new():
    return {
        "text": home_new_text,
        "reply_markup": InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        button_to_schema,
                        callback_data="to_schema"
                    )
                ],
                [
                    InlineKeyboardButton(
                        button_to_register,
                        callback_data="to_register"
                    )
                ]
            ]
        )
    }


def home_exist(user_id):
    return {
        "text": home_exist_text.format(user_id=user_id),
        "reply_markup": InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        button_to_profile,
                        callback_data="to_profile"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        button_to_schema,
                        callback_data="to_schema"
                    ),
                    InlineKeyboardButton(
                        button_to_statistic,
                        callback_data="to_statistic"
                    )
                ]
            ]
        )
    }


def loyality_schema():
    return {
        "text": loyality_schema_cooked,
        "reply_markup": InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        button_to_home,
                        callback_data="to_home"
                    )
                ]
            ]
        )
    }


def loading():
    return {
        "text": 'loading...'
    }


def register_already_register():
    return {
        "text": 'Ты уже в ПРОГРАММЕ ЛОЯЛЬНОСТИ!',
        "reply_markup": InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        button_to_home,
                        callback_data="to_home"
                    )
                ]
            ]
        )
    }


def register_not_subscribed():
    return {
        "text": 'Ты забыл подписаться. 😬\nПодпишись и попробуй снова.\n👉🏻@dot_ch👈🏿',
        "reply_markup": InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        button_to_home,
                        callback_data="to_home"
                    )
                ],
                [
                    InlineKeyboardButton(
                        button_to_register,
                        callback_data="to_register"
                    )
                ]
            ]
        )
    }


def register_successfully_emoji():
    return {
        "text": "🥳"
    }


def register_successfully():
    return {
        "text": 'Готово! С регистрацией!',
        "reply_markup": InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        button_to_home,
                        callback_data="to_home"
                    )
                ]
            ]
        )
    }


def profile(user_id):
    user_level = users[user_id]["loyalty_program"]["level"]
    user_exp_days = seconds_from_timestamp(users[user_id]["loyalty_program"]["subscribed_since"])/86400
    user_registration_time = timestamp_to_datetime(users[user_id]["registered_since"])
    user_money_won = users[user_id]["loyalty_program"]["money_won"]
    user_referer_id = users[user_id]["loyalty_program"]["referer_id"]

    return {
        "text": profile_text.format(
            user_id=user_id,
            user_level=user_level,
            user_exp_days=user_exp_days,
            user_registration_time=user_registration_time,
            user_money_won=user_money_won,
            user_referer_id=user_referer_id
        ),
        "reply_markup": InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        button_to_profile_refresh,
                        callback_data="to_profile"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        button_to_referal_program,
                        callback_data="to_referal_program"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        button_to_home,
                        callback_data="to_home"
                    )
                ]
            ]
        )
    }


def level_up(congrats_text, congrats_link):
    return {
        "text": "🥳LEVEL UP🥳",
        "reply_markup": InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        congrats_text,
                        url=congrats_link
                    )
                ]
            ]
        )
    }


def statistic():
    users_cnt = len(users)
    users_win = sum([float(users[user]['loyalty_program']['money_won']) for user in users])
    return {
        "text": f'Всего пользователей: {users_cnt}\nПолучено суммарно: {users_win} TON.',
        "reply_markup": InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        button_to_home,
                        callback_data="to_home"
                    )
                ]
            ]
        )
    }


def referal_program(user_id):
    return {
        "text": 'Реферальная программа!',
        "reply_markup": InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(  # Opens the inline interface in the current chat
                        "Добавить реферера",
                        switch_inline_query_current_chat="добавить реферера с ID: "
                    )
                ],
                [
                    InlineKeyboardButton(  # Opens the inline interface in the current chat
                        "Пригласить друга",
                        switch_inline_query=referal_program_invite.format(
                            bot_username=bot_username,
                            my_id=user_id
                        )
                    ),
                    InlineKeyboardButton(
                        button_to_home,
                        callback_data="to_home"
                    )
                ],
            ]
        )
    }


def set_referer_confirm(referer_id):
    return {
        "text": f'Ты хочешь назначить своим реферером юзера с ID=`{referer_id}`?',
        "reply_markup": InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Да!",
                        callback_data=f"to_set_referer?referer_id={referer_id}"
                    ),
                    InlineKeyboardButton(
                        "Нет!!!",
                        callback_data="to_referal_program"
                    )
                ],
            ]
        )
    }


def set_referer_smth_wrong(text):
    return {
        "text": text,
        "reply_markup": InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "К реферальной программе",
                        callback_data="to_referal_program"
                    )
                ],
            ]
        )
    }


def set_referer_successfully_emoji():
    return {
        "text": "🥳"
    }


def set_referer_successfully():
    return {
        "text": 'Готово! Реферер установлен!',
        "reply_markup": InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        button_to_referal_program,
                        callback_data="to_referal_program"
                    )
                ]
            ]
        )
    }


def unknown_command():
    return {
        "text": '''Привет! Вижу, что ты пытаешься ввести какую-то команду, но такой команды нет.''',
        "reply_markup": InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        button_to_home,
                        callback_data="to_home"
                    )
                ]
            ]
        )
    }


def set_referer_not_number():
    return {
        "text": set_referer_not_number_text,
        "reply_markup": InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        button_to_profile,
                        callback_data="to_profile"
                    )
                ]
            ]
        )
    }


def no_messages():
    return {
        "text": '''Не читаю твои текстовые сообщения. 🙈\nЛучше попробуй /start!'''
    }


def no_voices():
    return {
        "text": '''Не слушаю твои войсы. 🙉\nЛучше попробуй /start!'''
    }


def no_video_notes():
    return {
        "text": '''Не слушаю и не смотрю твои блинчики. 🙉🙈\nЛучше попробуй /start!'''
    }


def unsubscribed_from_channel_gif():
    return {
        "animation": server.server_vars.unsubscribed_animation,
        "unsave": False
    }


def unsubscribed_from_channel():
    return {
        "text": '😓 Ты приходи, хоть иногда 😓',
        "reply_markup": InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        button_to_home,
                        callback_data="to_home"
                    )
                ]
            ]
        )
    }


def money_hidden_block_check(text="💸"):
    return {
        "text": text
    }


def money(send_message, text=None, button_text=None, reply_to_message_id=None):
    return {
        "text": send_message.message if not text else text,
        "reply_markup": InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Получить на @wallet" if not button_text else button_text,
                        url=send_message.reply_markup.rows[0].buttons[0].url
                    )
                ]
            ]
        ),
        "reply_to_message_id": reply_to_message_id
    }


def create(client, chat_id, screen):
    if "animation" in screen:
        client.send_animation(
            chat_id,
            **screen
        )
        return 0

    client.send_message(
        chat_id,
        **screen
    )


def update(client, chat_id, message_id, screen):
    client.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        **screen
    )
