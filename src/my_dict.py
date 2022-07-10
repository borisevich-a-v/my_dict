from string import ascii_lowercase

from .errors import BusinessLogicError


def check_and_normalize_word(word: str) -> str:
    if word is None:
        raise BusinessLogicError("Message does not contain text")
    word = word.strip().lower()
    for char in word:
        if char.lower() not in ascii_lowercase:
            raise BusinessLogicError("Message contains non eng letter")
    return word


def process_word(text, storage):
    try:
        word = check_and_normalize_word(text)
    except BusinessLogicError as exp:
        return str(exp)
    storage.save_word(word)
    return f"{word} saved"
