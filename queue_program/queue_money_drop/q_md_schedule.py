
import warnings
from datetime import datetime

import server.server_vars
from apscheduler.schedulers.background import BackgroundScheduler
from lib.useful_lib import random_datetime

from lib.q_md_lib import create_queue_money_drop

from global_vars import print

warnings.filterwarnings("ignore")


def q_drop_scheduler(dot_ch_chat_id, money_drop_message_id, moneydrop_scheduler, verbose=True):
    if verbose:
        print("Start drop_scheduler!")
    from datetime import timedelta
    run_date = random_datetime(timedelta(minutes=server.server_vars.money_drop_period_minutes))
    print(run_date)
    moneydrop_scheduler.add_job(
        create_queue_money_drop,
        'date',
        run_date=run_date,
        kwargs={
            "dot_ch_chat_id": dot_ch_chat_id,
            "money_drop_message_id": money_drop_message_id,
            "amount": server.server_vars.money_drop_amount
        }
    )


def start_q_moneydrop_scheduler(verbose=True):
    q_moneydrop_scheduler = BackgroundScheduler()

    q_moneydrop_scheduler.add_job(
        q_drop_scheduler, "interval", minutes=server.server_vars.money_drop_period_minutes,
        kwargs={
            "dot_ch_chat_id": server.server_vars.dot_ch_chat_id,
            "money_drop_message_id": server.server_vars.money_drop_message_id,
            "moneydrop_scheduler": q_moneydrop_scheduler,
            "verbose": verbose
        }, max_instances=1, next_run_time=datetime.now()
    )

    q_moneydrop_scheduler.start()


if __name__ == "__main__":
    from pyrogram import idle
    start_q_moneydrop_scheduler(verbose=True)
    idle()
