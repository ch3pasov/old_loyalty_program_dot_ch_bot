from pyrogram import idle
import schedule
import interface
# import logging
# import sys
app_human = interface.app_human
app = interface.app
users = interface.users
print(f"Я запустил main и смотрю на users. Его id {id(users)}")

# path_out = 'stdout.log'
# sys.stdout = open(path_out, "a")
# path_err = 'stderr.log'
# sys.stderr = open(path_err, 'a')

# # create logger
# logger = logging.getLogger("logging_tryout2")
# logger.setLevel(logging.DEBUG)

# # create console handler and set level to debug
# ch = logging.StreamHandler()
# ch.setLevel(logging.DEBUG)

# # create formatter
# formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s")

# # add formatter to ch
# ch.setFormatter(formatter)

# # add ch to logger
# logger.addHandler(ch)

# # "application" code
# logger.debug("debug message")
# logger.info("info message")
# logger.warn("warn message")
# logger.error("error message")
# logger.critical("critical message")

if __name__ == '__main__':
    print("login in robot!")
    app.start()
    print("login in human!")
    app_human.start()
    schedule.start_scheduler(users, app, app_human, verbose=False)
    print(f"Я запустил name=main в main и смотрю на users. Его id {id(users)}")
    idle()
