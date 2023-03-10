import global_vars
from global_vars import print, active_queues, queue_local_scheduler
import server.server_vars
from pyrogram import filters
from lib.useful_lib import sanitize_comment_message, datetime_to_text, now_plus_n_minutes
from lib.queue_lib import (
    create_queue,
    fast_update_comments_queue,
    add_user_queue_event,
    update_queue,
    prerender_queue_user_and_update_name_and_get_queue_user,
    add_user_to_queue,
    update_queue_user_click,
    delete_queue
)
from lib.social_lib import is_user_in_queue_or_cabinet
import lib.screen as screen
from queue_program.queue_schedule import set_check_user_scheduler_job, check_to_cabinet_pull
import re

users = global_vars.users
user_referers = global_vars.user_referers

app_billing = global_vars.app_billing
app = global_vars.app


def start_queue_handlers():
    print("start_queue_handlers")

    @app.on_callback_query(filters.regex(r"queue\?id=(\d+)"))
    def queue_click(client, callback_query, **kwargs):

        queue_id = re.search(r"queue\?id=(\d+)", callback_query.data).group(1)
        user_id = str(callback_query.from_user.id)

        if queue_id not in active_queues:
            callback_query.answer(
                r"🫥 Очередь не найдена ¯\_(ツ)_/¯",
                show_alert=False
            )
            return

        queue = active_queues[queue_id]["queue_order"]
        queue_delay_minutes = active_queues[queue_id]["rules"]["delay_minutes"]

        queue_user = prerender_queue_user_and_update_name_and_get_queue_user(callback_query.from_user)

        queue_or_cabinet = is_user_in_queue_or_cabinet(user_id)
        if queue_or_cabinet:
            if queue_or_cabinet == "cabinet":
                callback_query.answer(
                    "👥🚪👤 Ты уже сидишь в кабинете!",
                    show_alert=False
                )
                return

            if user_id not in queue:
                callback_query.answer(
                    "❌👥 Ты уже стоишь в другой очереди!",
                    show_alert=False
                )
                return
            else:
                update_queue_user_click(user_id)
                click_deadline = now_plus_n_minutes(queue_delay_minutes)
                click_deadline_text = datetime_to_text(click_deadline)
                callback_query.answer(
                    f"👤👥 Кликни снова до {click_deadline_text} ({queue_delay_minutes} мин)",
                    show_alert=False
                )
        else:
            add_user_to_queue(user_id, queue_id)
            print(f'new in queue {queue_id}')
            cabinet = active_queues[queue_id]['cabinet']
            if cabinet:
                check_to_cabinet_pull(queue_id)

            click_deadline = now_plus_n_minutes(queue_delay_minutes)
            click_deadline_text = datetime_to_text(click_deadline)

            if queue_user["in"]["type"] == "queue":
                callback_query.answer(
                    f"🆕👥 Кликни снова до {click_deadline_text} ({queue_delay_minutes} мин)",
                    show_alert=False
                )
            else:
                callback_query.answer(
                    "🆕🚪 Добро пожаловать в кабинет!",
                    show_alert=False
                )

            update_queue(queue_id)

        set_check_user_scheduler_job(queue_local_scheduler, user_id)
        # print(queue_local_scheduler.get_job(user_id))

    @app.on_message(filters.chat(server.server_vars.dot_ch_chat_id) & filters.reply)
    def answer_comment(client, message):
        # print('message!')

        top_message_id = message.reply_to_top_message_id if message.reply_to_top_message_id else message.reply_to_message_id

        queue_ids = [active_queue_id for active_queue_id in active_queues if active_queues[active_queue_id]["id"]["chat"] == top_message_id]
        if queue_ids:
            print('new comment!')
            queue_id = queue_ids[0]

            fast_update_comments_queue(queue_id, change=1)

            if message.sender_chat:
                update_queue(queue_id)
                # комменты от каналов — игнорируем
                return

            user_id = str(message.from_user.id)
            prerender_queue_user_and_update_name_and_get_queue_user(message.from_user)

            message_text_sanitized = sanitize_comment_message(message)
            if message_text_sanitized:
                comment_url = f"https://t.me/c/{(-server.server_vars.dot_ch_chat_id)%10**10}/{message.id}?thread={top_message_id}"
                event = f"[пишет]({comment_url}):\n{message_text_sanitized}"
                add_user_queue_event(queue_id, user_id, event, event_emoji='🗣', gap=' ', ignore_time=True)

            update_queue(queue_id)

    def test_sum(param1: int, param2: int = 123) -> int:
        """Тестовая функция, даёт сумму"""
        return param1+param2
    commands = {
        test_sum.__name__: test_sum,
        create_queue.__name__: create_queue,
        delete_queue.__name__: delete_queue
    }

    @app.on_message(filters.command(["admin"]) & filters.chat(server.server_vars.creator_id))
    def answer_admin_command(client, message):
        print(message.command)
        if len(message.command) > 1:
            command_name = message.command[1]
            args = map(int, message.command[2:])
            if command_name in commands:
                command = commands[command_name]

                command_output = None
                errors = None
                try:
                    command_output = command(*args)
                    is_success = True
                except Exception as e:
                    errors = e
                    is_success = False
                screen.create(
                    client,
                    message.chat.id,
                    screen.queue_admin_run(
                        command_output=command_output,
                        is_success=is_success,
                        errors=errors
                    )
                )
                return

        return screen.create(client, message.chat.id, screen.queue_admin_help(commands))
