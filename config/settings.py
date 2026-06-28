from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List


class Settings(BaseSettings):
    # Bot
    bot_token: str
    bot_name: str = "MyBot"

    # Database
    database_url: str = "sqlite+aiosqlite:///./data/bot.db"

    # Admin
    admin_ids: List[int] = []

    # App
    debug: bool = False
    log_level: str = "INFO"

    @field_validator("admin_ids", mode="before")
    @classmethod
    def parse_admin_ids(cls, v):
        if isinstance(v, str):
            return [int(x.strip()) for x in v.split(",") if x.strip()]
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()