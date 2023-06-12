
import warnings
from datetime import datetime

from lib.useful_lib import random_datetime

from lib.q_md_lib import queue_money_drop

from global_vars import print, queue_md_params, common_scheduler

warnings.filterwarnings("ignore")


def q_drop_scheduler(q_moneydrop_scheduler, verbose=True):
    if verbose:
        print("Start q_drop_scheduler!")
    from datetime import timedelta
    for i in range(queue_md_params["drops"]):
        run_date = random_datetime(timedelta(minutes=queue_md_params["period_minutes"]))
        print(run_date)
        q_moneydrop_scheduler.add_job(
            queue_money_drop,
            'date',
            run_date=run_date
        )


def start_q_moneydrop_scheduler(verbose=True):

    common_scheduler.add_job(
        q_drop_scheduler, "interval", minutes=queue_md_params["period_minutes"],
        kwargs={
            "q_moneydrop_scheduler": common_scheduler,
            "verbose": verbose
        }, max_instances=1, next_run_time=datetime.now(),
        id="q_drop_scheduler"
    )


if __name__ == "__main__":
    from pyrogram import idle
    start_q_moneydrop_scheduler(verbose=True)
    idle()
