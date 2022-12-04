import logging
import sys

import json

from pyrogram import Client
import server.secret as secret

fancy_stdout = logging.getLogger(__name__)
fancy_stdout.setLevel(logging.INFO)

# настройка обработчика и форматировщика для fancy_stdout

handler_logger = logging.FileHandler("sandbox.log", mode='a')
handler_fancy_stdout = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s %(levelname)s [%(filename)s:%(lineno)s] %(message)s")


# добавление форматировщика к обработчику
handler_logger.setFormatter(formatter)
handler_fancy_stdout.setFormatter(formatter)
# добавление обработчика к логгеру
fancy_stdout.addHandler(handler_logger)
fancy_stdout.addHandler(handler_fancy_stdout)

print = fancy_stdout.info

with open('server/users.json') as f:
    users = json.load(f)

with open('server/active_queues.json') as f:
    active_queues = json.load(f)

api_id = secret.api_id
api_hash = secret.api_hash

app_human = Client("account_human", api_id, api_hash)
app = Client("account_robot", api_id, api_hash)