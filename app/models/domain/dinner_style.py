from pydantic import BaseModel


class DinnerStyle(BaseModel):
    id: int
    name: str
    items: list
