from typing import Dict, Any, List
from bson import ObjectId
from src.repositories.item_repository import ItemRepository
from src.utils.exceptions import EntityNotFoundError, ValidationError
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class ItemService:
    def __init__(self, item_repository: ItemRepository):
        self.item_repository = item_repository

    def _serialize(self, doc: Dict) -> Dict:
        if doc and "_id" in doc:
            doc["id"] = str(doc.pop("_id"))
        return doc

    async def get_all(self) -> List[Dict[str, Any]]:
        docs = await self.item_repository.get_many_by_query({})
        return [self._serialize(d) for d in docs]

    async def get_by_id(self, item_id: str) -> Dict[str, Any]:
        if not ObjectId.is_valid(item_id):
            raise EntityNotFoundError("Item", item_id, "Invalid ID format")
        doc = await self.item_repository.get_one_by_query({"_id": ObjectId(item_id)})
        if not doc:
            raise EntityNotFoundError("Item", item_id)
        return self._serialize(doc)

    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if not data.get("name"):
            raise ValidationError("Item name is required", field="name")
        existing = await self.item_repository.find_by_name(data["name"])
        if existing:
            raise ValidationError(f"Item with name '{data['name']}' already exists")
        doc = await self.item_repository.insert_one(data)
        return self._serialize(doc)

    async def update(self, item_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        if not ObjectId.is_valid(item_id):
            raise EntityNotFoundError("Item", item_id, "Invalid ID format")
        query = {"_id": ObjectId(item_id)}
        doc = await self.item_repository.get_one_by_query(query)
        if not doc:
            raise EntityNotFoundError("Item", item_id)
        update_data = {k: v for k, v in data.items() if v is not None}
        updated = await self.item_repository.update_one(query, update_data)
        return self._serialize(updated)

    async def delete(self, item_id: str) -> bool:
        if not ObjectId.is_valid(item_id):
            raise EntityNotFoundError("Item", item_id, "Invalid ID format")
        query = {"_id": ObjectId(item_id)}
        doc = await self.item_repository.get_one_by_query(query)
        if not doc:
            raise EntityNotFoundError("Item", item_id)
        return await self.item_repository.delete_one(query)
