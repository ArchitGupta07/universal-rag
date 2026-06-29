from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from src.config.db_config import DB_CONFIG
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class DatabaseManager:
    def __init__(self):
        self.client: AsyncIOMotorClient = None
        self.db = None

    def connect_db(self):
        self.client = AsyncIOMotorClient(
            DB_CONFIG.DATABASE_URI,
            maxPoolSize=DB_CONFIG.MONGODB_MAX_POOL_SIZE,
            minPoolSize=DB_CONFIG.MONGODB_MIN_POOL_SIZE,
            maxIdleTimeMS=DB_CONFIG.MONGODB_MAX_IDLE_TIME_MS,
            connectTimeoutMS=DB_CONFIG.MONGODB_CONNECT_TIMEOUT_MS,
            socketTimeoutMS=DB_CONFIG.MONGODB_SOCKET_TIMEOUT_MS,
            serverSelectionTimeoutMS=DB_CONFIG.MONGODB_SERVER_SELECTION_TIMEOUT_MS,
        )
        self.db = self.client[DB_CONFIG.DATABASE_NAME]
        logger.info(f"Connected to MongoDB: {DB_CONFIG.DATABASE_NAME}")

    async def close_db(self):
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed.")

    def get_collection(self, collection_name: str) -> AsyncIOMotorCollection:
        if self.db is None:
            raise RuntimeError("Database not initialized. Call connect_db() first.")
        return self.db[collection_name]


db_manager = DatabaseManager()
