from pydantic import BaseModel
from typing import Optional


class CreateItemRequest(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    in_stock: bool = True


class UpdateItemRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    in_stock: Optional[bool] = None
