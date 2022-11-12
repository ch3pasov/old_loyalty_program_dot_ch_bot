import json
import os
from datetime import datetime, timezone
from apscheduler.schedulers.background import BackgroundScheduler
import warnings
warnings.filterwarnings("ignore")

import global_vars
users = global_vars.users
import server.server_vars

from useful_lib import is_registered, seconds_from_timestamp, send_money
import screen

def backup_log_job(verbose=False):
    if verbose:
        print('backup!')
    global users

    now = datetime.now(timezone.utc)
    filename = f"server/logs/{now.strftime('%Y-%m-%d')}/{now.strftime('%H_%M')}/users.json"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=4)


def save_log_job(verbose=False):
    if verbose:
        print('save!')
    global users

    filename = f"server/users.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=4)


# def test_app(app, verbose=True):
#     print('test app!')
#     app.send_message("drakedoin", "пук")

def update_user_progress(app, app_human, verbose=True):
    if verbose:
        print('update_user_progress!')
    global users

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
        schema_level = server.server_vars.loyality_programm[user_line["level"]]
        user_exp_days = seconds_from_timestamp(user_line["subscribed_since"])/86400
        level_need_days = schema_level["days"]
        if user_exp_days >= level_need_days:
            reward = schema_level["reward"]
            send_money(app, app_human, reward, user_id)
            users[user_id]["loyality_programm"]["level"] += 1
            users[user_id]["loyality_programm"]["money_won"] += reward

            screen.create(app, user_id, screen.level_up())


def start_scheduler(app, app_human, verbose=True):
    global users

    scheduler = BackgroundScheduler()
    scheduler.add_job(backup_log_job, "interval", minutes=30, kwargs={"verbose":verbose}, max_instances=1, next_run_time=datetime.now())
    scheduler.add_job(save_log_job, "interval", seconds=30, kwargs={"verbose":verbose}, max_instances=1)
    # scheduler.add_job(test_app, "interval", seconds=30, kwargs={"app":app, "verbose":verbose}, max_instances=1)
    scheduler.add_job(update_user_progress, "interval", minutes=10, kwargs={"app": app, "app_human": app_human, "verbose":verbose}, max_instances=1, next_run_time=datetime.now())
    scheduler.start()