
import warnings
from datetime import datetime

import lib.screen as screen
import server.server_vars
from lib.useful_lib import timestamp_now, seconds_between_timestamps
from lib.dataclasses import LoyaltyLevel
from lib.social_lib import check_if_banned_before_money, is_registered, is_member
from lib.money import send_money

from global_vars import print, app, users, common_scheduler

warnings.filterwarnings("ignore")


# 1. Удаляет всех отписавшихся от канала.
# 2. Левелапает всех, кого надо левалапнуть.
# 3. Баню, если внезапно чел заблочил бота.
def update_user_progress(verbose=True):
    if verbose:
        print('update_user_progress!')

    # member_ids = [member.user.id for member in app.get_chat_members(server.server_vars.dot_ch_id)]
    # print(member_ids)

    timestamp_now_const = timestamp_now()

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

        user_exp_days = seconds_between_timestamps(timestamp_now_const, user_line["subscribed_since"])/86400
        level_need_days = schema_level.days
        if user_exp_days >= level_need_days:
            # если он меня забанил — то я его тоже 🔫🔫🔫
            if not check_if_banned_before_money(user_id):
                continue

            reward = schema_level.reward
            send_money(reward, user_id, referer_enable=True)
            users[user_id]["loyalty_program"]["level"] += 1

            screen.create(
                app,
                user_id,
                screen.level_up(
                    congrats_link=schema_level.congrats_link,
                    congrats_text=schema_level.congrats_text,
                )
            )


def start_loyalty_scheduler(verbose=True):
    common_scheduler.add_job(
        update_user_progress,
        "interval", minutes=30, kwargs={"verbose": verbose},
        max_instances=1, next_run_time=datetime.now(),
        id="update_user_progress"
    )


if __name__ == "__main__":
    from pyrogram import idle

    start_loyalty_scheduler(verbose=True)
    idle()
