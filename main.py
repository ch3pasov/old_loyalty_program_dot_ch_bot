from pyrogram import idle
import schedule
from global_vars import print
from interface import app
import server.server_vars

if __name__ == '__main__':
    try:
        # app.send_message(
        #     chat_id=server.server_vars.dot_ch_chat_id,
        #     text='Я запустился!',
        #     reply_to_message_id=server.server_vars.bot_debug_message_id
        # )

        schedule.start_scheduler(verbose=False)
        idle()
    finally:
        print('FINALLY')
        schedule.backup_log_job(verbose=True)
        schedule.save_log_job(verbose=True)
        # app.send_message(
        #     chat_id=server.server_vars.dot_ch_chat_id,
        #     text='Я выключился! @yandex_links, обрати внимание, если это незапланированное выключение.',
        #     reply_to_message_id=server.server_vars.bot_debug_message_id
        # )
