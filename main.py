from pyrogram import idle
import schedule
import interface
from global_vars import print
# import logging
# import sys
app_human = interface.app_human
app = interface.app
users = interface.users

print(f"Я запустил main и смотрю на users. Его id {id(users)}")

if __name__ == '__main__':
    print("login in robot!")
    app.start()
    print("login in human!")
    app_human.start()
    schedule.start_scheduler(users, app, app_human, verbose=False)
    print(f"Я запустил name=main в main и смотрю на users. Его id {id(users)}")
    idle()
