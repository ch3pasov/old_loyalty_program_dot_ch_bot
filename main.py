from pyrogram import idle
import schedule
from global_vars import print, users
from interface import app
import server.server_vars

print(f"Я запустил main и смотрю на users. Его id {id(users)}")

if __name__ == '__main__':
    try:
        app.send_message(
            chat_id=server.server_vars.dot_ch_chat_id,
            text='Я запустился!',
            reply_to_message_id=server.server_vars.bot_debug_message_id
        )

        schedule.start_scheduler(users, verbose=False)
        print(f"Я запустил name=main в main и смотрю на users. Его id {id(users)}")
        idle()
    finally:
        print('FINALLY')
        app.send_message(
            chat_id=server.server_vars.dot_ch_chat_id,
            text='Я выключился! @yandex_links, обрати внимание, если это незапланированное выключение.',
            reply_to_message_id=server.server_vars.bot_debug_message_id
        )
        schedule.backup_log_job(users, verbose=True)
        schedule.save_log_job(users, verbose=True)
