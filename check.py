import configparser
import os
import time

from loguru import logger
from telethon import TelegramClient, errors, functions

config = configparser.ConfigParser()
config.read("config.ini")

id = config.get("default", "api_id")
hash = config.get("default", "api_hash")


if id == "UPDATE ME" or hash == "UPDATE ME":
    print("Please read the config.ini and README.md")
    input()
    exit()
else:
    id = int(id)
    client = TelegramClient("Checker", id, hash)
    client.start()


def userLookup(account):
    try:
        result = client(functions.account.CheckUsernameRequest(username=account))
        if result == True:
            logger.success(f"{account} is available")
            file = open(output(), "a")
            file.write("%s\n" % (account))
            file.close()
        else:
            logger.info(f"{account} is not available")
    except errors.FloodWaitError as fW:
        logger.warning(f"Hit the rate limit, waiting {fW.seconds} seconds")
        time.sleep(fW.seconds)
    except errors.UsernameInvalidError:
        logger.info("Username is invalid")
    except errors.rpcbaseerrors.BadRequestError as bR:
        logger.error(f"Error: {bR.message}")


def getWords():
    words = []
    delay = config.get("default", "delay")
    path = os.path.join("word_lists", config.get("default", "wordList"))
    if path is not None:
        file = open(path, "r", encoding="utf-8-sig")
        words = file.read().split("\n")
        file.close()
    else:
        print("Word list not found.")

    for i in range(len(words)):
        name = words[i]
        userLookup(name)
        time.sleep(int(delay))
        # delay to deter hitting rate limit
        # https://core.telegram.org/bots/faq#my-bot-is-hitting-limits-how-do-i-avoid-this
    print("All done")
    input("Press enter to exit...")


def output():
    return config.get("default", "outPut", fallback="AVAILABLE.txt")


def main():
    print("""
▄▄▄█████▓▓█████  ██▓    ▓█████   ▄████  ██▀███   ▄▄▄       ███▄ ▄███▓
▓  ██▒ ▓▒▓█   ▀ ▓██▒    ▓█   ▀  ██▒ ▀█▒▓██ ▒ ██▒▒████▄    ▓██▒▀█▀ ██▒
▒ ▓██░ ▒░▒███   ▒██░    ▒███   ▒██░▄▄▄░▓██ ░▄█ ▒▒██  ▀█▄  ▓██    ▓██░
░ ▓██▓ ░ ▒▓█  ▄ ▒██░    ▒▓█  ▄ ░▓█  ██▓▒██▀▀█▄  ░██▄▄▄▄██ ▒██    ▒██ 
  ▒██▒ ░ ░▒████▒░██████▒░▒████▒░▒▓███▀▒░██▓ ▒██▒ ▓█   ▓██▒▒██▒   ░██▒
  ▒ ░░   ░░ ▒░ ░░ ▒░▓  ░░░ ▒░ ░ ░▒   ▒ ░ ▒▓ ░▒▓░ ▒▒   ▓▒█░░ ▒░   ░  ░
    ░     ░ ░  ░░ ░ ▒  ░ ░ ░  ░  ░   ░   ░▒ ░ ▒░  ▒   ▒▒ ░░  ░      ░
  ░         ░     ░ ░      ░   ░ ░   ░   ░░   ░   ░   ▒   ░      ░   
            ░  ░    ░  ░   ░  ░      ░    ░           ░  ░       ░   
                                                                     
                        - Username Checker -
        Make sure to read the config.ini and README.md on github
    bulk checking may result in false positives and longer wait times
        """)
    print(
        "1 = Enter username manually\n2 = Read a list of usernames from the word_lists folder"
    )
    set = ["1", "2"]
    option = input("Select your option: ")
    while True:
        if str(option) in set:
            if option == set[0]:
                name = input("Enter a username: ")
                userLookup(name)
            else:
                getWords()
                break
        else:
            option = input("1 or 2 ... Please!: ")


main()
