import datetime
import logging

import gspread

from .config import settings
from .errors import StorageError

logger = logging.getLogger(__file__)


class SpreadSheet:
    type = "spreadsheet"

    def __init__(self) -> None:
        self.gc = gspread.service_account()
        self.spreadsheet = self.gc.open(settings.spreadsheet_name)
        self.worksheet = self.spreadsheet.worksheet(settings.worksheet_name)
        logger.info("Setup worksheet successfully")

    def save_word(self, word: str, priority: int = 1, *args, **kwargs) -> None:
        logger.info(f"Saving {word=} with {priority=}")
        row_to_adding = [word, str(datetime.datetime.now()), str(priority)]
        response = self.worksheet.append_row(
            row_to_adding, include_values_in_response=True
        )
        if not response:
            raise StorageError("The word is not saved")
        logger.info(f"{word=}, {priority=} saved")


if __name__ == "__main__":
    s = SpreadSheet()
    for st in [str(i) for i in range(100)]:
        s.save_word(st)
