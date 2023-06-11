from global_vars import print, app, the_library
from pyrogram import filters
import lib.screen as screen
from lib.screen_library import screen_library


def start_the_library_handlers():
    print("start_the_library_handlers")

    @app.on_callback_query(filters.regex(r"^to_library$"))
    async def answer_library_home(client, callback_query, **kwargs):
        await screen.update(client, callback_query.message.chat.id, callback_query.message.id, screen.library_home())

    @app.on_callback_query(filters.regex(r"^to_library\?id=([a-zA-Z\d_]+)$"))
    async def answer_library_id(client, callback_query, **kwargs):
        library_id = callback_query.matches[0].group(1)
        if library_id in the_library:
            desired_screen = screen_library(library_id)
        else:
            desired_screen = screen.library_unknown()
        await screen.update(client, callback_query.message.chat.id, callback_query.message.id, desired_screen)
