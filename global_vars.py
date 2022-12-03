import json

with open('server/users.json') as f:
    users = json.load(f)

with open('server/active_queues.json') as f:
    active_queues = json.load(f)

from pyrogram import Client

import server.secret as secret
api_id = secret.api_id
api_hash = secret.api_hash

app_human = Client("account_human", api_id, api_hash)
app = Client("account_robot", api_id, api_hash)
