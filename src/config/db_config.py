from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class DBConfig(BaseSettings):
    DATABASE_URI: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "universal_rag_db"
    MONGODB_MAX_POOL_SIZE: int = 200
    MONGODB_MIN_POOL_SIZE: int = 10
    MONGODB_MAX_IDLE_TIME_MS: int = 30000
    MONGODB_CONNECT_TIMEOUT_MS: int = 10000
    MONGODB_SOCKET_TIMEOUT_MS: int = 60000
    MONGODB_SERVER_SELECTION_TIMEOUT_MS: int = 15000

    class Config:
        extra = "allow"
        env_file = ".env"
        env_file_encoding = "utf-8"


DB_CONFIG = DBConfig()
