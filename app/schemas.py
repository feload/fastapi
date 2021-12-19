from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from sqlalchemy.engine import create_engine

from app.database import Base


class PostBase(BaseModel):
    title: str
    content: str
    published: bool


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    type: str


class TokenData(BaseModel):
    id: Optional[str] = None
