
import warnings
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from lib.queue_lib import slow_update_comments_queue, update_queue, kick_user_from_queue, open_cabinet, close_cabinet
from lib.useful_lib import timestamp_now, seconds_between_timestamps
from global_vars import print, active_queues, queue_users

warnings.filterwarnings("ignore")


# Пересчитываю комменты в очередях
# Проверяю, а не открылся ли кабинет
# Проверяю, а не закрылся ли кабинет
def update_all_queues(verbose=True):
    if verbose:
        print("update_all_queues!")
    timestamp_now_const = timestamp_now()
    for queue_id in active_queues:
        cabinet = active_queues[queue_id]["cabinet"]
        if cabinet:
            if cabinet['meta']['start'] < timestamp_now_const and cabinet['state'] == "before_work":
                open_cabinet(queue_id)
            if cabinet['meta']['end'] < timestamp_now_const and cabinet['state'] == "work":
                close_cabinet(queue_id)

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

        kick_user_from_queue(queue_user, user_id)
        queues_to_update.add(in_queue)
    for queue_id in queues_to_update:
        update_queue(queue_id)


def check_to_kick(user_id, last_clicked, verbose=True):
    queue_user = queue_users[user_id]
    in_queue = queue_user["in_queue"]
    if not in_queue:
        if verbose:
            print(f"{user_id} not in queue!")
        return
    if last_clicked != queue_user["last_clicked"]:
        if verbose:
            print(f"{user_id} user clicked!")
        return
    # выгнать
    if verbose:
        print(f"{user_id} kick user!")
    kick_user_from_queue(queue_user, user_id)
    print(in_queue)
    update_queue(in_queue)


def start_queue_global_scheduler(verbose=True):
    queue_global_scheduler = BackgroundScheduler()
    queue_global_scheduler.add_job(update_all_queues, "interval", minutes=1, kwargs={"verbose": verbose}, max_instances=1, next_run_time=datetime.now())
    queue_global_scheduler.add_job(update_queue_users, "interval", minutes=30, kwargs={"verbose": verbose}, max_instances=1, next_run_time=datetime.now())
    queue_global_scheduler.start()


def start_queue_local_scheduler():
    queue_local_scheduler = BackgroundScheduler()
    queue_local_scheduler.start()
    return queue_local_scheduler


if __name__ == "__main__":
    from pyrogram import idle

    start_queue_global_scheduler(verbose=True)
    idle()
