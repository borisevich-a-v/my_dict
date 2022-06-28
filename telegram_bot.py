import time
import urllib
from string import ascii_lowercase
from typing import List, Optional

import requests  # type: ignore

from config import settings
from db.google_sheets import add_word_to_db
from models import HumanReadableException, Message, Update, Updates

URL = f"https://api.telegram.org/bot{settings.token}/"


def get_updates(offset: int = None) -> List[Update]:
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += f"&offset={offset}"
    response = send_request(url)
    content = response.content.decode("utf8")
    updates = Updates.parse_raw(content)
    return updates.result


# TODO: improve it
def send_request(url: str) -> requests.Response:
    print(f"Sending request {url}")
    return requests.get(url)


def get_next_update_id(updates: Optional[List[Update]]) -> Optional[int]:
    if not updates:
        return None
    last_update = max(updates, key=lambda x: int(x.update_id))
    return int(last_update.update_id) + 1


def get_new_updates(updates: Optional[List[Update]]) -> List[Update]:
    next_update_id = get_next_update_id(updates)
    return get_updates(next_update_id)


def get_word_from_message(message: Message) -> str:
    if message.text is None:
        raise HumanReadableException("Message does not contain text")
    word = message.text.strip().lower()
    if len(word.split()) != 1:
        raise HumanReadableException("Message doesn't contain single word")
    for char in word:
        if char.lower() not in ascii_lowercase:
            raise HumanReadableException("Message contains non eng letter")
    return word


def reply_message(message: Message, text: str) -> None:
    tot = urllib.parse.quote_plus(text)  # type: ignore
    url = f"{URL}sendMessage?chat_id={message.chat.id}&text={tot}&reply_to_message_id={message.message_id}"
    send_request(url)


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
            except HumanReadableException as exp:
                reply_message(update.message, str(exp))
                continue
            add_word_to_db(word)
            reply_message(update.message, word)


if __name__ == "__main__":
    main()
