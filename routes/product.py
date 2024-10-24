from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from config.db import get_db
from models.product import Product as ProductModel
from schemas.product import ProductCreate, ProductUpdate, ProductOut
from models.user import User as UserModel
from utils.auth import get_current_user

product = APIRouter(prefix="/products", tags = ["products"])



# Create product
@product.post("/products", response_model=ProductOut)
async def create_product(product_data: ProductCreate, current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):

    db_product = ProductModel(
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        in_stock=product_data.in_stock)

    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


# Get products
@product.get("/products", response_model=List[ProductOut])
async def get_products(db: Session = Depends(get_db)):
    products = db.query(ProductModel).all()
    return products


# Get product by id
@product.get("/products/{product_id}", response_model=ProductOut)
async def get_product(product_id: int, db: Session = Depends(get_db)):

    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return product
    

# Update product
@product.put("/products/{product_id}", response_model=ProductOut)
async def update_product(product_id: int, product_update: ProductUpdate, current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):

     db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()

     if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

     if product_update.name is not None:
        db_product.name = product_update.name

     if product_update.description is not None:
        db_product.description = product_update.description

     if product_update.price is not None:
        db_product.price = product_update.price

     if product_update.in_stock is not None:
        db_product.in_stock = product_update.in_stock

     db.commit()
     db.refresh(db_product)

     return db_product


# Delete product
@product.delete("/products/{product_id}", response_model=dict)
async def delete_product(product_id:int, current_user:UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()

    if not db_product: 
        raise HTTPException(status_code = 404, detail="Product not found")
    
    db.delete(db_product)
    db.commit()
    
    return {"message": "Product deleted"}