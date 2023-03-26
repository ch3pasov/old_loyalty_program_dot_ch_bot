
import warnings
from datetime import datetime

# from apscheduler.schedulers.background import BackgroundScheduler
from lib.queue_lib import slow_update_comments_queue, update_queue, kick_user_from_queue, add_user_queue_event, add_global_user_queue_event
from lib.cabinet_actions_lib import cabinet_start, cabinet_finish, get_user_cabinet_status_before_reward
from lib.useful_lib import timestamp_now, timestamp_to_datetime, dt_plus_n_minutes, datetime_to_timestamp
from lib.money import send_money
# from lib.useful_lib import seconds_between_timestamps
from global_vars import print, active_queues, queue_users, bot_username, queue_common_scheduler

warnings.filterwarnings("ignore")


def check_user(user_id, verbose=True, to_update_queue=False):
    if verbose:
        print(f"check user! {user_id}")

    queue_user = queue_users[user_id]

    timestamp = queue_user['in']["timestamp"]
    delay_minutes = queue_user['in']["delay_minutes"]
    click_deadline = datetime_to_timestamp(dt_plus_n_minutes(timestamp_to_datetime(timestamp), delay_minutes))

    queue_id = queue_user["in"]["id"]

    if timestamp_now() <= click_deadline:
        return

    intype = queue_user['in']['type']
    if intype == "queue":
        # кикнуть из очереди
        if verbose:
            print(f"kick user {user_id} from queue! queue {queue_id}.")
        kick_user_from_queue(user_id, to_update_queue=to_update_queue)
    elif intype == "cabinet":
        # Подсчитать награду и кикнуть из очереди
        if verbose:
            print(f"push user {user_id} from cabinet! queue {queue_id}.")
        cabinet_push(queue_id, to_update_queue=to_update_queue)
    else:
        raise ValueError(f'queue_user["in"]["type"] must be "queue" or "cabinet", not {intype}!')


def erase_check_user_scheduler_job(user_id):
    # print(f"Debug! {user_id}")
    if queue_common_scheduler.get_job(user_id):
        # print("Debug! нашёл и удалил!")
        queue_common_scheduler.remove_job(user_id)


def set_check_user_scheduler_job(user_id):
    erase_check_user_scheduler_job(user_id)
    queue_user = queue_users[user_id]

    # Это может быть и очередь, и кабинет

    timestamp = queue_user['in']["timestamp"]
    delay_minutes = queue_user['in']["delay_minutes"]

    job_dt = dt_plus_n_minutes(timestamp_to_datetime(timestamp), delay_minutes)
    queue_common_scheduler.add_job(
        check_user,
        "date",
        run_date=job_dt,
        kwargs={
            "user_id": user_id,
            "verbose": True,
            "to_update_queue": True
        },
        id=user_id
    )


def initial_set_check_user_scheduler_jobs(verbose=True):
    print("initial_set_check_user_scheduler_jobs")
    for user_id in queue_users:
        queue_user = queue_users[user_id]
        if not queue_user["in"]:
            continue

        # Это может быть и очередь, и кабинет
        set_check_user_scheduler_job(user_id)


def cabinet_pull(queue_id, to_update_queue=False):
    queue = active_queues[queue_id]
    user_id = queue['queue_order'].pop(0)
    queue_user = queue_users[user_id]

    add_user_queue_event(queue_id, user_id, "заходит в кабинет!", event_emoji="⬆️")
    queue_user['in'] = {
        "type": "cabinet",
        "id": queue_id,
        "timestamp": timestamp_now(),
        "delay_minutes": queue['cabinet']['rules']['work']['delay_minutes']
    }
    queue['cabinet']['state']['inside'] = user_id

    set_check_user_scheduler_job(user_id)

    if to_update_queue:
        update_queue(queue_id)


def check_to_cabinet_pull(queue_id, to_update_queue=False):
    queue = active_queues[queue_id]
    cabinet = queue['cabinet']
    if cabinet['state']['cabinet_status'] == 0 and cabinet['state']['inside'] is None and len(queue['queue_order']) > 0:
        erase_check_user_scheduler_job(user_id=queue['queue_order'][0])
        cabinet_pull(queue_id, to_update_queue=to_update_queue)


