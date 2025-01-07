import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str
    
class tokenData(BaseModel):
    id: Optional[int] = None

class UserBase(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserCreate(UserBase):
    pass


class UserOutput(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime.datetime
    updated_at: datetime.datetime
    class Config:
        from_attributes = True

class userLogin(BaseModel):
    email: EmailStr
    password: str


class UserLoginOutput(UserOutput):
    access_token: str
    token_type: str
    pass
    class Config:
        from_attributes = True

