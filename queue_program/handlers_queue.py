from pyrogram import filters
from lib.useful_lib import now_text, sanitize_comment_message
from lib.queue_lib import add_event_queue, update_queue, fast_update_comments_queue
from global_vars import app, active_queues, print
import server.server_vars


@app.on_callback_query(filters.regex(r"queue\?id=(\d+)"))
def answer(client, callback_query, **kwargs):
    import re

    queue_id = re.search(r"queue\?id=(\d+)", callback_query.data).group(1)
    user_id = str(callback_query.from_user.id)
    # print(callback_query.from_user.id, callback_query.data, callback_query.id)
    # print(kwargs)

    event = f"{now_text()}: `{user_id}` нажал на `{queue_id}`"
    callback_query.answer(
        f"{event}",
        show_alert=False
    )

    add_event_queue(queue_id, event)

    queue = active_queues[queue_id]["queue"]
    if user_id not in queue:
        queue.append(user_id)

    update_queue(queue_id)


@app.on_message(filters.chat(server.server_vars.dot_ch_chat_id) & filters.reply)
def answer_comment(client, message):
    top_message_id = message.reply_to_top_message_id if message.reply_to_top_message_id else message.reply_to_message_id

    queue_ids = [active_queue_id for active_queue_id in active_queues if active_queues[active_queue_id]["chat_message_id"] == top_message_id]
    if queue_ids:
        queue_id = queue_ids[0]

        user_id = str(message.from_user.id)

        message_text_sanitized = sanitize_comment_message(message)

        print(f"message_text_sanitized {message_text_sanitized}")

        event = f"{now_text()}: `{user_id}` написал коммент: {message_text_sanitized}"
        add_event_queue(queue_id, event)

        fast_update_comments_queue(queue_id, change=1)
        update_queue(queue_id)
