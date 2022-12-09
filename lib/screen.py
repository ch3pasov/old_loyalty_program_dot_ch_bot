import global_vars
import server.server_vars
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
# from pyrogram.enums import ParseMode
from lib.useful_lib import seconds_from_timestamp, timestamp_to_datetime
from global_vars import users


bot_username = global_vars.bot_username

home_new_text = '''Привет! 🖖🏻
Я провожу ПРОГРАММУ ЛОЯЛЬНОСТИ 😳 телеграм-канала Анатолия @ch_an.

Правила такие:
1. Подписываешься на мой канал: 👉🏻 @ch_an.
2. Регистрируешься у бота в ПРОГРАММЕ ЛОЯЛЬНОСТИ (чтобы потом не было вопросов чё это я тебе пишу 🤔).
3. Не отписываешься от канала и поднимаешь уровень. ☝🏻
4. За прохождение каждого уровеня ты получаешь монетки TON 💎 (через @wallet).

Увидеть нынешнюю сетку уровней и зарегистрироваться в ПРОГРАММЕ ЛОЯЛЬНОСТИ ты можешь по кнопкам ниже:'''

home_exist_text = '''Привет, юзер с ID `{user_id}`! 😳

Увидеть сетку уровней, свой профиль и глобальную статистику ты можешь по кнопкам ниже:'''

level_schema_header = f"`{'Стаж':<7}{'Награда':<10}{'Уровень':<3}`\n"
level_schema_preform = [
    (
        f"{f'`{obj.days:11f}'.strip('0').strip('.,'):<8}" + f"{f'{obj.reward:0.4f}':<10}" + f"{obj.level:<3}`",
        obj
    ) for obj in server.server_vars.loyalty_program
]


def level_status(loyalty_program_row, user_level=None):
    n = loyalty_program_row.level
    if not user_level:
        return '▫️'
    if n < user_level:
        return f"[{loyalty_program_row.congrats_text}]({loyalty_program_row.congrats_link})"
    elif n > user_level:
        return '▫️'
    else:
        return '◼'


def render_level_schema(user_level=None):
    return level_schema_header + '\n'.join([obj[0]+level_status(obj[1], user_level) for obj in level_schema_preform])


# schema_columns = "👤уровень\t🗓Дней\t🪙Награда"

# schema_level = """**👤 уровень: {level}**
# 🗓 Дней, для левелапа: {days}
# 🪙 Награда при левелапе: {reward}💎"""

# schema_cooked = '\n\n'.join([schema_level.format(**line.__dict__) for line in server.server_vars.loyalty_program])

referer_program_text = '''**Реферерная программа**

{referer_status}

**Правила следующие:**
0. Все мы — рефералы.
1. Каждый реферал может указать своего реферера — того, кто будет получать бонусы.
2. Реферер должен быть активным участником ПРОГРАММЫ ЛОЯЛЬНОСТИ и зарегистрирован раньше, чем реферал.
3. Реферал в любой момент может поменять реферера на другого.
4. Реферер получает как бонус половину от всех выигрышей реферала в программе лояльности, реферал ничего не теряет и получает глубокое уважение от своего реферера.

Два уточнения:
1. Бонусный чек тоже считается выигрышем. Таким образом, реферер твоего реферера тоже может получить бонус.
2. по техническим причинам невозможно создавать чеки на <0.0001 💎, поэтому реферер получает чек, только если реферал получает ≥0.0002 💎.'''

set_referer_not_number_text = '''😬 Привет! Для добавления реферера нужно добавить его численный ID пользователя.
Попроси реферера прислать тебе сообщение с его 👤профилем👤 — его ID можно будет скопировать оттуда.'''

referer_program_invite = '''— бот 🧞 программы 💾 лояльности ⛓ канала 🗣 Анатолия 🤧 @ch_an 🤑.

**TL;DR** подписываешься на канал, получаешь TON-награду 💎 за то, что не отписываешься.

Ты можешь добавить меня как реферера — зарегистрируйся в боте и открой мою ссылку: t.me/{bot_username}?start=referer_id={my_id}.
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
button_to_statistic = '''📊статистика📊'''
button_to_profile = '''👤Мой профиль👤'''
button_to_profile_refresh = '''🔄Мой профиль🔄'''
button_to_referer_program = '''😳Реферерная программа😳'''


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


def schema(user_level=None):
    return {
        "text": render_level_schema(user_level),
        "reply_markup": InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        button_to_home,
                        callback_data="to_home"
                    )
                ]
            ]
        ),
        "disable_web_page_preview": True
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
        "text": 'Ты забыл подписаться. 😬\nПодпишись и попробуй снова.\n👉🏻@ch_an👈🏿',
        "reply_markup": InlineKeyboardMarkup(
            [

                [
                    InlineKeyboardButton(
                        button_to_register,
                        callback_data="to_register"
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


def congratulation_emoji():
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
                        button_to_referer_program,
                        callback_data="to_referer_program"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        button_to_home,
                        callback_data="to_home"
                    ),
                    InlineKeyboardButton(
                        button_to_profile_refresh,
                        callback_data="to_profile"
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
        "text": f'Всего пользователей: {users_cnt}\nПолучено суммарно: {users_win:.4f} TON 💎.',
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


def referer_program(user_id):
    referer_id = users[user_id]['loyalty_program']['referer_id']
    if referer_id:
        referer_status = f"У тебя уже установлен реферер: `{referer_id}`."
    else:
        referer_status = "Здесь ты можешь поучаствовать в реферерной программе ПРОГРАММЫ ЛОЯЛЬНОСТИ телеграм-канала Анатолия @ch_an."

    return {
        "text": referer_program_text.format(referer_status=referer_status),
        "reply_markup": InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(  # Opens the inline interface in the current chat
                        "Пригласить друга",
                        switch_inline_query=referer_program_invite.format(
                            bot_username=bot_username,
                            my_id=user_id
                        )
                    )
                ],
                [
                    InlineKeyboardButton(
                        button_to_home,
                        callback_data="to_home"
                    ),
                    InlineKeyboardButton(  # Opens the inline interface in the current chat
                        "Добавить реферера",
                        switch_inline_query_current_chat="добавить реферера с ID: "
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
                        "Да ✅",
                        callback_data=f"to_set_referer?referer_id={referer_id}"
                    ),
                    InlineKeyboardButton(
                        "Нет ❌",
                        callback_data="to_referer_program"
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
                        "◀️ К реферерной программе",
                        callback_data="to_referer_program"
                    )
                ],
            ]
        )
    }


def set_referer_successfully():
    return {
        "text": 'Готово! Реферер установлен!',
        "reply_markup": InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        button_to_referer_program,
                        callback_data="to_referer_program"
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
                        "◀️ К реферерной программе",
                        callback_data="to_referer_program"
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


def unsubscribed_from_channel_emoji():
    return {
        "text": "😓",
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
        "text": text,
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
