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
    is_admin: Optional[bool] = False
    

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    is_admin: Optional[bool] = None

class UserInDB(UserBase):
    id: int
    hashed_password: str
    is_admin: bool

    class Config:
        from_attributes = True

class UserOut(UserBase):
    id: int
    is_admin: bool

    class Config:
        from_attributes = True

class UserSelfUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
   