from scr.config import settings
from scr.errors import BusinessLogicError
from scr.google_sheets import SpreadSheet
from scr.telegram_bot import TelegramBot
from scr.utils import check_and_normalize_word

storage = SpreadSheet()


def main() -> None:
    bot = TelegramBot(token=settings.token)
    for update in bot.listen_updates():
        text = bot.get_text_from_update(update)
        if not text:
            continue
        try:
            word = check_and_normalize_word(text)
        except BusinessLogicError:
            continue
        storage.save_word(word)
        bot.reply_message(update.message, f"{word} saved")


if __name__ == "__main__":
    main()
