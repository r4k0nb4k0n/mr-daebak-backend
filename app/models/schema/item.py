
from typing import Optional

from pydantic import BaseModel

from app.models.domain.item import Item


class ItemInCreate(BaseModel):
    name: str
    type: str
    price: int
    stock: int


class ItemInUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    price: Optional[int] = None
    stock: Optional[int] = None
