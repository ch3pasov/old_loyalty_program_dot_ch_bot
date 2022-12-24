
import warnings
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from lib.queue_lib import slow_update_comments_queue, update_queue, clear_queue_user, add_event_queue
from lib.useful_lib import timestamp_now, seconds_between_timestamps
from global_vars import print, active_queues, queue_users

warnings.filterwarnings("ignore")


# Пересчитываю комменты в очередях
def update_all_queues(verbose=True):
    if verbose:
        print("update_all_queues!")
    for queue_id in active_queues:
        slow_update_comments_queue(queue_id)
        update_queue(queue_id)


def update_queue_users(verbose=True):
    if verbose:
        print('update_queue_users!')

    timestamp_now_const = timestamp_now()
    queues_to_update = set()
    for user_id in queue_users:
        queue_user = queue_users[user_id]

        # print(queue_user)
        # print(seconds_between_timestamps(timestamp_now_const, queue_user["last_clicked"]), queue_user["minutes_to_refresh"]*60)

        in_queue = queue_user["in_queue"]
        if not in_queue:
            # чел не в очереди
            continue
        if seconds_between_timestamps(timestamp_now_const, queue_user["last_clicked"]) < queue_user["minutes_to_refresh"]*60:
            # чел недавно кликал
            continue
        # надо выгнать чела из очереди

        add_event_queue(in_queue, queue_user, "вылетает из очереди!", event_emoji='🥾')
        clear_queue_user(user_id)
        queues_to_update.add(in_queue)
    for queue_id in queues_to_update:
        update_queue(queue_id)


def start_queue_scheduler(verbose=True):
    # global users
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_all_queues, "interval", minutes=30, kwargs={"verbose": verbose}, max_instances=1, next_run_time=datetime.now())
    scheduler.add_job(update_queue_users, "interval", seconds=30, kwargs={"verbose": verbose}, max_instances=1, next_run_time=datetime.now())
    scheduler.start()


if __name__ == "__main__":
    from pyrogram import idle

    start_queue_scheduler(verbose=True)
    idle()
