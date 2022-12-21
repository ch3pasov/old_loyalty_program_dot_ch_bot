import json
import os
import warnings
from datetime import datetime, timezone

import lib.screen as screen
import server.server_vars
from apscheduler.schedulers.background import BackgroundScheduler
from lib.useful_lib import seconds_from_timestamp, random_datetime
from lib.dataclasses import LoyaltyLevel
from lib.social_lib import check_if_banned_before_money, is_registered, is_member
from lib.money import send_money, money_drop

from global_vars import print, app, users, active_queues

warnings.filterwarnings("ignore")


# бэкап в папку server/logs/
def backup_log_job(verbose=False):
    if verbose:
        print('backup!')

    now = datetime.now(timezone.utc)
    filename = f"server/logs/{now.strftime('%Y-%m-%d')}/{now.strftime('%H_%M')}/users.json"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=4)
    filename = f"server/logs/{now.strftime('%Y-%m-%d')}/{now.strftime('%H_%M')}/active_queues.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(active_queues, f, ensure_ascii=False, indent=4)


# сохранение нынешнего users в server/users.json
def save_log_job(verbose=False):
    if verbose:
        print('save!')
    # global users

    filename = "server/users.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=4)
    filename = "server/active_queues.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(active_queues, f, ensure_ascii=False, indent=4)


# 1. Удаляет всех отписавшихся от канала.
# 2. Левелапает всех, кого надо левалапнуть.
# 3. Баню, если внезапно чел заблочил бота.
def update_user_progress(users, verbose=True):
    if verbose:
        print('update_user_progress!')
    # global users

    # member_ids = [member.user.id for member in app.get_chat_members(server.server_vars.dot_ch_id)]
    # print(member_ids)

    for user_id in users:
        # незареганных — игнорить
        if not is_registered(user_id):
            continue
        # отписавшихся — выкидываем
        if not is_member(server.server_vars.dot_ch_id, int(user_id)):
            users[user_id]["loyalty_program"]["subscribed_since"] = None
            screen.create(app, user_id, screen.unsubscribed_from_channel_emoji())
            screen.create(app, user_id, screen.unsubscribed_from_channel())
            continue

        # живых — проверяем на левелап
        user_line = users[user_id]["loyalty_program"]
        current_level = user_line["level"]
        schema_level: LoyaltyLevel = server.server_vars.loyalty_program[current_level]

        user_exp_days = seconds_from_timestamp(user_line["subscribed_since"])/86400
        level_need_days = schema_level.days
        if user_exp_days >= level_need_days:
            # если он меня забанил — то я его тоже 🔫🔫🔫
            if not check_if_banned_before_money(user_id):
                continue

            reward = schema_level.reward
            send_money(reward, user_id, referer_enable=True)
            users[user_id]["loyalty_program"]["level"] += 1

            screen.create(app, user_id, screen.level_up(
                congrats_link=schema_level.congrats_link,
                congrats_text=schema_level.congrats_text,
            ))


def drop_scheduler(dot_ch_chat_id, money_drop_message_id, scheduler):
    print("Start drop_scheduler!")
    from datetime import timedelta
    for i in range(server.server_vars.money_drop_drops):
        run_date = random_datetime(timedelta(minutes=server.server_vars.money_drop_period_minutes))
        print(run_date)
        scheduler.add_job(
            money_drop,
            'date',
            run_date=run_date,
            kwargs={
                "dot_ch_chat_id": dot_ch_chat_id,
                "money_drop_message_id": money_drop_message_id,
                "amount": server.server_vars.money_drop_amount
            }
        )


def test_app(app, verbose=True):
    print('test app!')
    app.send_message("drakedoin", "пук")


def start_scheduler(verbose=True):
    # global users
    scheduler = BackgroundScheduler()

    scheduler.add_job(backup_log_job, "interval", minutes=30, kwargs={"verbose": verbose}, max_instances=1, next_run_time=datetime.now())
    scheduler.add_job(save_log_job, "interval", seconds=30, kwargs={"verbose": verbose}, max_instances=1)
    scheduler.add_job(update_user_progress, "interval", minutes=2, kwargs={"users": users, "verbose": verbose}, max_instances=1, next_run_time=datetime.now())

    scheduler.add_job(
        drop_scheduler, "interval", minutes=server.server_vars.money_drop_period_minutes,
        kwargs={
            "dot_ch_chat_id": server.server_vars.dot_ch_chat_id,
            "money_drop_message_id": server.server_vars.money_drop_message_id,
            "scheduler": scheduler
        }, max_instances=1, next_run_time=datetime.now()
    )

    scheduler.start()
    print(f"Я запустил start_scheduler из модуля scheduler и смотрю на users. Его id {id(users)}")


if __name__ == "__main__":
    from pyrogram import idle

    print(f"[дебаг] Я запустил schedule напрямую и импортировал users. Его id {id(users)}")
    start_scheduler(verbose=True)
    idle()
