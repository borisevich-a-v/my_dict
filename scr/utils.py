from string import ascii_lowercase

import requests  # type: ignore

from scr.errors import BusinessLogicError


# TODO: improve it
def send_request(url: str) -> requests.Response:
    print(f"Sending request {url}")
    return requests.get(url)


def check_and_normalize_word(word: str) -> str:
    if word is None:
        raise BusinessLogicError("Message does not contain text")
    word = word.strip().lower()
    for char in word:
        if char.lower() not in ascii_lowercase:
            raise BusinessLogicError("Message contains non eng letter")
    return word
