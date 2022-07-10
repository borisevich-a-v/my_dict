from pathlib import Path
from typing import List

from pydantic import BaseSettings, Field

dotenv_path = Path(__file__).parents[1] / ".env"


class Settings(BaseSettings):
    token: str = Field(..., env="TG_BOT_TOKEN")
    spreadsheet_name: str
    worksheet_name: str
    allowed_users: List[str] = ["240856036"]  # my name

    class Config:
        env_file = dotenv_path
        env_file_encoding = "utf-8"


settings = Settings()
