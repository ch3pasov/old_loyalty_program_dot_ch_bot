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
        "id": {
            "channel": channel_message_id,
            "chat": chat_message_id
        },
        "queue_order": [],
        "rules": {
            "delay_minutes": 15
        },
        "show": {
            "last_n_events": [],
            "comments": {
                "cnt": 0,
                "fingerprint": "👀"
            }
        },
        "cabinet": None
    }

    screen.update(app, server.server_vars.dot_ch_id, channel_message_id, screen.queue_state(queue_id))
    screen.create(app, server.server_vars.dot_ch_chat_id, screen.queue_first_comment(queue_id, chat_message_id))

    active_queues[queue_id] = queue
    print(f"Очередь {queue_id} создана!")


def update_queue(queue_id):
    channel_message_id = int(active_queues[queue_id]["id"]["channel"])
    try:
        screen.update(app, server.server_vars.dot_ch_id, channel_message_id, screen.queue_state(queue_id))
    except errors.exceptions.bad_request_400.MessageNotModified:
        print(f'{queue_id} ничего не изменилось')


def slow_update_comments_queue(queue_id):
    comments_cnt = app_billing.get_discussion_replies_count(
        server.server_vars.dot_ch_chat_id,
        message_id=int(active_queues[queue_id]["id"]["chat"])
    )

    active_queues[queue_id]["show"]["comments"]["cnt"] = comments_cnt


def fast_update_comments_queue(queue_id, change=1):
    active_queues[queue_id]["show"]["comments"]["cnt"] += change
    active_queues[queue_id]["show"]["comments"]["fingerprint"] = emoji_fingerprint(active_queues[queue_id]["show"]["comments"]["cnt"])


def add_queue_event(queue_id, event, event_emoji=''):
    new_event = f"`{now_text()}` {event_emoji} {event}"
    active_queues[queue_id]["show"]["last_n_events"] = (active_queues[queue_id]["show"]["last_n_events"]+[new_event])[-10:]


def add_user_queue_event(queue_id, queue_user, event, event_emoji=''):
    add_queue_event(queue_id, f"{queue_user['name']} {event}", event_emoji=event_emoji)


def add_global_queue_event(queue_id, event, event_emoji=''):
    add_queue_event(queue_id, event, event_emoji=event_emoji)
    app.send_message(
        server.server_vars.dot_ch_chat_id,
        f"{event_emoji} {event}",
        reply_to_message_id=active_queues[queue_id]["id"]["chat"]
    )
    fast_update_comments_queue(queue_id, change=1)


def prerender_queue_user_and_update_name_and_get_queue_user(user):
    user_id = str(user.id)
    queue_users.setdefault(
        user_id,
        {
            "in": None,
            "name": None
        }
    )
    queue_user = queue_users[user_id]
    queue_user["name"] = get_user_name(user)

    return queue_user


def clear_queue_user(user_id):
    queue_user = queue_users[user_id]

    assert queue_user["in"]["type"] == "queue", f'queue_user["in"]["type"] must be "queue", not {queue_user["in"]["type"]}'
    queue_id = queue_user["in"]["id"]
    queue_user["in"] = None
    active_queues[queue_id]['queue_order'].remove(user_id)


def kick_user_from_queue(queue_user, user_id, to_update_queue=False):
    assert queue_user["in"]["type"] == "queue", f'queue_user["in"]["type"] must be "queue", not {queue_user["in"]["type"]}'
    queue_id = queue_user["in"]["id"]

    add_user_queue_event(queue_id, queue_user, "вылетает из очереди!", event_emoji='🥾')
    clear_queue_user(user_id)
    if to_update_queue:
        update_queue(queue_id)
