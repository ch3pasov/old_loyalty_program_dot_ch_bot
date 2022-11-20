import global_vars
import server.server_vars
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

users = global_vars.users

home_new_text = '''Привет! 🖖🏻
Я провожу ПРОГРАММУ ЛОЯЛЬНОСТИ 😳 телеграм-канала @dot_ch.

Правила такие:
1. Подписываешься на мой канал: 👉🏻 @dot_ch.
2. Регистрируешься у бота в ПРОГРАММЕ ЛОЯЛЬНОСТИ (чтобы потом не было вопросов чё это я тебе пишу 🤔).
3. Не отписываешься от канала и поднимаешь уровень ☝🏻.
4. За прохождение каждого уровеня ты получаешь монетки TON (через @wallet).

Увидеть нынешнюю сетку уровней и зарегистрироваться в ПРОГРАММЕ ЛОЯЛЬНОСТИ ты можешь по кнопкам ниже:'''

home_exist_text = '''Привет, юзер с номером {user_id}! 😳

Увидеть сетку уровней, проверить свой статус и поглядеть статистику ты можешь по кнопкам ниже:'''

loyality_schema_level = """**👤 уровень: {level}**
🗓 Дней, для левелапа: {days}
🪙 Награда при левелапе в TON: {reward}"""

loyality_schema_cooked = '\n\n'.join([loyality_schema_level.format(**line.__dict__) for line in server.server_vars.loyality_programm])

button_to_schema = '''📈сетка уровней📈'''
button_to_home = '''🏘на главную🏘'''
button_to_register = '''❇️регистрация❇️'''
button_to_statistic = '''📊статистика📊'''
button_to_leveling = '''🔄проверить свой уровень🔄'''


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
                        button_to_leveling,
                        callback_data="to_leveling"
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
        "text": 'Готово! Теперь ты зарегистрирован!',
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


def leveling(user_level, user_exp_days):
    global users
    return {
        "text": f'''Твой нынешний уровень: {user_level}\nТы подписан на канал {user_exp_days:.4f} дней!''',
        "reply_markup": InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        button_to_leveling,
                        callback_data="to_leveling"
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
    global users
    return {
        "text": "🥳LEVEL UP🥳",
        "reply_markup": InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        congrats_text,
                        url=congrats_link
                    )
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


def money_hidden_block_check():
    return {
        "animation": server.server_vars.money_animation,
        "unsave": False
    }


def money(send_message):
    return {
        "text": send_message.message,
        "reply_markup": InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Получить на @wallet",
                        url=send_message.reply_markup.rows[0].buttons[0].url
                    )
                ]
            ]
        )
    }


def statistic():
    global users
    return {
        "text": f'Количество пользователей: {len(users)}',
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


def send_money(app, app_human, amount, user_id):
    global users

    assert amount < 1, "МНОГО ДЕНЕГ"

    non_collision_amount = amount + int(user_id) % 100000/10**10

    r = app_human.get_inline_bot_results('@wallet', str(non_collision_amount))

    result = r.results[0]
    if "TON" in result.title and "BTC" not in result.title:
        app_human.send_inline_bot_result(server.server_vars.money_chat_id, r.query_id, result.id)
        app_human.send_message(server.server_vars.money_chat_id, f"отправил {amount} TON юзеру {user_id}")

        create(app, user_id, money(result.send_message))
    else:
        raise ValueError("BTC! СЛЕВА НАПРАВО")
