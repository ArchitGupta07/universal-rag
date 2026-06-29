from fastapi import APIRouter, Request
from typing import Dict, Any, List
from src.containers import ApplicationContainer as Container
from src.services.item import ItemService
from src.models.request.item import CreateItemRequest, UpdateItemRequest
from src.utils.logger import setup_logger
from dependency_injector.wiring import inject, Provide

logger = setup_logger(__name__)


class ItemController:

    @inject
    def __init__(
        self,
        item_service: ItemService = Provide[Container.services.item_service],
    ):
        self.item_service = item_service
        self.router = APIRouter()
        self.setup_routes()

    def setup_routes(self):
        self.router.get("", summary="List all items")(self.get_all)
        self.router.get("/{item_id}", summary="Get item by ID")(self.get_by_id)
        self.router.post("", status_code=201, summary="Create item")(self.create)
        self.router.put("/{item_id}", summary="Update item")(self.update)
        self.router.delete("/{item_id}", status_code=204, summary="Delete item")(self.delete)

    async def get_all(self, request: Request) -> List[Dict[str, Any]]:
        return await self.item_service.get_all()

    async def get_by_id(self, item_id: str, request: Request) -> Dict[str, Any]:
        return await self.item_service.get_by_id(item_id)

    async def create(self, body: CreateItemRequest, request: Request) -> Dict[str, Any]:
        return await self.item_service.create(body.model_dump())

    async def update(
        self, item_id: str, body: UpdateItemRequest, request: Request
    ) -> Dict[str, Any]:
        return await self.item_service.update(item_id, body.model_dump())

    async def delete(self, item_id: str, request: Request) -> None:
        await self.item_service.delete(item_id)
