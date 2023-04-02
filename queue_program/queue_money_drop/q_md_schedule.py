
import warnings
from datetime import datetime

import server.server_vars
from apscheduler.schedulers.background import BackgroundScheduler
from lib.useful_lib import random_datetime

from lib.q_md_lib import queue_money_drop

from global_vars import print

warnings.filterwarnings("ignore")


def q_drop_scheduler(q_moneydrop_scheduler, verbose=True):
    if verbose:
        print("Start q_drop_scheduler!")
    from datetime import timedelta
    run_date = random_datetime(timedelta(minutes=server.server_vars.queue_md["period_minutes"]))
    print(run_date)
    q_moneydrop_scheduler.add_job(
        queue_money_drop,
        'date',
        run_date=run_date
    )


def start_q_moneydrop_scheduler(verbose=True):
    q_moneydrop_scheduler = BackgroundScheduler()

    q_moneydrop_scheduler.add_job(
        q_drop_scheduler, "interval", minutes=server.server_vars.queue_md["period_minutes"],
        kwargs={
            "q_moneydrop_scheduler": q_moneydrop_scheduler,
            "verbose": verbose
        }, max_instances=1, next_run_time=datetime.now()
    )

    q_moneydrop_scheduler.start()


if __name__ == "__main__":
    from pyrogram import idle
    start_q_moneydrop_scheduler(verbose=True)
    idle()
