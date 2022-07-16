from src.config import settings
from src.google_sheets import SpreadSheet
from src.my_dict import Commands, process_command, process_word
from src.telegram_bot import TelegramBot

storage = SpreadSheet()
bot = TelegramBot(token=settings.token)


def main() -> None:
    for update in bot.listen_updates():
        if update.message.text in [c.value for c in Commands]:
            reply_message = process_command(update.message.text, storage)
            bot.reply_message(update.message, reply_message)
            continue

        text = bot.get_text_from_update(update)
        reply = process_word(text, storage)
        bot.reply_message(update.message, reply)


if __name__ == "__main__":
    main()
