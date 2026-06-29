import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from typing import Optional

load_dotenv()


class AppConfig(BaseSettings):
    ENVIRONMENT: str = "dev"
    PORT: str = "8000"
    APP_NAME: str = "UniversalRAG"
    LOG_LEVEL: str = "INFO"
    ENABLE_REQUEST_BODY_LOGGING: bool = False
    ENABLE_COMPRESSION: bool = True
    COMPRESSION_MIN_SIZE_BYTES: int = 102400
    COMPRESSION_LEVEL: int = 6

    class Config:
        extra = "allow"
        env_file = ".env"
        env_file_encoding = "utf-8"


APP_CONFIG = AppConfig()
