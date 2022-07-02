import time

from scr.errors import CustomException
from scr.google_sheets import SpreadSheet
from scr.telegram_bot import get_new_updates, get_word_from_message, reply_message

storage = SpreadSheet()


def main() -> None:
    updates = None
    while True:
        updates = get_new_updates(updates)
        if not updates:
            time.sleep(0.1)
            continue

        for update in updates:
            if update.message is None:
                continue
            try:
                word = get_word_from_message(update.message)
            except CustomException as exp:
                reply_message(update.message, str(exp))
                continue
            storage.save_word(word)
            reply_message(update.message, word)


if __name__ == "__main__":
    main()
