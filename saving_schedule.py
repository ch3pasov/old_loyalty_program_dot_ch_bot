import json
import os
import warnings
from datetime import datetime, timezone
from apscheduler.schedulers.background import BackgroundScheduler
from global_vars import print, users, active_queues, queue_users

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

    filename = f"server/logs/{now.strftime('%Y-%m-%d')}/{now.strftime('%H_%M')}/queue_users.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(queue_users, f, ensure_ascii=False, indent=4)


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

    filename = "server/queue_users.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(queue_users, f, ensure_ascii=False, indent=4)


def restore_queue_users():
    for user_id in queue_users:
        queue_user = queue_users[user_id]
        if not queue_user["in"]:
            continue

        queue_id = queue_user["in"]["id"]
        if queue_user["in"]["type"] == "queue":
            if user_id not in active_queues[queue_id]['queue']:
                print(f"⁉️ {user_id} in_queue problem. Fixed it!")
                queue_user["in"] = None
        elif queue_user["in"]["type"] == "cabinet":
            if user_id != active_queues[queue_id]['cabinet']['state']['inside']:
                print(f"⁉️ {user_id} in_cabinet problem. Fixed it!")
                queue_user["in"] = None
        else:
            raise ValueError(f'queue_user["in"]["type"] must be "queue" or "cabinet", not {queue_user["in"]["type"]}!')


def start_saving_scheduler(verbose=True):
    restore_queue_users()
    saving_scheduler = BackgroundScheduler()

    saving_scheduler.add_job(backup_log_job, "interval", minutes=30, kwargs={"verbose": verbose}, max_instances=1, next_run_time=datetime.now())
    saving_scheduler.add_job(save_log_job, "interval", seconds=30, kwargs={"verbose": verbose}, max_instances=1)

    saving_scheduler.start()


if __name__ == "__main__":
    from pyrogram import idle

    start_saving_scheduler(verbose=True)
    idle()
