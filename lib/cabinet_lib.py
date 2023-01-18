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
        "rules": {
            "work": {
                "start": start,
                "finish": end,
                "delay_minutes": 5
            },
            "reward": {
                "per_one": 0.0001,
                "max_sum": 0.01
            }
        },
        "state": {
            "cabinet_status": -1,
            "inside": None,
            "winners": {
                "players": [],
                "sum": 0
            }
        }
    }

    update_queue(queue_id)


def cabinet_start(queue_id, to_update_queue=False):
    active_queues[queue_id]['cabinet']['state']['cabinet_status'] = 0
    add_global_queue_event(queue_id, "раздача началась!", event_emoji='🚩')
    if to_update_queue:
        update_queue(queue_id)


def cabinet_finish(queue_id, to_update_queue=False):
    active_queues[queue_id]['cabinet']['state']['cabinet_status'] = 1
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
    user_id = queue['queue_order'].pop(0)
    queue_user = queue_users[user_id]

    add_user_queue_event(queue_id, queue_user, "заходит в кабинет!", event_emoji="➡️🚪")
    queue_user['in'] = {
        "type": "cabinet",
        "id": queue_id,
        "timestamp": timestamp_now(),
        "delay_minutes": queue['cabinet']['rules']['work']['delay_minutes']
    }
    queue['cabinet']['state']['inside'] = user_id
    if to_update_queue:
        update_queue(queue_id)
