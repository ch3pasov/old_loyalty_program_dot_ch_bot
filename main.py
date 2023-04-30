from pyrogram import idle
from global_vars import print

from saving_schedule import backup_log_job, save_log_job, start_saving_scheduler

# from loyalty_program.moneydrop.moneydrop_schedule import start_moneydrop_scheduler
from queue_program.queue_money_drop.q_md_schedule import start_q_moneydrop_scheduler

from queue_program.queue_schedule import start_queue_scheduler
from loyalty_program.loyalty_schedule import start_loyalty_scheduler

from queue_program.queue_handlers import start_queue_handlers
from loyalty_program.bot_handlers import start_handlers
from admin_program.admin_handlers import start_admin_handlers

import server.server_vars
chat_id = server.server_vars.dot_ch_chat_id
reply_to_message_id = server.server_vars.bot_debug_message_id

if __name__ == '__main__':
    try:
        start_saving_scheduler(verbose=False)

        # start_moneydrop_scheduler(verbose=True)
        start_q_moneydrop_scheduler(verbose=True)

        start_queue_scheduler(verbose=True)
        start_loyalty_scheduler(verbose=False)

        start_queue_handlers()
        start_admin_handlers()
        start_handlers()

        # from global_vars import app
        # app.send_message(
        #     chat_id=server.server_vars.dot_ch_chat_id,
        #     text='Я запустился!',
        #     reply_to_message_id=server.server_vars.bot_debug_message_id
        # )
        idle()
    finally:
        print('FINALLY')
        backup_log_job(verbose=True)
        save_log_job(verbose=True)

        # app.send_message(
        #     chat_id=server.server_vars.dot_ch_chat_id,
        #     text=f'Я выключился! @{server.server_vars.creator_username_alarm}, обрати внимание, если это незапланированное выключение.',
        #     reply_to_message_id=server.server_vars.bot_debug_message_id
        # )
