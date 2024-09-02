from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from passlib.context import CryptContext
from config.db import get_db
from models.user import User as UserModel
from schemas.user import UserCreate, UserOut

user = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

@user.post("/users", response_model=UserOut)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)

    db_user = UserModel(
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        hashed_password=hashed_password,
        created_at=datetime.utcnow()
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@user.get("/users", response_model=list[UserOut])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(UserModel).all()
    return users