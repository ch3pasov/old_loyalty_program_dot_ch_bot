
import warnings
from datetime import datetime

import server.server_vars
from lib.useful_lib import random_datetime
from lib.money import money_drop

from global_vars import print, common_scheduler

warnings.filterwarnings("ignore")


def drop_scheduler(dot_ch_chat_id, money_drop_message_id, moneydrop_scheduler, verbose=True):
    if verbose:
        print("Start drop_scheduler!")
    from datetime import timedelta
    for i in range(server.server_vars.money_drop_drops):
        run_date = random_datetime(timedelta(minutes=server.server_vars.money_drop_period_minutes))
        print(run_date)
        common_scheduler.add_job(
            money_drop,
            'date',
            run_date=run_date,
            kwargs={
                "dot_ch_chat_id": dot_ch_chat_id,
                "money_drop_message_id": money_drop_message_id,
                "amount": server.server_vars.money_drop_amount
            },
            id="money_drop"
        )


def start_moneydrop_scheduler(verbose=True):
    common_scheduler.add_job(
        drop_scheduler, "interval", minutes=server.server_vars.money_drop_period_minutes,
        kwargs={
            "dot_ch_chat_id": server.server_vars.dot_ch_chat_id,
            "money_drop_message_id": server.server_vars.money_drop_message_id,
            "moneydrop_scheduler": common_scheduler,
            "verbose": verbose
        }, max_instances=1, next_run_time=datetime.now(),
        id="start_moneydrop_scheduler"
    )


if __name__ == "__main__":
    from pyrogram import idle
    start_moneydrop_scheduler(verbose=True)
    idle()
