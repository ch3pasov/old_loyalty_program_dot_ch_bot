
import warnings
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from lib.queue_lib import slow_update_comments_queue, update_queue, kick_user_from_queue
from lib.cabinet_lib import cabinet_start, cabinet_finish, cabinet_pull
from lib.useful_lib import timestamp_now, seconds_between_timestamps, timestamp_to_datetime, dt_plus_n_minutes
from global_vars import print, active_queues, queue_users

warnings.filterwarnings("ignore")


def check_to_cabinet_pull(queue_id, to_update_queue=False):
    queue = active_queues[queue_id]
    cabinet = queue['cabinet']
    if cabinet['state']['is_door_open'] and cabinet['state']['inside'] is None and len(queue['queue']) > 0:
        cabinet_pull(queue_id, to_update_queue=to_update_queue)


def cabinet_start_and_pull(queue_id):
    cabinet_start(queue_id)
    check_to_cabinet_pull(queue_id)
    update_queue(queue_id)


def check_to_cabinet_start(queue_id, timestamp_now_const, verbose=True):
    cabinet = active_queues[queue_id]['cabinet']
    if cabinet['meta']['start'] < timestamp_now_const and cabinet['state']['cabinet_work'] == "before_work":
        if verbose:
            print(f"{queue_id} open cabinet!")
        cabinet_start_and_pull(queue_id)


def check_to_cabinet_finish(queue_id, timestamp_now_const, verbose=True):
    cabinet = active_queues[queue_id]['cabinet']
    if cabinet['meta']['end'] < timestamp_now_const and cabinet['state']['cabinet_work'] == "work":
        if verbose:
            print(f"{queue_id} close cabinet!")
        cabinet_finish(queue_id)


def check_to_kick(user_id, last_clicked, verbose=True):
    queue_user = queue_users[user_id]
    queue_id = queue_user["in_queue"]
    if not queue_id:
        if verbose:
            print(f"{user_id} not in queue!")
        return
    if last_clicked != queue_user["last_clicked"]:
        if verbose:
            print(f"{user_id} user clicked!")
        return
    # выгнать
    if verbose:
        print(f"kick user {user_id}! queue {queue_id}.")
    kick_user_from_queue(queue_user, user_id, to_update_queue=True)


# Пересчитываю комменты в очередях
# Проверяю, а не открылся ли кабинет
# Проверяю, а не закрылся ли кабинет
def update_all_queues(verbose=True):
    if verbose:
        print("update_all_queues!")
    timestamp_now_const = timestamp_now()
    for queue_id in active_queues:
        if active_queues[queue_id]['cabinet']:
            check_to_cabinet_start(queue_id, timestamp_now_const, verbose=True)
            check_to_cabinet_finish(queue_id, timestamp_now_const, verbose=True)

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


def initial_set_cabinet_state_scheduler_jobs(scheduler, verbose=True):
    for queue_id in active_queues:
        cabinet = active_queues[queue_id]['cabinet']
        if cabinet:
            timestamp_now_const = timestamp_now()
            start = cabinet['meta']['start']
            end = cabinet['meta']['end']
            if timestamp_now_const < start:
                open_date = timestamp_to_datetime(start)
                scheduler.add_job(cabinet_start_and_pull, "date", run_date=open_date, args=[queue_id])
            if timestamp_now_const < end:
                close_date = timestamp_to_datetime(end)
                scheduler.add_job(cabinet_finish, "date", run_date=close_date, args=[queue_id, True])
            check_to_cabinet_pull(queue_id)


def set_kick_user_scheduler_job(scheduler, user_id):
    last_clicked = queue_users[user_id]["last_clicked"]
    minutes_to_refresh = queue_users[user_id]["minutes_to_refresh"]

    click_deadline = dt_plus_n_minutes(timestamp_to_datetime(last_clicked), minutes_to_refresh)
    if scheduler.get_job(user_id):
        scheduler.remove_job(user_id)
    scheduler.add_job(
        check_to_kick,
        "date",
        run_date=click_deadline,
        kwargs={
            "user_id": user_id,
            "last_clicked": last_clicked,
            "verbose": True
        },
        id=user_id
    )


def initial_set_kick_user_scheduler_jobs(scheduler, verbose=True):
    print("initial_set_kick_user_scheduler_jobs")
    for user_id in queue_users:
        if queue_users[user_id]["in_queue"]:
            set_kick_user_scheduler_job(scheduler, user_id)


def start_queue_scheduler(verbose=True):
    queue_scheduler = BackgroundScheduler()
    queue_scheduler.add_job(update_all_queues, "interval", minutes=30, kwargs={"verbose": verbose}, max_instances=1, next_run_time=datetime.now())
    queue_scheduler.add_job(update_queue_users, "interval", minutes=30, kwargs={"verbose": verbose}, max_instances=1, next_run_time=datetime.now())
    initial_set_cabinet_state_scheduler_jobs(queue_scheduler)
    initial_set_kick_user_scheduler_jobs(queue_scheduler)
    print(queue_scheduler.get_jobs())
    queue_scheduler.start()


if __name__ == "__main__":
    from pyrogram import idle

    start_queue_scheduler(verbose=True)
    idle()
