from copy import deepcopy
from fastapi import APIRouter, Depends, HTTPException, status
from starlette.status import HTTP_401_UNAUTHORIZED
from app.database.database import db
from app.models.domain.dinner_menu import DinnerMenu
from app.models.schema.dinner_menu import DinnerMenuInCreate, DinnerMenuInUpdate
from app.services.jwt import *
from app.services.security import *

router = APIRouter()


@router.get("/dinner_menu", tags=["dinner_menu"])
def read_dinner_menu():
    dinnerMenus = deepcopy(db.table["dinner_menu"])
    for i in range(len(dinnerMenus)):
        dinnerMenus[i]["price"] = 0
        for item in dinnerMenus[i]["items"]:
            price = [x for x in db.table["item"]
                     if x["id"] == item["id"]][0]["price"]
            dinnerMenus[i]["price"] += price * item["amount"]
    return {
        "success": True,
        "dinner_menus": dinnerMenus
    }


@router.get("/dinner_menu/{dinner_menu_id}", tags=["dinner_menu"])
def read_dinner_menu_specific_id(dinner_menu_id):
    dinner_menu_id = int(dinner_menu_id)
    dinnerMenuFound = [x for x in db.table["dinner_menu"]
                       if x["id"] == dinner_menu_id]
    if len(dinnerMenuFound) < 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not found", headers={"WWW-Authenticate": "Bearer"})
    dinnerMenu = deepcopy(dinnerMenuFound[0])
    dinnerMenu["price"] = 0
    for item in dinnerMenu["items"]:
        price = [x for x in db.table["item"]
                 if x["id"] == item["id"]][0]["price"]
        dinnerMenu["price"] += price * item["amount"]
    return {
        "success": True,
        "dinner_menu": dinnerMenu
    }


@router.post("/dinner_menu", tags=["dinner_menu"])
def create_dinner_menu(dinner_menu: DinnerMenuInCreate):
    dinnerMenuFound = [x for x in db.table["dinner_menu"]
                       if x["name"] == dinner_menu.name]
    if len(dinnerMenuFound) > 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Duplicated dinner_menu name")
    payload = {}
    payload["id"] = len(db.table["dinner_menu"])
    payload["name"] = dinner_menu.name
    payload["items"] = dinner_menu.items
    db.table["dinner_menu"].append(payload)
    db.commit()
    return {
        "success": True
    }


@router.patch("/dinner_menu/{dinner_menu_id}", tags=["dinner_menu"])
def update_dinner_menu(dinner_menu_id, dinner_menu: DinnerMenuInUpdate):
    dinner_menu_id = int(dinner_menu_id)
    index = next((i for i, dinner_menu in enumerate(db.table["dinner_menu"])
                  if dinner_menu["id"] == dinner_menu_id), -1)
    if index < 0:
        raise HTTPException(status_code=404, detail="Not Found")

    if dinner_menu.name is not None:
        db.table["dinner_menu"][index]["name"] = dinner_menu.name
    if dinner_menu.items is not None:
        db.table["dinner_menu"][index]["items"] = dinner_menu.items
    db.commit()
    return {
        "success": True
    }


@router.delete("/dinner_menu/{dinner_menu_id}", tags=["dinner_menu"])
def delete_dinner_menu(dinner_menu_id):
    dinner_menu_id = int(dinner_menu_id)
    index = next((i for i, dinner_menu in enumerate(db.table["dinner_menu"])
                  if dinner_menu["id"] == dinner_menu_id), -1)
    if index < 0:
        raise HTTPException(status_code=404, detail="Not Found")
    del db.table["dinner_menu"][index]
    db.commit()
    return {
        "success": True
    }
