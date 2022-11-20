import json
import os
import warnings
from datetime import datetime, timezone

import lib.screen as screen
import server.server_vars
from apscheduler.schedulers.background import BackgroundScheduler
from lib.useful_lib import is_registered, seconds_from_timestamp
from pyrogram import errors

warnings.filterwarnings("ignore")

# import global_vars
# users = global_vars.users
# print(f"Я запустил schedule и импортировал users. Его id {id(users)}")


def backup_log_job(users, verbose=False):
    if verbose:
        print('backup!')
    # global users

    now = datetime.now(timezone.utc)
    filename = f"server/logs/{now.strftime('%Y-%m-%d')}/{now.strftime('%H_%M')}/users.json"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=4)


def save_log_job(users, verbose=False):
    if verbose:
        print('save!')
    # global users

    filename = "server/users.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=4)


# def test_app(app, verbose=True):
#     print('test app!')
#     app.send_message("drakedoin", "пук")

def update_user_progress(users, app, app_human, verbose=True):
    if verbose:
        print('update_user_progress!')
    # global users

    member_ids = [member.user.id for member in app.get_chat_members(server.server_vars.dot_ch_id)]
    # print(member_ids)

    for user_id in users:
        # незареганных — игнорить
        if not is_registered(user_id, users):
            continue
        # отписавшихся — выкидываем
        if int(user_id) not in member_ids:
            users[user_id]["loyality_programm"]["subscribed_since"] = None
            screen.create(app, user_id, screen.unsubscribed_from_channel_gif())
            screen.create(app, user_id, screen.unsubscribed_from_channel())
            continue

        # живых — проверяем на левелап
        user_line = users[user_id]["loyality_programm"]
        current_level = user_line["level"]
        max_level = len(server.server_vars.loyality_programm) - 1
        next_level = min(max_level, current_level + 1)

        schema_level: server.server_vars.LoyalityLevel = server.server_vars.loyality_programm[current_level]
        schema_next_level: server.server_vars.LoyalityLevel = server.server_vars.loyality_programm[next_level]

        user_exp_days = seconds_from_timestamp(user_line["subscribed_since"])/86400
        level_need_days = schema_level.days
        if user_exp_days >= level_need_days:
            # если он меня забанил — то я его тоже 🔫🔫🔫
            try:
                screen.create(app, user_id, screen.money_hidden_block_check())
            except errors.exceptions.bad_request_400.UserIsBlocked:
                print(f"{user_id} IS BLOCKED ME")
                users[user_id]["loyality_programm"]["subscribed_since"] = None
                continue

            reward = schema_level.reward
            screen.send_money(app, app_human, reward, user_id)
            users[user_id]["loyality_programm"]["level"] += 1
            users[user_id]["loyality_programm"]["money_won"] += reward

            screen.create(app, user_id, screen.level_up(
                congrats_link=next_level.congrats_link,
                congrats_text=next_level.congrats_text,
            ))


def start_scheduler(users, app, app_human, verbose=True):
    # global users

    scheduler = BackgroundScheduler()
    scheduler.add_job(backup_log_job, "interval", minutes=30, kwargs={"users": users, "verbose": verbose}, max_instances=1, next_run_time=datetime.now())
    scheduler.add_job(save_log_job, "interval", seconds=30, kwargs={"users": users, "verbose": verbose}, max_instances=1)
    # scheduler.add_job(test_app, "interval", seconds=30, kwargs={"app":app, "verbose":verbose}, max_instances=1)
    scheduler.add_job(update_user_progress, "interval", minutes=10, kwargs={"users": users, "app": app, "app_human": app_human, "verbose": verbose}, max_instances=1, next_run_time=datetime.now())
    scheduler.start()
    print(f"Я запустил start_scheduler из модуля scheduler из скрипта main и смотрю на users. Его id {id(users)}")

# if __name__ == "__main__":
#     start_scheduler(app, app_human)
