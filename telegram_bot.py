from typing import List, Optional

import requests

from config import settings
from models import Update, Updates

URL = f"https://api.telegram.org/bot{settings.token}/"


def get_updates(offset: int = None) -> List[Update]:
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += f"&offset={offset}"
    response = requests.get(url)
    content = response.content.decode("utf8")
    updates = Updates.parse_raw(content)
    return updates.result


def get_last_update_id(updates: List[Update]) -> int:
    update_ids = []
    for update in updates:
        update_ids.append(int(update.update_id))
    return max(update_ids)


def get_new_updates(updates: Optional[List[Update]]) -> List[Update]:
    if updates is None:
        updates = []
    last_update_id = get_last_update_id(updates) + 1
    return get_updates(last_update_id)


def echo_all(updates: List[Update]) -> None:
    for update in updates:
        if update.message is not None and update.message.text is not None:
            text = update.message.text
            chat = update.message.chat.id
            print(text)


def main() -> None:
    updates = None
    while True:
        updates = get_new_updates(updates)
        if updates:
            echo_all(updates)


if __name__ == "__main__":
    main()
