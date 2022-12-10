from lib import screen
from lib.useful_lib import timestamp
from lib.social_lib import check_if_banned_before_money
import server.server_vars
from global_vars import app, app_billing, users, print


def send_money(
    amount, user_id,
    add_to_money_won=True,
    reply_to_message_id=None, text=None, button_text=None, debug_comment=None,
    referer_enable=False
):

    assert amount >= 0.0001, "wallet не позволяет отправлять меньше 0.0001 TON!"
    non_collision_amount = amount + int(timestamp() * 10**6) % 10**3 * 10**(-7) + int(user_id) % 10**3 * 10**(-10)
    assert non_collision_amount < 1, "МНОГО ДЕНЕГ"

    r = app_billing.get_inline_bot_results('@wallet', str(non_collision_amount))

    result = r.results[0]
    if "TON" in result.title and "BTC" not in result.title:
        # создание чека в биллинге
        updates = app_billing.send_inline_bot_result(server.server_vars.money_chat_id, r.query_id, result.id).updates
        billing_message_id = updates[0].id

        # создание дебаг-сообщения в биллинге
        app_billing.send_message(
            server.server_vars.money_chat_id,
            f"amount={amount}\nuser_id={user_id}\n{debug_comment}",
            reply_to_message_id=billing_message_id
        )
        print(f"amount={amount}\tuser_id={user_id}\t{debug_comment}")
        # отправка чека адресату
        screen.create(app, user_id, screen.money(result.send_message, text=text, button_text=button_text, reply_to_message_id=reply_to_message_id))

        if add_to_money_won:
            users[user_id]["loyalty_program"]["money_won"] += amount

        referer_amount = amount/2
        if referer_enable and referer_amount >= 0.0001 and users[user_id]["loyalty_program"]["referer_id"]:
            referer_id = users[user_id]["loyalty_program"]["referer_id"]
            if check_if_banned_before_money(referer_id, text="🪙"):
                send_money(
                    referer_amount, referer_id,
                    text=None, button_text="Бонус за реферала🫡",
                    debug_comment=f"Бонус за реферала {user_id} billing_message_id={billing_message_id}",
                    referer_enable=True
                )

    else:
        raise ValueError("BTC! СЛЕВА НАПРАВО")
