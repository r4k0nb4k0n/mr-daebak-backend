from pydantic import BaseModel


class Item(BaseModel):
    id: int
    name: str
    type: str
    price: int
    stock: int
