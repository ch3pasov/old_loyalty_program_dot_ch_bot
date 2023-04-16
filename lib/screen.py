import global_vars
import server.server_vars
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
# from pyrogram.enums import ParseMode
from lib.useful_lib import seconds_from_timestamp, timestamp_to_datetime_text_long, timestamp_to_time_text
from global_vars import users, queue_users, active_queues


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

level_schema_prequel = '''Стаж показан в днях, награда — в TON'ах, дело — в шляпе.
'''
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
4. Реферер получает как бонус половину от всех выигрышей реферала в программе лояльности; реферал ничего не теряет и получает глубокое уважение от своего реферера.

Два уточнения:
1. Бонусный чек тоже считается выигрышем. Таким образом, реферер твоего реферера тоже может получить бонус.
2. по техническим причинам невозможно создавать чеки на <0.0001 💎, поэтому реферер получает чек, только если реферал получает ≥0.0002 💎.

Твоя пригласительная ссылка: `{referer_link}`'''

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

button_to_schema = '''📈уровни📈'''
button_to_home = '''🏘на главную🏘'''
button_to_register = '''❇️регистрация❇️'''
button_to_statistic = '''📊статистика📊'''
button_to_profile = '''👤мой профиль👤'''
button_to_profile_refresh = '''🔄мой профиль🔄'''
button_to_referer_program = '''😳реферерная программа😳'''
button_back_to_referer_program = '''◀️ к реферерной программе'''


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
                        button_to_referer_program,
                        callback_data="to_referer_program"
                    )
                ],
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
        "text": level_schema_prequel+render_level_schema(user_level),
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
    user_registration_time = timestamp_to_datetime_text_long(users[user_id]["registered_since"])
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
        referer_status = f"Твой реферер на данный момент: `{referer_id}`."
    else:
        referer_status = "Здесь ты можешь поучаствовать в реферерной программе ПРОГРАММЫ ЛОЯЛЬНОСТИ телеграм-канала Анатолия @ch_an."

    return {
        "text": referer_program_text.format(referer_status=referer_status, referer_link=f"https://t.me/{bot_username}?start=referer_id={user_id}"),
        "reply_markup": InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "💬пригласить друга💬",
                        switch_inline_query=referer_program_invite.format(
                            bot_username=bot_username,
                            my_id=user_id
                        )
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🖇добавить реферера🖇",
                        switch_inline_query_current_chat="добавить реферера с ID: "
                    )
                ],
                [
                    InlineKeyboardButton(
                        "👼🏻Мои рефералы👼🏾",
                        callback_data="to_referals_list"
                    )
                ],
                [
                    InlineKeyboardButton(
                        button_to_home,
                        callback_data="to_home"
                    )
                ],
            ]
        )
    }


def referals_list(user_id):
    referals = [user for user in users if users[user]['loyalty_program']['referer_id'] == user_id]

    referals_cnt = len(referals)
    if referals_cnt > 0:
        text = f"**(прямых) рефералов:** {referals_cnt}\n\n**Их айдишники:**\n" + '\n'.join([f"`{obj}`" for obj in referals])
    else:
        text = "🙅🏻‍♀️ Пока никто не указал тебя своим реферером! Но ты всегда можешь это исправить:\n" + f"`https://t.me/{bot_username}?start=referer_id={user_id}`"

    return {
        "text": text,
        "reply_markup": InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        button_back_to_referer_program,
                        callback_data="to_referer_program"
                    )
                ],
            ]
        )
    }


def set_referer_confirm(referer_id):
    return {
        "text": f'Назначить твоим реферером юзера с ID=`{referer_id}`?',
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
                        button_back_to_referer_program,
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
                        button_back_to_referer_program,
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


def queue_admin_help(commands):
    from inspect import signature
    out = "Добро пожаловать в админку!\nКоманды:"
    for command_name in commands:
        command = commands[command_name]
        signature_command = signature(command)
        out += f"\n{command_name} — {command.__doc__}\n{signature_command}"
        out += f"\n`/admin {command_name} {' '.join([obj for obj in signature_command.parameters])}`"

    return {
        "text": out
    }


def queue_admin_run(command_output=None, is_success=True, errors=None):
    if is_success:
        text = f"Команда запущена успешно! Вывод:\n{command_output}"
    else:
        text = f"Ошибка! Вывод:\n{errors}"
    return {
        "text": text
    }


def queue_initial_post():
    return {
        "text": "Генерация поста-очереди. Подождите 10с.."
    }


def queue_first_comment(queue_id, chat_message_id):
    return {
        "text": '👥👥👥',
        "reply_markup": InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "👥",
                        callback_data=f"queue?id={queue_id}"
                    )
                ]
            ]
        ),
        "reply_to_message_id": chat_message_id
    }


def queue_state(queue_id, archive=False):
    queue = active_queues[queue_id]
    comments = queue["show"]["comments"]

    comments_cnt = comments["cnt"]
    comments_fingerprint = comments["fingerprint"]
    chat_message_id = queue["id"]["chat"]
    queue_order = queue["queue_order"]

    is_locked = queue["state"]["is_locked"]

    if queue_order:
        queue_text = f"{'🔒' if is_locked else ''}\n" + "\n".join([f"`{n+1}.`{queue_users[queue_order[n]]['name']}" for n in range(len(queue_order))][::-1])
    else:
        queue_text = f"{'🔒' if is_locked else '🫥'}"

    post_text = ''
    if archive:
        post_text += "[АРХИВ]\n"
    post_text += "👥 **Очередь:** "
    post_text += queue_text

    last_n_events = queue["show"]["last_n_events"]
    queue_delay_minutes = queue["rules"]["delay_minutes"]

    cabinet = queue["cabinet"]
    if cabinet:
        cabinet_state = cabinet["state"]

        inside_user = cabinet_state['inside']
        post_text += "\n🚪 **Кабинет:** "
        if inside_user:
            inside_name = queue_users[inside_user]['name']
            post_text += f"{inside_name}"
        elif cabinet_state['cabinet_status'] == -1:
            post_text += "🔒ещё не открыт"
        elif cabinet_state['cabinet_status'] == 1:
            post_text += "🔒уже закрыт"
        else:
            post_text += "🫥"

        rules = cabinet['rules']
        rules_work = rules['work']
        start = timestamp_to_time_text(rules_work['start'])
        end = timestamp_to_time_text(rules_work['finish'])
        post_text += f"\n\n⌚️ **Время раздачи:**\n{start}–{end} UTC"

        rules_reward = rules['reward']
        winners_sum = cabinet_state['winners']['sum']
        post_text += f"\n\n🏆 **Награда в тонах:** {rules_reward['per_one']}"
        post_text += f"\n🏦 **Банк очереди:** {rules_reward['max_sum']-winners_sum:.4f}/{rules_reward['max_sum']}"

    post_text += "\n"
    if cabinet:
        post_text += f"\n⌚️🚪 **Минут в кабинете:** {rules_work['delay_minutes']}"
    post_text += f"\n⌚️👥 **Афк-минут в очереди:** {queue_delay_minutes}"

    post_text += "\n\n**Последние 10 событий:**\n"
    post_text += '\n'.join(last_n_events[:-11:-1])

    return {
        "text": post_text,
        "reply_markup": InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "👥",
                        callback_data=f"queue?id={queue_id}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        f"{comments_fingerprint} комменты ({comments_cnt})",
                        url=f'https://t.me/c/{(-server.server_vars.dot_ch_chat_id)%10**10}/{chat_message_id}?thread={chat_message_id}'
                    )
                ]
            ]
        )
    }


def create(client, chat_id, screen):
    return client.send_message(
        chat_id,
        **screen
    )


def update(client, chat_id, message_id, screen):
    assert type(message_id) == int, f"message_id должен быть int, не {type(message_id)}"
    if "text" in screen:
        return client.edit_message_text(
            chat_id=chat_id,
            message_id=int(message_id),
            **screen
        )
    else:
        return client.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=int(message_id),
            **screen
        )
