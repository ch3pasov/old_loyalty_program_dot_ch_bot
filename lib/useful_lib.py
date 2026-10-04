# import server.server_vars
from datetime import datetime, timezone, timedelta
from pyrogram.enums import MessageMediaType
from emoji import emoji_list
# import lib.screen as screen


def now():
    return datetime.now(timezone.utc)


def dt_plus_n_minutes(dt, n):
    return dt + timedelta(minutes=n)


def now_plus_n_minutes(n):
    return dt_plus_n_minutes(datetime.now(timezone.utc), n)


def datetime_to_text(dt):
    return dt.strftime('%T')


def now_text():
    return datetime_to_text(now())


def datetime_to_timestamp(dt):
    return dt.timestamp()


def timestamp_now():
    return datetime_to_timestamp(now())


def timestamp_to_datetime(timestamp):
    return datetime.fromtimestamp(timestamp, timezone.utc)


def timestamp_to_datetime_text_long(timestamp):
    return timestamp_to_datetime(timestamp).strftime('%F %T.%f')


def timestamp_to_time_text(timestamp):
    return datetime_to_text(datetime.fromtimestamp(timestamp, timezone.utc))


def seconds_between_timestamps(timestamp_after, timestamp_before):
    return (datetime.fromtimestamp(timestamp_after, timezone.utc) - datetime.fromtimestamp(timestamp_before, timezone.utc)).total_seconds()


def seconds_from_timestamp(timestamp):
    return seconds_between_timestamps(timestamp_now(), timestamp)
    # return (now() - datetime.fromtimestamp(timestamp, timezone.utc)).total_seconds()


def random_datetime(up_timedelta):
    from random import random
    return datetime.now(timezone.utc)+up_timedelta*random()


def count_emoji_len(string):
    string_emoji_list = emoji_list(string)
    # считаю кол-во эмодзи символов, чтобы не учитывать их в длине строки
    string_emoji_len = sum([obj['match_end']-obj['match_start'] for obj in string_emoji_list])
    return len(string) - string_emoji_len + len(string_emoji_list)*(23/9)


def telegram_comment_strip(string, string_len):
    string_emoji_list = emoji_list(string)

    answer_text = ''
    answer_weight = 0
    for i in range(len(string)):
        symbol, weight = string[i], 1

        if string_emoji_list != []:
            string_emoji = string_emoji_list[0]
            match_start, match_end, emoji = string_emoji['match_start'], string_emoji['match_end'], string_emoji['emoji']
            if i == match_end - 1:
                string_emoji_list.pop(0)
            if match_start < i < match_end:
                continue
            if i == match_start:
                symbol, weight = emoji, 23/9

        # print(i, symbol, weight, string_emoji)
        if answer_weight + weight > string_len:
            break
        answer_text += symbol
        answer_weight += weight

    return answer_text


def sanitize_comment_message(message):
    if message.media:
        if message.media == MessageMediaType.STICKER:
            media_emoji = message.sticker.emoji
            media_text = "Стикер"
        elif message.media == MessageMediaType.DICE:
            media_emoji = message.dice.emoji
            media_text = f"Ролл — {message.dice.value}!"
        else:
            media_emoji = {
                MessageMediaType.AUDIO: "🎵",
                MessageMediaType.DOCUMENT: "📄",
                MessageMediaType.PHOTO: "🖼",
                MessageMediaType.VIDEO: "🎥",
                MessageMediaType.ANIMATION: "📹",
                MessageMediaType.VOICE: "🎤",
                MessageMediaType.VIDEO_NOTE: "📺",
                MessageMediaType.CONTACT: "👤",
                MessageMediaType.LOCATION: "📍",
                MessageMediaType.VENUE: "📍",
                MessageMediaType.POLL: "🗳",
                MessageMediaType.WEB_PAGE: "🔗",
                MessageMediaType.GAME: "🕹"
            }[message.media]

            media_text = {
                MessageMediaType.AUDIO: "Аудио 🎵",
                MessageMediaType.DOCUMENT: "Документ 📄",
                MessageMediaType.PHOTO: "Фото 🖼",
                MessageMediaType.VIDEO: "Видео 🎥",
                MessageMediaType.ANIMATION: "Анимация 🐭",
                MessageMediaType.VOICE: "Войс 🤡",
                MessageMediaType.VIDEO_NOTE: "Блинчик 🥞",
                MessageMediaType.CONTACT: "Контакт 🤔",
                MessageMediaType.LOCATION: "Локация 😤",
                MessageMediaType.VENUE: "Рандеву́ 🎩",
                MessageMediaType.POLL: "Г О Л О С О В А Н И Е",
                MessageMediaType.WEB_PAGE: "Веб-страничка 🧚🏻‍♀️🧚🏼‍♀️🧚🏽‍♀️🧚🏾‍♀️🧚🏿‍♀️",
                MessageMediaType.GAME: "Игра 🍸"
            }[message.media]

    if message.text:
        message_text = message.text
    elif message.caption:
        message_text = message.caption
    elif message.media and not message.media_group_id:
        message_text = media_text
    else:
        return None

    if message.media:
        message_text = f"{media_emoji} {message_text}"

    # удаляем плохие символы, что могут сломать разметку
    message_text = ''.join((i if i not in '\\`\n/*_|~@.' else ' ') for i in message_text)
    # обрезаем коммент до приемлимых N символов с учётом эмодзи
    message_text = telegram_comment_strip(message_text, 29)

    if message_text == "":
        return None

    # накинем моноспейса
    message_text = "`"+message_text+"`"
    return message_text


def emoji_fingerprint(cnt):
    emoji_list = ['👀', '🤔', '🫣', '👃', '🙈', '🆘', '📳', '💟']
    # print(emoji_list[cnt % len(emoji_list)])
    return emoji_list[cnt % len(emoji_list)]
