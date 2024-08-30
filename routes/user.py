from fastapi import APIRouter
from config.db import conn
from models.user import users

user = APIRouter()


@user.get("/user")
async def get_users():
    return conn.execute(users.select()).fetchall()