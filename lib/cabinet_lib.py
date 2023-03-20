# import server.server_vars
from global_vars import users, active_queues
from lib.queue_lib import add_global_queue_event, update_queue
from lib.useful_lib import datetime_to_timestamp, now_plus_n_minutes
from lib.social_lib import check_if_banned_before_money
# import lib.screen as screen
# from queue_program.queue_schedule import check_to_cabinet_start, check_to_cabinet_finish


def create_cabinet(
    queue_id,
    start=datetime_to_timestamp(now_plus_n_minutes(3)),
    end=datetime_to_timestamp(now_plus_n_minutes(30)),
    reward_per_one=0.0001,
    reward_max_sum=0.01,
    cabinet_delay_minutes=5
):
    queue = active_queues[queue_id]

    queue['cabinet'] = {
        "rules": {
            "work": {
                "start": start,
                "finish": end,
                "delay_minutes": cabinet_delay_minutes
            },
            "reward": {
                "per_one": reward_per_one,
                "max_sum": reward_max_sum
            }
        },
        "state": {
            "cabinet_status": -1,
            "inside": None,
            "winners": {
                "players": {},
                "sum": 0
            }
        }
    }

    update_queue(queue_id)


def cabinet_start(queue_id, to_update_queue=False):
    active_queues[queue_id]['cabinet']['state']['cabinet_status'] = 0
    add_global_queue_event(queue_id, "кабинет открывается!\nПроходим в порядке очереди!", event_emoji='🚩')
    if to_update_queue:
        update_queue(queue_id)


def cabinet_finish(queue_id, to_update_queue=False):
    active_queues[queue_id]['cabinet']['state']['cabinet_status'] = 1
    add_global_queue_event(queue_id, "кабинет закрывается!\nВсем спасибо за участие ❤️", event_emoji='🏁')
    if to_update_queue:
        update_queue(queue_id)


def get_user_cabinet_status_before_reward(user_id, queue_id, verbose=True):
    cabinet = active_queues[queue_id]["cabinet"]
    winners = cabinet["state"]["winners"]
    reward = cabinet["rules"]["reward"]
    if user_id not in users:
        user_cabinet_status = "stranger"
    elif not users[user_id]["loyalty_program"]["subscribed_since"]:
        user_cabinet_status = "unsubscriber"
    elif winners["sum"] + reward["per_one"] >= reward["max_sum"]:
        user_cabinet_status = "pauper"
    elif user_id in winners["players"]:
        user_cabinet_status = "repeater"
    else:
        is_available_to_reward = check_if_banned_before_money(user_id, text="🏆")
        if is_available_to_reward:
            user_cabinet_status = "winner"
        else:
            user_cabinet_status = "unsubscriber"

    if verbose:
        print(user_cabinet_status)
    return user_cabinet_status
