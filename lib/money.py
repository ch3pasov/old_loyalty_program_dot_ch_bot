from lib import screen
from lib.useful_lib import timestamp
import server.server_vars
import global_vars

users = global_vars.users


def send_money(
    app, app_human, amount, user_id,
    reply_to_message_id=None, text=None, button_text=None, debug_comment=None,
    referer_enable=False, referer_billing_message_id=None
):
    global users

    assert amount >= 0.0001, "wallet не позволяет отправлять меньше 0.0001 TON!"
    non_collision_amount = amount + int(timestamp() * 10**6) % 10**3 * 10**(-7) + int(user_id) % 10**3 * 10**(-10)
    assert non_collision_amount < 1, "МНОГО ДЕНЕГ"

    r = app_human.get_inline_bot_results('@wallet', str(non_collision_amount))

    result = r.results[0]
    if "TON" in result.title and "BTC" not in result.title:
        # создание чека в биллинге
        updates = app_human.send_inline_bot_result(server.server_vars.money_chat_id, r.query_id, result.id).updates
        billing_message_id = updates[0].id

        # создание дебаг-сообщения в биллинге
        app_human.send_message(
            server.server_vars.money_chat_id,
            f"amount={amount}\nuser_id={user_id}\n{debug_comment}",
            reply_to_message_id=billing_message_id
        )

        # отправка чека адресату
        screen.create(app, user_id, screen.money(result.send_message, text=text, button_text=button_text, reply_to_message_id=reply_to_message_id))

        if referer_enable and amount/2 >= 0.0001:
            pass
            # send_money(
            #     app, app_human, amount, user_id,
            #     reply_to_message_id=None, text=None, button_text=None, debug_comment=None,
            #     referer_enable=False, referer_billing_message_id=None
            # )

    else:
        raise ValueError("BTC! СЛЕВА НАПРАВО")
