from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from starlette.status import HTTP_401_UNAUTHORIZED
from app.database.database import db
from app.models.domain.user import User
from app.models.schema.user import UserInCreate, UserInRegister, UserInUpdate
from app.services.jwt import *
from app.services.security import *

router = APIRouter()


async def get_current_user(token: str = Depends(oauth2_scheme)):
    username = get_username_from_token(token)
    userFound = [x for x in db.table["user"] if x["username"] == username]
    if len(userFound) < 1:
        raise credentials_exception
    return userFound[0]


@router.get("/user/me", tags=["user"])
async def auth_me(current_user: User = Depends(get_current_user)):
    return {
        "success": True,
        "user": current_user
    }


@router.post("/token", tags=["user"])
def sign_in(formData: OAuth2PasswordRequestForm = Depends()):
    userFound = [x for x in db.table["user"] if x["username"] ==
                 formData.username and verify_password(formData.password, x["hashed_password"])]
    if len(userFound) < 1:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Bad email or password", headers={"WWW-Authenticate": "Bearer"})
    access_token = create_jwt_token(userFound[0]["username"])
    return {
        "success": True,
        "access_token": access_token,
        "token_type": "bearer",
        "user": userFound[0]
    }


@router.post("/signup", tags=["user"])
def sign_up(user: UserInRegister):
    userFound = [x for x in db.table["user"] if x["username"] == user.username]
    if len(userFound) > 0:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)
    payload = {}
    payload["id"] = len(db.table["user"])
    payload["username"] = user.username
    payload["hashed_password"] = get_password_hash(user.password)
    payload["address"] = user.address
    payload["contact"] = user.contact
    payload["type"] = "customer"
    payload["important"] = False
    db.table["user"].append(payload)
    db.commit()
    return {
        "success": True
    }


@router.get("/user", tags=["user"])
def read_user(current_user: User = Depends(get_current_user)):
    currentUser = current_user
    if currentUser["type"] == "customer":
        return {
            "success": True,
            "user": currentUser
        }
    else:
        return {
            "success": True,
            "users": db.table["user"]
        }


@router.get("/user/{user_id}", tags=["user"])
def read_user_specific_id(user_id, current_user: User = Depends(get_current_user)):
    user_id = int(user_id)
    userFound = [x for x in db.table["user"] if x["id"] == user_id]
    if len(userFound) < 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not found", headers={"WWW-Authenticate": "Bearer"})
    currentUser = current_user
    if currentUser["type"] != "customer" or (currentUser["type"] == "customer" and currentUser["id"] == user_id):
        return {
            "success": True,
            "user": userFound[0]
        }
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="unauthorized", headers={"WWW-Authenticate": "Bearer"})


@router.post("/user", tags=["user"])
def create_user(user: UserInCreate, current_user: User = Depends(get_current_user)):
    if current_user["type"] == "customer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="unauthorized", headers={"WWW-Authenticate": "Bearer"})
    userFound = [x for x in db.table["user"]
                 if x["username"] == user.email]
    if len(userFound) > 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Duplicated email")
    payload = {}
    payload["id"] = len(db.table["user"])
    payload["username"] = user.email
    payload["hashed_password"] = get_password_hash(user.password)
    payload["address"] = user.address
    payload["contact"] = user.contact
    payload["type"] = "customer"
    payload["important"] = False
    db.table["user"].append(payload)
    db.commit()
    return {
        "success": True
    }


@router.patch("/user/{user_id}", tags=["user"])
def update_user(user_id, user: UserInUpdate, current_user: User = Depends(get_current_user)):
    user_id = int(user_id)
    index = next((i for i, item in enumerate(db.table["user"])
                  if item["id"] == user_id), -1)
    if index < 0:
        raise HTTPException(status_code=404, detail="Not Found")

    if user.password is not None:
        db.table["user"][index]["hashed_password"] = get_password_hash(
            user.password)
    if user.address is not None:
        db.table["user"][index]["address"] = user.address
    if user.contact is not None:
        db.table["user"][index]["contact"] = user.contact
    if user.type is not None:
        db.table["user"][index]["type"] = user.type
    if user.important is not None:
        db.table["user"][index]["important"] = user.important
    db.commit()
    return {
        "success": True
    }


@router.delete("/user/{user_id}", tags=["user"])
def delete_user(user_id, current_user: User = Depends(get_current_user)):
    user_id = int(user_id)
    if current_user["type"] == "customer" and current_user["id"] != user_id:
        raise HTTPException(statue_code=403, detail="Forbidden")
    index = next((i for i, item in enumerate(db.table["user"])
                  if item["id"] == user_id), -1)
    if index < 0:
        raise HTTPException(status_code=404, detail="Not Found")

    del db.table["user"][index]
    db.commit()
    return {
        "success": True
    }
