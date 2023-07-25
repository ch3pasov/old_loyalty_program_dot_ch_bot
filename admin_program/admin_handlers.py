import global_vars
from global_vars import print, common_scheduler
import server.server_vars
from pyrogram import filters
from lib.queue_lib import create_queue
from lib.queue_actions_lib import queue_delete
from lib.q_md_lib import queue_money_drop_by_type, get_qmd_params_type_keys, get_qmd_params_type  # , queue_money_drop
import lib.screen as screen
from lib.money import money_drop
from saving_schedule import reread_all_job
import json

users = global_vars.users

app = global_vars.app


def test_sum(param1: str, param2: str = 'string_two') -> str:
    """Тестовая функция, даёт сумму строк"""
    return param1+param2


def test_sum_int(param1: int, param2: int = 1) -> int:
    """Тестовая функция, даёт сумму чисел"""
    param1 = int(param1)
    param2 = int(param2)
    return test_sum(param1, param2)


def get_all_jobs():
    """Получить список всех работ common_scheduler"""
    return f"{json.dumps([(item.id, item.name) for item in common_scheduler.get_jobs()], indent=4)}"


commands = {
    test_sum.__name__: test_sum,
    test_sum_int.__name__: test_sum_int,
    create_queue.__name__: create_queue,
    queue_delete.__name__: queue_delete,
    # queue_money_drop.__name__: queue_money_drop,
    queue_money_drop_by_type.__name__: queue_money_drop_by_type,
    money_drop.__name__: money_drop,
    reread_all_job.__name__: reread_all_job,
    get_qmd_params_type_keys.__name__: get_qmd_params_type_keys,
    get_qmd_params_type.__name__: get_qmd_params_type,
    get_all_jobs.__name__: get_all_jobs
}


def start_admin_handlers():
    print("start_admin_handlers")

    @app.on_message(filters.command(["admin"]) & filters.chat(server.server_vars.creator_id))
    def answer_admin_command(client, message):
        print(message.command)
        if len(message.command) > 1:
            command_name = message.command[1]
            args = message.command[2:]
            if command_name in commands:
                command = commands[command_name]

                command_output = None
                errors = None
                excpetion_except_pyrogram = (
                    AttributeError,
                    ArithmeticError,
                    EOFError,
                    NameError,
                    LookupError,
                    StopIteration,
                    OSError,
                    TypeError,
                    ValueError
                )
                try:
                    print('try!')
                    command_output = command(*args)
                    is_success = True
                except excpetion_except_pyrogram as e:
                    print('except!')
                    errors = e
                    is_success = False
                # command_output = command(*args)
                # is_success = True
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
