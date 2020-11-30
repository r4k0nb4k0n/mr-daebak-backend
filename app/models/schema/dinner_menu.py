
from typing import Optional

from pydantic import BaseModel

from app.models.domain.dinner_menu import DinnerMenu


class DinnerMenuInCreate(BaseModel):
    name: str
    items: list


class DinnerMenuInUpdate(BaseModel):
    name: Optional[str] = None
    items: Optional[list] = None
