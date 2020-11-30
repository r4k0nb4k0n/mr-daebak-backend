
from typing import Optional

from pydantic import BaseModel

from app.models.domain.dinner_style import DinnerStyle


class DinnerStyleInCreate(BaseModel):
    name: str
    items: list


class DinnerStyleInUpdate(BaseModel):
    name: Optional[str] = None
    items: Optional[list] = None
