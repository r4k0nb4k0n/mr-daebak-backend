from copy import deepcopy
from fastapi import APIRouter, Depends, HTTPException, status
from starlette.status import HTTP_401_UNAUTHORIZED
from app.database.database import db
from app.models.domain.order import Order
from app.models.schema.order import OrderInCreate, OrderInUpdate
from app.services.jwt import *
from app.services.security import *

router = APIRouter()


@router.get("/order", tags=["order"])
def read_order():
    orders = deepcopy(db.table["order"])
    return {
        "success": True,
        "orders": orders
    }


@router.get("/order/{order_id}", tags=["order"])
def read_order_specific_id(order_id):
    order_id = int(order_id)
    orderFound = [x for x in db.table["order"]
                  if x["id"] == order_id]
    if len(orderFound) < 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not found", headers={"WWW-Authenticate": "Bearer"})
    order = deepcopy(orderFound[0])
    return {
        "success": True,
        "order": order
    }


@router.post("/order", tags=["order"])
def create_order(order: OrderInCreate):
    payload = {}
    payload["id"] = len(db.table["order"])
    payload["customer_id"] = order.customer_id
    payload["cook_id"] = order.cook_id
    payload["rider_id"] = order.rider_id
    payload["date_start"] = order.date_start
    payload["date_end"] = order.date_end
    payload["status"] = order.status
    payload["address"] = order.address
    payload["contact"] = order.contact
    payload["credit_card_number"] = order.credit_card_number
    payload["order_details"] = order.order_details
    db.table["order"].append(payload)
    db.commit()
    return {
        "success": True
    }


@router.patch("/order/{order_id}", tags=["order"])
def update_order(order_id, order: OrderInUpdate):
    order_id = int(order_id)
    index = next((i for i, order in enumerate(db.table["order"])
                  if order["id"] == order_id), -1)
    if index < 0:
        raise HTTPException(status_code=404, detail="Not Found")

    if order.customer_id is not None:
        db.table["order"][index]["customer_id"] = order.customer_id
    if order.cook_id is not None:
        db.table["order"][index]["cook_id"] = order.cook_id
    if order.rider_id is not None:
        db.table["order"][index]["rider_id"] = order.rider_id
    if order.date_start is not None:
        db.table["order"][index]["date_start"] = order.date_start
    if order.date_end is not None:
        db.table["order"][index]["date_end"] = order.date_end
    if order.status is not None:
        db.table["order"][index]["status"] = order.status
    if order.address is not None:
        db.table["order"][index]["address"] = order.address
    if order.contact is not None:
        db.table["order"][index]["contact"] = order.contact
    if order.credit_card_number is not None:
        db.table["order"][index]["credit_card_number"] = order.credit_card_number
    if order.order_details is not None:
        db.table["order"][index]["order_details"] = order.order_details
    db.commit()
    return {
        "success": True
    }


@router.delete("/order/{order_id}", tags=["order"])
def delete_order(order_id):
    order_id = int(order_id)
    index = next((i for i, order in enumerate(db.table["order"])
                  if order["id"] == order_id), -1)
    if index < 0:
        raise HTTPException(status_code=404, detail="Not Found")
    del db.table["order"][index]
    db.commit()
    return {
        "success": True
    }
