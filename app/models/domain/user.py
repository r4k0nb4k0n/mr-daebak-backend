from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    username: EmailStr
    hashed_password: str
    address: str
    contact: str
    type: str
    important: bool
