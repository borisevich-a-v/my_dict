from enum import Enum
from string import ascii_lowercase

from .errors import BusinessLogicError
from .google_sheets import SpreadSheet

PERMITTED_SYMBOLS = ascii_lowercase + " -'"
ONE_CHAR_WORDS = ["a", "i"]


class Commands(Enum):
    NEW_WORDS = "/new_words"


def process_command(command: str, storage: SpreadSheet):
    if command == Commands.NEW_WORDS.value:
        new_words = storage.get_new_words()
        return ",".join(new_words)


def check_and_normalize_word(words: str) -> str:
    if words is None:
        raise BusinessLogicError("Message does not contain text")
    words = words.strip().lower()
    for char in words:
        if char.lower() not in PERMITTED_SYMBOLS:
            raise BusinessLogicError("Message contains non eng letter")
    for word in words.split():
        if len(word) == 1 and word not in ONE_CHAR_WORDS:
            raise BusinessLogicError(f"{word} is too short")
        if len(word) > 16:
            raise BusinessLogicError(f"{word} is too long")

    return words


def get_new_words():
    ...


def process_word(text, storage):
    try:
        word = check_and_normalize_word(text)
    except BusinessLogicError as exp:
        return str(exp)
    storage.save_word(word)
    return f"`{word}` saved"
