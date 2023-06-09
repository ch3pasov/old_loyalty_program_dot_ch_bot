from global_vars import the_library
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def screen_library(library_id):
    text = f"**{the_library[library_id]['title']}**\n\n{the_library[library_id]['text']}"

    markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    the_library.get(obj, {"title": "¯\\_(ツ)_/¯"})['title'],
                    callback_data=f"to_library?id={obj}"
                )
            ]
            for obj in the_library[library_id]['markup_to']
        ] +
        [
            [
                InlineKeyboardButton(
                    "🏘 к каталогу 📚",
                    callback_data="to_library"
                )
            ]
        ]
    )
    return {
        "text": text,
        "reply_markup": markup
    }
