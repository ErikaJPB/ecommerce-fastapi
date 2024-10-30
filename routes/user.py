from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from passlib.context import CryptContext
from config.db import get_db
from models.user import User as UserModel
from schemas.user import UserCreate, UserOut, UserSelfUpdate, UserUpdate
from utils.auth import get_current_user, is_admin_user

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
        is_admin=user.is_admin,
        created_at=datetime.utcnow()
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Get all users, admin only
@user.get("/", response_model=list[UserOut], dependencies=[Depends(is_admin_user)])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(UserModel).all()
    return users

# Get user by id, admin can see all, user can only see their own
@user.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: int, current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if not db_user: 
        raise HTTPException(status_code=404, detail="User not found")
    
    if db_user.id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to view this user")

    return db_user

# Update user profile
@user.put("/profile", response_model=UserOut)
async def update_own_profile(
    user_update: UserSelfUpdate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_user = db.query(UserModel).filter(UserModel.id == current_user.id).first()

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


# Admin route to update any user profile.
@user.put("/{user_id}", response_model=UserOut)
async def admin_update_user(
    user_id: int,
    user_update: UserUpdate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can update other users")

    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    
    if user_update.is_admin is not None:
        db_user.is_admin = user_update.is_admin
    if user_update.first_name is not None:
        db_user.first_name = user_update.first_name
    if user_update.last_name is not None:
        db_user.last_name = user_update.last_name
    if user_update.password is not None:
        db_user.hashed_password = hash_password(user_update.password)

    db.commit()
    db.refresh(db_user)

    return db_user


# Delete own profile
@user.delete("/profile", response_model=dict)
async def delete_own_profile(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_user = db.query(UserModel).filter(UserModel.id == current_user.id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return {"message": "Your account has been deleted"}


# Admin only route to delete any user by id
@user.delete("/{user_id}", response_model=dict, dependencies=[Depends(is_admin_user)])
async def admin_delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if not db_user: 
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted"}



