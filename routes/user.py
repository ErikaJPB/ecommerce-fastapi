from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from passlib.context import CryptContext
from config.db import get_db
from models.user import User as UserModel
from schemas.user import UserCreate, UserOut, UserUpdate

user = APIRouter(prefix="/users", tags = ["users"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Create user
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

# Get users
@user.get("/users", response_model=list[UserOut])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(UserModel).all()
    return users

# Get user by id
@user.get("/users/{user_id}", response_model=UserOut)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if not db_user: 
        raise HTTPException(status_code=404, detail="User not found")

    return db_user

# Update user
@user.put("/users/{user_id}", response_model=UserOut)
async def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
   db_user = db.query(UserModel).filter(UserModel.id == user_id).first() 

   if not db_user: 
        raise HTTPException(status_code=404, detail="User not found")
   
   if user_update.first_name is not None: 
       db_user.first_name = user_update.first_name

   if user_update.last_name is not None:
       db_user.last_name = user_update.last_name

   if user_update.password is not None:
       db_user.hashed_password = hash_password(user_update.password) 

       db.commit()
       db.refresh(db_user)

       return db_user

# Delete user
@user.delete("/users/{user_id}", response_model=dict)
async def delete_user(user_id:int, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if not db_user: 
        raise HTTPException(status_code = 404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted"}


