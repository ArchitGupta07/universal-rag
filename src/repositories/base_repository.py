from typing import Any, Dict, List, Optional, Tuple
from motor.motor_asyncio import AsyncIOMotorCollection
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class BaseRepository:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def get_many_by_query(
        self,
        query: Dict[str, Any],
        sort: Optional[List[Tuple[str, int]]] = None,
        projection: Optional[Dict] = None,
    ) -> List[Dict[str, Any]]:
        try:
            cursor = self.collection.find(query, projection)
            if sort:
                cursor = cursor.sort(sort)
            return await cursor.to_list(length=None)
        except Exception as e:
            logger.error(f"get_many_by_query error: {e}", exc_info=True)
            raise

    async def get_one_by_query(
        self,
        query: Dict[str, Any],
        projection: Optional[Dict] = None,
    ) -> Optional[Dict[str, Any]]:
        try:
            return await self.collection.find_one(query, projection)
        except Exception as e:
            logger.error(f"get_one_by_query error: {e}", exc_info=True)
            raise

    async def insert_one(self, document: Dict[str, Any]) -> Dict[str, Any]:
        try:
            result = await self.collection.insert_one(document)
            return await self.collection.find_one({"_id": result.inserted_id})
        except Exception as e:
            logger.error(f"insert_one error: {e}", exc_info=True)
            raise

    async def update_one(
        self,
        query: Dict[str, Any],
        update_data: Dict[str, Any],
        projection: Optional[Dict] = None,
    ) -> Optional[Dict[str, Any]]:
        try:
            await self.collection.update_one(query, {"$set": update_data})
            return await self.collection.find_one(query, projection)
        except Exception as e:
            logger.error(f"update_one error: {e}", exc_info=True)
            raise

    async def delete_one(self, query: Dict[str, Any]) -> bool:
        try:
            result = await self.collection.delete_one(query)
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"delete_one error: {e}", exc_info=True)
            raise

    async def aggregate(
        self, pipeline: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        try:
            cursor = self.collection.aggregate(pipeline)
            return await cursor.to_list(length=None)
        except Exception as e:
            logger.error(f"aggregate error: {e}", exc_info=True)
            raise

    async def count(self, query: Dict[str, Any] = None) -> int:
        try:
            return await self.collection.count_documents(query or {})
        except Exception as e:
            logger.error(f"count error: {e}", exc_info=True)
            raise
