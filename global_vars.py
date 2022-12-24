import logging
import sys

import json

from pyrogram import Client
import server.secret.secret as secret

formatter = logging.Formatter('%(asctime)s %(levelname)s [%(filename)s:%(lineno)s] %(message)s')
handler_fancy_stdout = logging.StreamHandler(sys.stdout)
handler_logger = logging.FileHandler("server/common.log", mode='a')
handler_fancy_stdout.setFormatter(formatter)
handler_logger.setFormatter(formatter)
# Корневой логгер. Должен ловить все ошибки и писать в файл.
root = logging.getLogger()
root.setLevel(logging.WARNING)
root.addHandler(handler_fancy_stdout)
root.addHandler(handler_logger)
# Логгер для красивого принта. Почему он работает, не смотря на то, что root отлавливает только WARNING — не знаю.
fancy_stdout = logging.getLogger(__name__)
fancy_stdout.setLevel(logging.INFO)
print = fancy_stdout.info

with open('server/users.json') as f:
    users = json.load(f)

with open('server/active_queues.json') as f:
    active_queues = json.load(f)

with open('server/queue_users.json') as f:
    queue_users = json.load(f)

api_id = secret.api_id
api_hash = secret.api_hash

app_billing = Client("server/secret/account_billing", api_id, api_hash)
app = Client("server/secret/account_robot", api_id, api_hash)

print("login in robot!")
app.start()
print("login in billing!")
app_billing.start()

user_referers = {}
bot_username = app.get_me().username
