import global_vars
from global_vars import print
import server.server_vars
from pyrogram import filters
from lib.queue_lib import (
    create_queue,
)
from lib.q_md_lib import queue_money_drop, generate_queue_params
import lib.screen as screen
from lib.money import money_drop

users = global_vars.users

app = global_vars.app


def test_sum(param1: int, param2: int = 123) -> int:
    """Тестовая функция, даёт сумму"""
    return param1+param2


commands = {
    test_sum.__name__: test_sum,
    create_queue.__name__: create_queue,
    # queue_delete_int.__name__: queue_delete_int,
    queue_money_drop.__name__: queue_money_drop,
    generate_queue_params.__name__: generate_queue_params,
    money_drop.__name__: money_drop
}


def start_admin_handlers():
    print("start_admin_handlers")

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
