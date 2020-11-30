from fastapi import APIRouter, Depends, HTTPException, status
from starlette.status import HTTP_401_UNAUTHORIZED
from app.database.database import db
from app.models.domain.item import Item
from app.models.schema.item import ItemInCreate, ItemInUpdate
from app.services.jwt import *
from app.services.security import *

router = APIRouter()


@router.get("/item", tags=["item"])
def read_item():
    return {
        "success": True,
        "items": db.table["item"]
    }


@router.get("/item/{item_id}", tags=["item"])
def read_item_specific_id(item_id):
    item_id = int(item_id)
    itemFound = [x for x in db.table["item"] if x["id"] == item_id]
    if len(itemFound) < 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not found", headers={"WWW-Authenticate": "Bearer"})
    return {
        "success": True,
        "item": itemFound[0]
    }


@router.post("/item", tags=["item"])
def create_item(item: ItemInCreate):
    itemFound = [x for x in db.table["item"]
                 if x["name"] == item.name]
    if len(itemFound) > 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Duplicated item name")
    payload = {}
    payload["id"] = len(db.table["item"])
    payload["name"] = item.name
    payload["type"] = item.type
    payload["price"] = item.price
    payload["stock"] = item.stock
    db.table["item"].append(payload)
    db.commit()
    return {
        "success": True
    }


@router.patch("/item/{item_id}", tags=["item"])
def update_item(item_id, item: ItemInUpdate):
    item_id = int(item_id)
    index = next((i for i, item in enumerate(db.table["item"])
                  if item["id"] == item_id), -1)
    if index < 0:
        raise HTTPException(status_code=404, detail="Not Found")

    if item.name is not None:
        db.table["item"][index]["name"] = item.name
    if item.type is not None:
        db.table["item"][index]["type"] = item.type
    if item.price is not None:
        db.table["item"][index]["price"] = item.price
    if item.stock is not None:
        db.table["item"][index]["stock"] = item.stock
    db.commit()
    return {
        "success": True
    }


@router.delete("/item/{item_id}", tags=["item"])
def delete_item(item_id):
    item_id = int(item_id)
    index = next((i for i, item in enumerate(db.table["item"])
                  if item["id"] == item_id), -1)
    if index < 0:
        raise HTTPException(status_code=404, detail="Not Found")
    del db.table["item"][index]
    db.commit()
    return {
        "success": True
    }
