
import warnings
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from lib.queue_lib import slow_update_comments_queue, update_queue, kick_user_from_queue
from lib.cabinet_lib import cabinet_start, cabinet_finish, cabinet_pull
from lib.useful_lib import timestamp_now, seconds_between_timestamps, timestamp_to_datetime, dt_plus_n_minutes
from global_vars import print, active_queues, queue_users, queue_local_scheduler

warnings.filterwarnings("ignore")


def erase_kick_user_scheduler_job(scheduler, user_id):
    # print(f"Debug! {user_id}")
    if scheduler.get_job(user_id):
        # print("Debug! нашёл и удалил!")
        scheduler.remove_job(user_id)


def set_kick_user_scheduler_job(scheduler, user_id):
    erase_kick_user_scheduler_job(scheduler, user_id)

    queue_user = queue_users[user_id]
    intype = queue_user["in"]["type"]
    if intype != "queue":
        return

    last_clicked = queue_user['in']["timestamp"]
    minutes_to_refresh = queue_user['in']["delay_minutes"]

    click_deadline = dt_plus_n_minutes(timestamp_to_datetime(last_clicked), minutes_to_refresh)
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
        queue_user = queue_users[user_id]
        if not queue_user["in"]:
            continue
        if queue_user["in"]["type"] == "queue":
            set_kick_user_scheduler_job(scheduler, user_id)


def check_to_cabinet_pull(queue_id, to_update_queue=False):
    queue = active_queues[queue_id]
    cabinet = queue['cabinet']
    if cabinet['state']['cabinet_status'] == 0 and cabinet['state']['inside'] is None and len(queue['queue_order']) > 0:
        erase_kick_user_scheduler_job(queue_local_scheduler, user_id=queue['queue_order'][0])
        cabinet_pull(queue_id, to_update_queue=to_update_queue)


def cabinet_start_and_pull(queue_id):
    cabinet_start(queue_id)
    check_to_cabinet_pull(queue_id)
    update_queue(queue_id)


def check_to_cabinet_start(queue_id, timestamp_now_const, verbose=True):
    cabinet = active_queues[queue_id]['cabinet']
    if cabinet['rules']['work']['start'] < timestamp_now_const and cabinet['state']['cabinet_status'] == -1:
        if verbose:
            print(f"{queue_id} open cabinet!")
        cabinet_start_and_pull(queue_id)


def check_to_cabinet_finish(queue_id, timestamp_now_const, verbose=True):
    cabinet = active_queues[queue_id]['cabinet']
    if cabinet['rules']['work']['finish'] < timestamp_now_const and cabinet['state']['cabinet_status'] == 0:
        if verbose:
            print(f"{queue_id} close cabinet!")
        cabinet_finish(queue_id)


def check_to_kick(user_id, last_clicked, verbose=True):
    queue_user = queue_users[user_id]

    intype = queue_user["in"]["type"]
    assert intype == "queue", f'queue_user["in"]["type"] must be "queue", not {intype}'
    queue_id = queue_user["in"]["id"]
    if not queue_id:
        if verbose:
            print(f"{user_id} not in queue!")
        return
    if last_clicked != queue_user["in"]["timestamp"]:
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

        if not queue_user["in"]:
            # чел ни в очереди, ни в кабинете
            continue
        if queue_user["in"]["type"] != "queue":
            # чел в кабинете
            continue
        if seconds_between_timestamps(timestamp_now_const, queue_user["in"]["timestamp"]) < queue_user["in"]["delay_minutes"]*60:
            # чел недавно кликал
            continue
        # надо выгнать чела из очереди

        queue_id = queue_user["in"]["id"]
        kick_user_from_queue(queue_user, user_id)
        queues_to_update.add(queue_id)
    for queue_id in queues_to_update:
        update_queue(queue_id)


def initial_set_cabinet_state_scheduler_jobs(scheduler, verbose=True):
    for queue_id in active_queues:
        cabinet = active_queues[queue_id]['cabinet']
        if cabinet:
            timestamp_now_const = timestamp_now()
            start = cabinet['rules']['work']['start']
            end = cabinet['rules']['work']['finish']
            if timestamp_now_const < start:
                open_date = timestamp_to_datetime(start)
                scheduler.add_job(cabinet_start_and_pull, "date", run_date=open_date, args=[queue_id])
            if timestamp_now_const < end:
                close_date = timestamp_to_datetime(end)
                scheduler.add_job(cabinet_finish, "date", run_date=close_date, args=[queue_id, True])
            check_to_cabinet_pull(queue_id)


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
