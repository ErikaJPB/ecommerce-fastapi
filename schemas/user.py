from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    created_at: datetime

class UserCreate(UserBase):
    password: str
    

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None

class UserInDB(UserBase):
    id: int
    hashed_password: str

    class Config:
        orm_mode = True

class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True


   