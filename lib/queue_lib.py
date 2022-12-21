import json
import server.server_vars
from global_vars import active_queues, app, app_billing, print
from pyrogram import errors
import lib.screen as screen
from lib.useful_lib import emoji_fingerprint


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
        "comments_cnt": 0,
        "comments_fingerprint": "👀"
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
        print('ничего не изменилось')


def add_event_queue(queue_id, event):
    active_queues[queue_id]["last_n_events"] = (active_queues[queue_id]["last_n_events"]+[event])[-5:]


def slow_update_comments_queue(queue_id):
    comments_cnt = app_billing.get_discussion_replies_count(server.server_vars.dot_ch_chat_id, message_id=active_queues[queue_id]["chat_message_id"])

    active_queues[queue_id]["comments_cnt"] = comments_cnt


def fast_update_comments_queue(queue_id, change=1):
    active_queues[queue_id]["comments_cnt"] += change
    active_queues[queue_id]["comments_fingerprint"] = emoji_fingerprint()