def cabinet_push(queue_id, to_update_queue=False):
    queue = active_queues[queue_id]

    user_id = queue['cabinet']['state']['inside']
    user_cabinet_status = get_user_cabinet_status_before_reward(user_id, queue_id)
    print(user_cabinet_status)

    gap = ' '
    if user_cabinet_status == "stranger":
        event_emoji = '😶'
        event_short = "странник! Выходит ни с чем!"
        gap = ', '
        event_long = f"вижу, что ты не являешься участником программы лояльности. Зарегистрируйся в программе лояльности: @{bot_username}, и попробуй встать в очередь снова."
        to_summon = True
    elif user_cabinet_status == "unsubscriber":
        event_emoji = '🐀'
        event_short = "отписчик! Выходит ни с чем!"
        gap = ', '
        event_long = f"вижу, что сейчас ты не являешься участником программы лояльности. Зарегистрируйся в программе лояльности заново: @{bot_username}, и попробуй встать в очередь снова."
        to_summon = True
    elif user_cabinet_status == "repeater":
        event_emoji = '🐷'
        event_short = "повторюшка! Выходит ни с чем!"
        event_long = "проходит кабиент повторно! Повторюшка дядя хрюшка, или ход гения? 🧠"
        to_summon = False
    elif user_cabinet_status == "pauper":
        event_emoji = '🐢'
        event_short = "опозданец! Выходит ни с чем!"
        gap = ', '
        event_long = "весь банк уже разобрали! Но спасибо за участие! ❤️"
        to_summon = False
    elif user_cabinet_status == "winner":
        reward = queue['cabinet']['rules']['reward']
        winners = queue['cabinet']['state']['winners']
        per_one = reward['per_one']
        event_emoji = '🏆'
        event_short = f"выигрывает {per_one}💎!"
        event_long = event_short
        to_summon = False
        # самое волнительное!
        send_money(per_one, user_id, referer_enable=True)
        winners["sum"] += per_one
        winners["players"].setdefault(user_id, 0)
        winners["players"][user_id] += per_one
    else:
        raise ValueError(f"Unknown user_cabinet_status! '{user_cabinet_status}'")

    add_global_user_queue_event(queue_id, user_id, event_short, event_long, event_emoji=event_emoji, gap=gap, to_summon=to_summon)
    add_user_queue_event(queue_id, user_id, "выходит из кабинета!", event_emoji="⬇️")

    queue_users[user_id]['in'] = None
    queue['cabinet']['state']['inside'] = None

    check_to_cabinet_pull(queue_id)
    if to_update_queue:
        update_queue(queue_id)


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


def initial_check_users(verbose=True):
    if verbose:
        print('initial_check_users!')
    for user_id in queue_users:
        if queue_users[user_id]["in"]:
            check_user(user_id, verbose=True, to_update_queue=False)


def add_cabinet_start_and_pull_job(start_timestamp, queue_id):
    open_date = timestamp_to_datetime(start_timestamp)
    queue_common_scheduler.add_job(cabinet_start_and_pull, "date", run_date=open_date, args=[queue_id])


def add_cabinet_finish_job(end_timestamp, queue_id):
    close_date = timestamp_to_datetime(end_timestamp)
    queue_common_scheduler.add_job(cabinet_finish, "date", run_date=close_date, args=[queue_id, True])


def set_cabinet_state_scheduler_job(queue_id, cabinet, verbose=True):
    timestamp_now_const = timestamp_now()
    start = cabinet['rules']['work']['start']
    end = cabinet['rules']['work']['finish']
    if timestamp_now_const < start:
        add_cabinet_start_and_pull_job(start, queue_id)
    if timestamp_now_const < end:
        add_cabinet_finish_job(end, queue_id)
    check_to_cabinet_pull(queue_id)


def initial_set_cabinet_state_scheduler_jobs(verbose=True):
    for queue_id in active_queues:
        cabinet = active_queues[queue_id]['cabinet']
        if cabinet:
            set_cabinet_state_scheduler_job(queue_id, cabinet, verbose=verbose)


def start_queue_scheduler(verbose=True):
    # queue_common_scheduler = BackgroundScheduler()

    initial_check_users()
    initial_set_check_user_scheduler_jobs()
    initial_set_cabinet_state_scheduler_jobs()

    queue_common_scheduler.add_job(update_all_queues, "interval", minutes=30, kwargs={"verbose": verbose}, max_instances=1, next_run_time=datetime.now())
    # queue_scheduler.add_job(update_queue_users, "interval", minutes=30, kwargs={"verbose": verbose}, max_instances=1, next_run_time=datetime.now())

    print(queue_common_scheduler.get_jobs())
    # queue_common_scheduler.start()


if __name__ == "__main__":
    from pyrogram import idle

    start_queue_scheduler(verbose=True)
    idle()
