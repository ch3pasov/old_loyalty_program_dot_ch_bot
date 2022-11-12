from pyrogram import Client, filters

import server.secret as secret
api_id = secret.api_id
api_hash = secret.api_hash

import global_vars
users = global_vars.users

from useful_lib import is_member
import server.server_vars

import screen

with Client("account_robot", api_id, api_hash) as app:
    print(is_member(app, server.server_vars.dot_ch_id, "drakedoin"))