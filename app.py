from fastapi import FastAPI
from routes.user import user
from routes.product import product
from config.db import Base, engine
from models.user import User
from models.order import Order, OrderItem
from models.product import Product

app = FastAPI()

app.include_router(user)
app.include_router(product)


# Create tables only if they do not exist
def create_tables():
    Base.metadata.create_all(bind=engine)

# Run on startup
@app.on_event("startup")
async def on_startup():
    create_tables()