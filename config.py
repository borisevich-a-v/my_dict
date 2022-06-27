from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    token: str = Field(..., env="TG_BOT_TOKEN")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
