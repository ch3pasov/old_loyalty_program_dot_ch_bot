from global_vars import app
from pyrogram import filters
from server.server_vars import dot_ch_id, dot_ch_chat_id, money_drop_amount
from time import sleep
from lib.money import money_drop

last_media_group_id = 0


def start_post_moneydrop_handlers():
    @app.on_message(filters.linked_channel)
    def my_handler(client, message):
        global last_media_group_id
        if message.sender_chat.id == dot_ch_id and message.chat.id == dot_ch_chat_id:
            if message.media_group_id != last_media_group_id:
                last_media_group_id = message.media_group_id if message.media_group_id else 0
                print('New post! Sleep!')
                sleep(15)
                print('Post-moneydrop!')
                money_drop(
                    dot_ch_chat_id,
                    message.id,
                    money_drop_amount
                )
