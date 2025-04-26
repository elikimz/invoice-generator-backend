
from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    full_name: Optional[str] = None

class UserInDB(UserBase):
    id: UUID
    hashed_password: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
