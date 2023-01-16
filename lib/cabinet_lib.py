# import server.server_vars
from global_vars import active_queues, queue_users
from lib.queue_lib import add_global_queue_event, add_user_queue_event, update_queue
from lib.useful_lib import datetime_to_timestamp, now_plus_n_minutes, timestamp_now
# import lib.screen as screen
# from queue_program.queue_schedule import check_to_cabinet_start, check_to_cabinet_finish


def create_cabinet(
    queue_id,
    start=datetime_to_timestamp(now_plus_n_minutes(3)),
    end=datetime_to_timestamp(now_plus_n_minutes(30))
):
    queue = active_queues[queue_id]

    queue['cabinet'] = {
        "meta": {
            "start": start,
            "end": end,
            "reward": 0.0001,
            "reward_delay_min": 5
        },
        "stats": {
            "winners": [],
            "money_won": 0
        },
        "state": {
            "cabinet_work": "before_work",
            "is_door_open": False,
            "inside": None
        }
    }

    update_queue(queue_id)


def cabinet_door_open(queue_id, to_update_queue=False):
    active_queues[queue_id]['cabinet']['state']['is_door_open'] = True
    if to_update_queue:
        update_queue(queue_id)


def cabinet_door_close(queue_id, to_update_queue=False):
    active_queues[queue_id]['cabinet']['state']['is_door_open'] = False
    if to_update_queue:
        update_queue(queue_id)


def cabinet_start(queue_id, to_update_queue=False):
    active_queues[queue_id]['cabinet']['state']['cabinet_work'] = "work"
    cabinet_door_open(queue_id)
    add_global_queue_event(queue_id, "раздача началась!", event_emoji='🚩')
    if to_update_queue:
        update_queue(queue_id)


def cabinet_finish(queue_id, to_update_queue=False):
    active_queues[queue_id]['cabinet']['state']['cabinet_work'] = "after_work"
    cabinet_door_close(queue_id)
    add_global_queue_event(queue_id, "раздача закончилась!", event_emoji='🏁')
    if to_update_queue:
        update_queue(queue_id)


def cabinet_push(queue_id, to_update_queue=False):
    queue = active_queues[queue_id]

    user_id = queue['cabinet']['state']['inside']
    queue_user = queue_users[user_id]

    add_user_queue_event(queue_id, queue_user, "выходит из кабинета!", event_emoji="🚪➡️")
    queue_user['in'] = None
    queue['cabinet']['state']['inside'] = None
    if to_update_queue:
        update_queue(queue_id)


def cabinet_pull(queue_id, to_update_queue=False):
    queue = active_queues[queue_id]
    user_id = queue['queue'].pop(0)
    queue_user = queue_users[user_id]

    add_user_queue_event(queue_id, queue_user, "заходит в кабинет!", event_emoji="➡️🚪")
    queue_user['in'] = {
        "type": "cabinet",
        "id": queue_id,
        "timestamp": timestamp_now(),
        "delay_minutes": queue['cabinet']['meta']['reward_delay_min']
    }
    queue['cabinet']['state']['inside'] = user_id
    if to_update_queue:
        update_queue(queue_id)
