import logging
from collections import defaultdict
from datetime import date, datetime
from typing import List, Optional

import gspread
from gspread import Cell
from pydantic import BaseModel

from .config import settings
from .errors import StorageError

logger = logging.getLogger(__file__)


class Row(BaseModel):
    word: str
    added_at: datetime
    priority: int


class Table(BaseModel):
    rows: List[Row]


class SpreadSheet:
    LAST_UPDATE_DATE_CELL = (1, 2)
    type = "spreadsheet"

    def __init__(self) -> None:
        self.gc = gspread.service_account()
        self.spreadsheet = self.gc.open(settings.spreadsheet_name)
        self.worksheet = self.spreadsheet.worksheet("words")
        self.metadata = self.spreadsheet.worksheet("metadata")
        logger.info("Setup worksheet successfully")

    def get_new_words(self):
        update_date = self.get_last_update_date()
        words = self.get_words_since_date(update_date)
        self.metadata.update_cell(
            *self.LAST_UPDATE_DATE_CELL, datetime.now().strftime(settings.str_fmt)
        )
        return words

    def get_last_update_date(self) -> Optional[date]:
        last_update_date = self.metadata.cell(*self.LAST_UPDATE_DATE_CELL).value
        if not last_update_date:
            return None
        return datetime.strptime(last_update_date, settings.str_fmt).date()

    def get_words_since_date(self, date_: datetime = None):
        table = self.get_all_table()
        if not date_:
            words = [row.word for row in table.rows]
            return words

        words = []
        for row in table.rows:
            if date_ > row.added_at.date():
                continue
            words.append(row.word)
        return words

    # TODO Move to serializer and rewrite it
    def get_all_table(self):
        cells: List[Cell] = [
            cell for cell in self.worksheet.get_all_cells() if cell.value
        ]
        table = defaultdict(dict)

        for cell in cells:
            table[cell.row][cell.col] = cell.value
        table.pop(1)

        p_table = Table(rows=[])
        for row in table.values():
            p_table.rows.append(Row(word=row[1], added_at=row[2], priority=row[3]))
        return p_table

    def save_word(self, word: str, priority: int = 1) -> None:
        logger.info(f"Saving {word=} with {priority=}")
        row_to_adding = [word, str(datetime.now()), str(priority)]
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
