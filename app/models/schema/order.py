from typing import Optional
from pydantic import BaseModel
from app.models.domain.order import Order


class OrderInCreate(BaseModel):
    customer_id: int
    cook_id: int
    rider_id: int
    date_start: str
    date_end: str
    status: str
    address: str
    contact: str
    credit_card_number: str
    order_details: list


class OrderInUpdate(BaseModel):
    customer_id: Optional[int] = None
    cook_id: Optional[int] = None
    rider_id: Optional[int] = None
    date_start: Optional[str] = None
    date_end: Optional[str] = None
    status: Optional[str] = None
    address: Optional[str] = None
    contact: Optional[str] = None
    credit_card_number: Optional[str] = None
    order_details: Optional[list] = None
