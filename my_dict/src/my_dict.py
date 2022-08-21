from collections import defaultdict
from enum import Enum
from string import ascii_lowercase
from urllib.parse import urljoin

import requests

from .config import settings
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
    try:
        phonetic, meanings = get_word_information(text)
        response = f"{phonetic}\n{parse_meanings(meanings)}"
    except:
        response = f"`{word}` saved"
    return response


def get_word_information(word):
    if ' ' in word:
        raise BusinessLogicError("Word has not to contain space")
    word_url = urljoin(settings.word_definition_api, word)
    response = requests.get(word_url).json()
    phonetic = response[0]["phonetic"]
    meanings = response[0]["meanings"]

    return phonetic, meanings


def parse_meanings(meanings):
    result = defaultdict(list)
    for i, meaning in enumerate(meanings):
        if i > 5:
            break
        for definition_number, definition in enumerate(meaning["definitions"], 1):
            if len(result[meaning['partOfSpeech']]) > 2:
                break

            result[meaning['partOfSpeech']].append(f"{definition_number}. {definition['definition']}")

    text = []
    for part_of_speach, definitions in result.items():
        definitions = '\n'.join(definitions)
        text.append(f"{part_of_speach.upper()}: \n{definitions}")

    return '\n\n'.join(text)
