from pydantic import BaseModel


class OrderDetail(BaseModel):
    id: int
    order_id: int
    dinner_menu: dict
    dinner_style: dict
