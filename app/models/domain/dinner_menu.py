from pydantic import BaseModel


class DinnerMenu(BaseModel):
    id: int
    name: str
    items: list
