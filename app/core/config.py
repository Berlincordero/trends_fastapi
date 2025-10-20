# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    SECRET_KEY: str = "change-me"
    ACCESS_TOKEN_EXPIRE_MIN: int = 1440
    DATABASE_URL: str = "postgresql+psycopg://postgres:12345@127.0.0.1:5432/trends"
    MEDIA_DIR: str = "./media"
    ALLOWED_ORIGINS: str = "*"
    REDIS_URL: str | None = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def allow_origins_list(self) -> List[str]:
        if self.ALLOWED_ORIGINS == "*":
            return ["*"]
        return [o.strip() for o in self.ALLOWED_ORIGINS.split(",") if o.strip()]

settings = Settings()
