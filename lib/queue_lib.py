import json
import server.server_vars
from global_vars import active_queues, queue_users, app, app_billing, print
from pyrogram import errors
import lib.screen as screen
from lib.useful_lib import emoji_fingerprint, now_text
from lib.social_lib import get_user_name


def create_queue():
    # создаю пост
    channel_message_id = (screen.create(app, server.server_vars.dot_ch_id, screen.queue_initial_post())).id
    # print(channel_message_id)

    queue_id = str(channel_message_id)

    chat_message_id = app_billing.get_discussion_message(
        chat_id=server.server_vars.dot_ch_id,
        message_id=channel_message_id
    ).id

    queue = {
        "channel_message_id": channel_message_id,
        "chat_message_id": chat_message_id,
        "queue": [],
        "last_n_events": [],
        "comments": {
            "cnt": 0,
            "fingerprint": "👀"
        },
        "cabinet": None,
        "minutes_to_refresh": 15
    }

    screen.update(app, server.server_vars.dot_ch_id, channel_message_id, screen.queue_state(queue))
    screen.create(app, server.server_vars.dot_ch_chat_id, screen.queue_first_comment(queue_id, chat_message_id))

    active_queues[queue_id] = queue
    filename = "server/active_queues.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(active_queues, f, ensure_ascii=False, indent=4)

    print(f"Очередь {queue_id} создана!")


def update_queue(queue_id):
    queue = active_queues[queue_id]
    channel_message_id = queue["channel_message_id"]
    try:
        screen.update(app, server.server_vars.dot_ch_id, channel_message_id, screen.queue_state(queue))
    except errors.exceptions.bad_request_400.MessageNotModified:
        print(f'{queue_id} ничего не изменилось')


def add_queue_event(queue_id, event, event_emoji=''):
    new_event = f"`{now_text()}` {event_emoji} {event}"
    active_queues[queue_id]["last_n_events"] = (active_queues[queue_id]["last_n_events"]+[new_event])[-5:]


def add_user_queue_event(queue_id, queue_user, event, event_emoji=''):
    add_queue_event(queue_id, f"{queue_user['name']} {event}", event_emoji=event_emoji)


def add_global_queue_event(queue_id, event, event_emoji=''):
    add_queue_event(queue_id, event, event_emoji=event_emoji)
    app.send_message(
        server.server_vars.dot_ch_chat_id,
        event_emoji,
        reply_to_message_id=active_queues[queue_id]["chat_message_id"]
    )


def slow_update_comments_queue(queue_id):
    comments_cnt = app_billing.get_discussion_replies_count(server.server_vars.dot_ch_chat_id, message_id=active_queues[queue_id]["chat_message_id"])

    active_queues[queue_id]["comments"]["cnt"] = comments_cnt


def fast_update_comments_queue(queue_id, change=1):
    active_queues[queue_id]["comments"]["cnt"] += change
    active_queues[queue_id]["comments"]["dfingerprint"] = emoji_fingerprint()


def prerender_queue_user_and_update_name_and_get_queue_user(user):
    user_id = str(user.id)
    queue_users.setdefault(
        user_id,
        {
            "in_queue": None,
            "last_clicked": None,
            "minutes_to_refresh": None,
            "name": None
        }
    )
    queue_user = queue_users[user_id]
    queue_user["name"] = get_user_name(user)

    return queue_user


def clear_queue_user(user_id):
    in_queue = queue_users[user_id]["in_queue"]
    for key in ["in_queue", "last_clicked", "minutes_to_refresh"]:
        queue_users[user_id][key] = None
    active_queues[in_queue]['queue'].remove(user_id)


def kick_user_from_queue(queue_user, user_id):
    add_user_queue_event(queue_user["in_queue"], queue_user, "вылетает из очереди!", event_emoji='🥾')
    clear_queue_user(user_id)


def open_cabinet(queue_id):
    active_queues[queue_id]['cabinet']['state'] = "work"
    add_global_queue_event(queue_id, "раздача началась!", event_emoji='🚩')


def close_cabinet(queue_id):
    active_queues[queue_id]['cabinet']['state'] = "after_work"
    add_global_queue_event(queue_id, "раздача закончилась!", event_emoji='🏁')
