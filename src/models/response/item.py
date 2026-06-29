from pydantic import BaseModel
from typing import Optional


class ItemResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    price: float
    in_stock: bool


class ItemListResponse(BaseModel):
    items: list[ItemResponse]
    total: int
