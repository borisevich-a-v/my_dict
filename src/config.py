from pathlib import Path

from pydantic import BaseSettings, Field

dotenv_path = Path(__file__).parents[1] / ".env"


class Settings(BaseSettings):
    token: str = Field(..., env="TG_BOT_TOKEN")
    spreadsheet_name: str
    worksheet_name: str

    class Config:
        env_file = dotenv_path
        env_file_encoding = "utf-8"


settings = Settings()
