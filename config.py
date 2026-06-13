"""
ARKHEIA-CPS — Configuration
Reads environment variables for database, secrets, and runtime mode.
"""
import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/arkheia_cps")

    # App
    ENV: str = os.getenv("ENV", "dev")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-in-production")
    APP_NAME: str = "ARKHEIA Contract Protection System"
    VERSION: str = "1.0.0"

    # Analysis defaults
    MAX_UPLOAD_MB: int = 20
    ALLOWED_EXTENSIONS: list = [".pdf", ".docx", ".doc"]

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
