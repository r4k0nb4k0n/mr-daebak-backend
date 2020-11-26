from os import access
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from Database import Database
from User import User

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()
db = Database("db.json")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class UserPydantic(BaseModel):
    email: str
    address: Optional[str] = None
    contact: Optional[str] = None
    type: Optional[str] = None
    important: Optional[str] = None


class UserSignin(BaseModel):
    email: str
    password: str


class UserSignUp(BaseModel):
    email: str
    password: str
    address: str
    contact: str


class UserCreate(BaseModel):
    email: str
    password: str
    address: str
    contact: str
    type: str


class UserUpdate(BaseModel):
    password: Optional[str] = None
    address: Optional[str] = None
    contact: Optional[str] = None
    type: Optional[str] = None
    important: Optional[bool] = None


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    userFound = [x for x in db.table["user"] if x["email"] == username]
    if len(userFound) < 1:
        raise credentials_exception
    return userFound[0]


@app.get("/auth")
async def auth(current_user: UserPydantic = Depends(get_current_user)):
    return {"success": True, "user": current_user}


@app.post("/token")
def signin(formData: OAuth2PasswordRequestForm = Depends()):
    userFound = [x for x in db.table["user"] if x["email"] ==
                 formData.username and pwdContext.verify(formData.password, x["hashedPassword"])]
    if len(userFound) < 1:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Bad email or password", headers={"WWW-Authenticate": "Bearer"})

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": userFound[0]["email"]}
    if access_token_expires:
        expire = datetime.utcnow() + access_token_expires
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return {
        "success": True,
        "access_token": encoded_jwt,
        "token_type": "bearer",
        "user": userFound[0]
    }


@app.post("/signup")
def signup(user: UserSignUp):
    userFound = [x for x in db.table["user"] if x["email"] == user.email]
    if len(userFound) > 0:
        raise HTTPException(status_code=401, detail="Duplicated email")
    payload = {}
    payload["id"] = len(db.table["user"])
    payload["email"] = user.email
    payload["hashedPassword"] = pwdContext.hash(user.password)
    payload["address"] = user.address
    payload["contact"] = user.contact
    payload["type"] = "customer"
    payload["important"] = False
    pUser = User(payload)
    db.table["user"].append(pUser.data)
    db.commit()
    return {
        "success": True
    }


@app.get("/user")
def readUser(current_user: UserPydantic = Depends(get_current_user)):
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


@app.get("/user/{user_id}")
def readUserSpecificId(user_id, current_user: UserPydantic = Depends(get_current_user)):
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


@app.post("/user")
def createUser(user: UserCreate, current_user: UserPydantic = Depends(get_current_user)):
    currentUser = current_user
    if currentUser["type"] == "customer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="unauthorized", headers={"WWW-Authenticate": "Bearer"})
    userFound = [x for x in db.table["user"] if x["email"] == user.email]
    if len(userFound) > 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Duplicated email")
    payload = {}
    payload["id"] = len(db.table["user"])
    payload["email"] = user.email
    payload["hashedPassword"] = pwdContext.hash(user.password)
    payload["address"] = user.address
    payload["contact"] = user.contact
    payload["type"] = "customer"
    payload["important"] = False
    pUser = User(payload)
    db.table["user"].append(pUser.data)
    db.commit()
    return {
        "success": True
    }


@app.patch("/user/{user_id}")
def updateUser(user_id, user: UserUpdate, current_user: UserPydantic = Depends(get_current_user)):
    user_id = int(user_id)
    currentUser = current_user
    index = next((i for i, item in enumerate(db.table["user"])
                  if item["id"] == user_id), -1)
    if index < 0:
        raise HTTPException(status_code=404, detail="Not Found")

    if user.password is not None:
        pUser = User(db.table["user"][index])
        pUser.setNewPassword(user.password, pwdContext)
        db.table["user"][index].hashedPassword = pUser.data.hashedPassword
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


@app.delete("/user/{user_id}")
def deleteUser(user_id, current_user: UserPydantic = Depends(get_current_user)):
    user_id = int(user_id)
    currentUser = current_user
    if currentUser["type"] == "customer" and currentUser["id"] != user_id:
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
