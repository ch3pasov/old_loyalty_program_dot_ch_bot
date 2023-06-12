from global_vars import users, active_queues, queue_users
from lib.queue_lib import add_global_queue_event, update_queue
from lib.social_lib import check_if_banned_before_money


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
    elif user_id in winners["players"]:
        user_cabinet_status = "repeater"
    elif winners["sum"] + reward["per_one"] >= reward["max_sum"]:
        user_cabinet_status = "pauper"
    else:
        is_available_to_reward = check_if_banned_before_money(user_id, text="🏆")
        if is_available_to_reward:
            user_cabinet_status = "winner"
        else:
            user_cabinet_status = "unsubscriber"

    if verbose:
        print(user_cabinet_status)
    return user_cabinet_status


def kick_user_from_cabinet(user_id, queue_id):
    '''Выкинуть юзера из кабинета. Без дополнительных комментариев'''
    queue_users[user_id]['in'] = None
    active_queues[queue_id]['cabinet']['state']['inside'] = None
