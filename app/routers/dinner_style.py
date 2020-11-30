from copy import deepcopy
from fastapi import APIRouter, Depends, HTTPException, status
from starlette.status import HTTP_401_UNAUTHORIZED
from app.database.database import db
from app.models.domain.dinner_style import DinnerStyle
from app.models.schema.dinner_style import DinnerStyleInCreate, DinnerStyleInUpdate
from app.services.jwt import *
from app.services.security import *

router = APIRouter()


@router.get("/dinner_style", tags=["dinner_style"])
def read_dinner_style():
    dinnerStyles = deepcopy(db.table["dinner_style"])
    for i in range(len(dinnerStyles)):
        dinnerStyles[i]["price"] = 0
        for item in dinnerStyles[i]["items"]:
            price = [x for x in db.table["item"]
                     if x["id"] == item["id"]][0]["price"]
            dinnerStyles[i]["price"] += price * item["amount"]
    return {
        "success": True,
        "dinner_styles": dinnerStyles
    }


@router.get("/dinner_style/{dinner_style_id}", tags=["dinner_style"])
def read_dinner_style_specific_id(dinner_style_id):
    dinner_style_id = int(dinner_style_id)
    dinnerStyleFound = [x for x in db.table["dinner_style"]
                        if x["id"] == dinner_style_id]
    if len(dinnerStyleFound) < 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not found", headers={"WWW-Authenticate": "Bearer"})
    dinnerStyle = deepcopy(dinnerStyleFound[0])
    dinnerStyle["price"] = 0
    for item in dinnerStyle["items"]:
        price = [x for x in db.table["item"]
                 if x["id"] == item["id"]][0]["price"]
        dinnerStyle["price"] += price * item["amount"]
    return {
        "success": True,
        "dinner_style": dinnerStyle
    }


@router.post("/dinner_style", tags=["dinner_style"])
def create_dinner_style(dinner_style: DinnerStyleInCreate):
    dinnerStyleFound = [x for x in db.table["dinner_style"]
                        if x["name"] == dinner_style.name]
    if len(dinnerStyleFound) > 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Duplicated dinner_style name")
    payload = {}
    payload["id"] = len(db.table["dinner_style"])
    payload["name"] = dinner_style.name
    payload["items"] = dinner_style.items
    db.table["dinner_style"].append(payload)
    db.commit()
    return {
        "success": True
    }


@router.patch("/dinner_style/{dinner_style_id}", tags=["dinner_style"])
def update_dinner_style(dinner_style_id, dinner_style: DinnerStyleInUpdate):
    dinner_style_id = int(dinner_style_id)
    index = next((i for i, dinner_style in enumerate(db.table["dinner_style"])
                  if dinner_style["id"] == dinner_style_id), -1)
    if index < 0:
        raise HTTPException(status_code=404, detail="Not Found")

    if dinner_style.name is not None:
        db.table["dinner_style"][index]["name"] = dinner_style.name
    if dinner_style.items is not None:
        db.table["dinner_style"][index]["items"] = dinner_style.items
    db.commit()
    return {
        "success": True
    }


@router.delete("/dinner_style/{dinner_style_id}", tags=["dinner_style"])
def delete_dinner_style(dinner_style_id):
    dinner_style_id = int(dinner_style_id)
    index = next((i for i, dinner_style in enumerate(db.table["dinner_style"])
                  if dinner_style["id"] == dinner_style_id), -1)
    if index < 0:
        raise HTTPException(status_code=404, detail="Not Found")
    del db.table["dinner_style"][index]
    db.commit()
    return {
        "success": True
    }
