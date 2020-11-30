from pydantic import BaseModel
from typing import Optional


class Order(BaseModel):
    id: int
    customer_id: int
    cook_id: Optional[int] = None
    rider_id: Optional[int] = None
    date_start: str
    date_end: Optional[str] = None
    status: str
    address: str
    contact: str
    credit_card_number: str
    order_details: list
