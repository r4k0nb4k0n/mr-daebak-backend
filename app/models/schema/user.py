
from typing import Optional

from pydantic import BaseModel, EmailStr

from app.models.domain.user import User


class UserInLogin(BaseModel):
    username: EmailStr
    password: str

class UserInRegister(UserInLogin):
    address: str
    contact: str

class UserInCreate(UserInRegister):
    type: str

class UserInUpdate(BaseModel):
    password: Optional[str] = None
    address: Optional[str] = None
    contact: Optional[str] = None
    type: Optional[str] = None
    important: Optional[bool] = None

class UserWithToken(User):
    token: str

class UserInResponse(BaseModel):
    user: UserWithToken