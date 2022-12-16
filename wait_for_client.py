from os.path import exists
from settings import TELEGRAM_SESSION_NAME
from time import sleep

if __name__ == '__main__':
    session_file_name = f"{TELEGRAM_SESSION_NAME}.session" if not TELEGRAM_SESSION_NAME.endswith(
        ".session") else TELEGRAM_SESSION_NAME
    if exists(session_file_name):
        print("Session file already exists")
    else:
        while not exists(session_file_name):
            sleep(0.1)
        print("Session file created, waiting for user to enter phone number and login")
        sleep(60)
