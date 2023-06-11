import global_vars
from global_vars import print, active_queues
import server.server_vars
from pyrogram import filters
from lib.useful_lib import sanitize_comment_message, datetime_to_text, now_plus_n_minutes
from lib.queue_lib import (
    fast_update_comments_queue,
    add_queue_event,
    add_user_queue_event,
    update_queue,
    prerender_queue_user_and_update_name_and_get_queue_user,
    add_user_to_queue,
    update_queue_user_click,
)
from lib.social_lib import is_user_in_queue_or_cabinet
from queue_program.queue_schedule import set_check_user_scheduler_job, check_to_cabinet_pull
import re

users = global_vars.users

app_billing = global_vars.app_billing
app = global_vars.app


def start_queue_handlers():
    print("start_queue_handlers")

    @app.on_callback_query(filters.regex(r"queue\?id=(\d+)"))
    async def queue_click(client, callback_query, **kwargs):

        queue_id = re.search(r"queue\?id=(\d+)", callback_query.data).group(1)
        user_id = str(callback_query.from_user.id)

        if queue_id not in active_queues:
            callback_query.answer(
                r"🫥 Очередь не найдена ¯\_(ツ)_/¯",
                show_alert=False
            )
            return

        queue = active_queues[queue_id]
        if queue['state']['is_locked']:
            callback_query.answer(
                r"🔒 Очередь закрыта! ¯\_(ツ)_/¯",
                show_alert=False
            )
            return

        queue_order = queue["queue_order"]
        queue_delay_minutes = queue["rules"]["delay_minutes"]

        prerender_queue_user_and_update_name_and_get_queue_user(callback_query.from_user)

        queue_or_cabinet = is_user_in_queue_or_cabinet(user_id)
        if queue_or_cabinet == "cabinet":  # в кабинете
            callback_query.answer(
                "👥🚪👤 Ты уже сидишь в кабинете!",
                show_alert=False
            )
            return
        elif queue_or_cabinet == "queue" and user_id not in queue_order:
            callback_query.answer(
                "❌👥 Ты уже стоишь в другой очереди!",
                show_alert=False
            )
            return
        elif queue_or_cabinet == "queue" and user_id in queue_order:  # Уже в этой очереди, обновить время
            update_queue_user_click(user_id)

            emoji_update = "👤👥"
            to_update = False
        else:
            add_user_to_queue(user_id, queue_id)
            print(f'new in queue {queue_id}')
            cabinet = queue['cabinet']
            if cabinet:
                await check_to_cabinet_pull(queue_id)

            emoji_update = "🆕👥"
            to_update = True

        queue_or_cabinet = is_user_in_queue_or_cabinet(user_id)
        if queue_or_cabinet == "queue":
            click_deadline = now_plus_n_minutes(queue_delay_minutes)
            click_deadline_text = datetime_to_text(click_deadline)
            callback_query.answer(
                f"{emoji_update} Кликни снова до {click_deadline_text} UTC",
                show_alert=False
            )
        elif queue_or_cabinet == "cabinet":  # Заходит в очередь и сразу в кабинет
            callback_query.answer(
                "🆕🚪 Добро пожаловать в кабинет!",
                show_alert=False
            )

        if to_update:
            await update_queue(queue_id)

        set_check_user_scheduler_job(user_id)

    @app.on_message(filters.chat(server.server_vars.dot_ch_chat_id) & filters.reply)
    async def answer_comment(client, message):
        # print('message!')

        top_message_id = message.reply_to_top_message_id if message.reply_to_top_message_id else message.reply_to_message_id

        queue_ids = [active_queue_id for active_queue_id in active_queues if active_queues[active_queue_id]["id"]["chat"] == top_message_id]
        if queue_ids:
            print('new comment!')
            queue_id = queue_ids[0]

            fast_update_comments_queue(queue_id, change=1)

            if message.sender_chat:
                add_queue_event(queue_id, "кто-то\nпишет от лица канала 🤮", event_emoji='🐖💨', ignore_time=False)
                await update_queue(queue_id)
                # комменты от каналов — игнорируем
                return

            user_id = str(message.from_user.id)
            prerender_queue_user_and_update_name_and_get_queue_user(message.from_user)

            message_text_sanitized = sanitize_comment_message(message)
            if message_text_sanitized:
                comment_url = f"https://t.me/c/{(-server.server_vars.dot_ch_chat_id)%10**10}/{message.id}?thread={top_message_id}"
                event = f"[пишет]({comment_url}):\n{message_text_sanitized}"
                add_user_queue_event(queue_id, user_id, event, event_emoji='🗣', gap=' ', ignore_time=True)

            await update_queue(queue_id)
