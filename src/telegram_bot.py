import time
import traceback
import urllib
from typing import Generator, Optional

from .config import settings
from .errors import TelegramBotError
from .models import Message, Update, Updates
from .utils import send_request


class TelegramBot:
    def __init__(self, token):
        self.url = f"https://api.telegram.org/bot{token}/"
        self.last_update_id: int = -1

    def check_user_name(self, update: Update) -> bool:
        if not update.message or not update.message.from_user:
            print(f"bad msg: {update}")
            return False
        if str(update.message.from_user.id) in settings.allowed_users:
            return True
        for _ in range(30):
            user_name = update.message.from_user.first_name
            self.reply_message(update.message, f"{user_name} shall not pass!")
        return False

    def listen_updates(self) -> Generator[Update, None, None]:
        while True:
            try:
                updates = self.get_updates(self.last_update_id + 1)
                if not updates.ok:
                    raise TelegramBotError("The updates results is not `ok`")
                for update in sorted(updates.result, key=lambda x: int(x.update_id)):
                    self.last_update_id = update.update_id
                    if not self.check_user_name(update):
                        continue
                    yield update
                time.sleep(0.1)
            except Exception as exp:
                print(traceback.format_exc())
                raise TelegramBotError("Can't read") from exp

    def get_updates(self, offset: int = 0) -> Updates:
        url = self.url + "getUpdates?timeout=100"
        if offset:
            url += f"&offset={offset}"
        response = send_request(url)
        content = response.content.decode("utf8")
        return Updates.parse_raw(content)

    def reply_message(self, message: Message, text: str) -> None:
        tot = urllib.parse.quote_plus(text)  # type: ignore
        url = f"{self.url}sendMessage?chat_id={message.chat.id}&text={tot}&reply_to_message_id={message.message_id}"
        send_request(url)

    def get_text_from_update(self, update: Update) -> Optional[str]:
        if not update.message or not update.message.text:
            print(f"Update#{update.update_id} does not contain text")
            return None
        return update.message.text
