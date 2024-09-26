from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from config.db import get_db
from models.cart import Cart as CartModel, CartItem as CartItemModel
from models.product import Product as ProductModel
from schemas.cart import CartCreate,  CartOut, CartItemCreate, CartItemOut, CartItemUpdate


cart = APIRouter(prefix="/carts", tags=["carts"])


# Create cart
@cart.post("/", response_model=CartOut)
async def create_cart(cart_data: CartCreate, db: Session = Depends(get_db)):
    db_cart = CartModel(
        user_id=cart_data.user_id
    )
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)

    for item_data in cart_data.items:
        product = db.query(ProductModel).filter(ProductModel.id == item_data.product_id).first()

        if not product:
         raise HTTPException(status_code=404, detail=f"Product {item_data.product_id} not found")
    
        cart_item = CartItemModel(
        cart_id = db_cart.id,
        product_id = item_data.product_id,
        quantity = item_data.quantity
    )

        db.add(cart_item)
        
    db.commit()
    db.refresh(cart_item)

    return db_cart


# Get cart
@cart.get("/{user_id}", response_model=CartOut)
async def get_cart(user_id: int, db: Session = Depends(get_db)):
    db_cart = db.query(CartModel).filter(CartModel.user_id == user_id).first()

    if not db_cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    return db_cart

# Add item to an existing cart
@cart.post("/{cart_id}/items", response_model=CartItemOut)
async def add_item_to_cart(cart_id: int, item_data: CartItemCreate, db: Session = Depends(get_db)):
    db_cart = db.query(CartModel).filter(CartModel.id == cart_id).first()

    if not db_cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    product = db.query(ProductModel).filter(ProductModel.id == item_data.product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail=f"Product {item_data.product_id} not found")
    

    cart_item = CartItemModel(
        cart_id = db_cart.id,
        product_id = item_data.product_id,
        quantity = item_data.quantity
    )

    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)

    return cart_item

# Update cart item
@cart.put("/{cart_id}/items/{item_id}", response_model=CartOut)
async def update_cart_item(cart_id: int, item_id: int, item_data: CartItemUpdate, db: Session = Depends(get_db)):
    
    cart_item = db.query(CartItemModel).filter(CartItemModel.id == item_id, CartItemModel.cart_id == cart_id).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    
    if item_data.quantity is not None:
        cart_item.quantity = item_data.quantity

    db.commit()
    db.refresh(cart_item)

    
    db_cart = db.query(CartModel).filter(CartModel.id == cart_id).first()

    if not db_cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    return db_cart


#  Remove item from cart
@cart.delete("/{cart_id}/items/{item_id}", response_model=dict)
async def remove_cart_item(cart_id: int, item_id: int, db: Session = Depends(get_db)):
    cart_item = db.query(CartItemModel).filter(CartItemModel.id == item_id, CartItemModel.cart_id == cart_id).first()

    if not  cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(cart_item)
    db.commit()
    return {"message": "The item has been removed from the cart"}
    

# Delete a user's cart
@cart.delete("/{cart_id}", response_model=dict)
async def delete_cart(cart_id: int, db: Session = Depends(get_db)):
    db_cart = db.query(CartModel).filter(CartModel.id == cart_id).first()

    if not db_cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    db.query(CartItemModel).filter(CartItemModel.cart_id == cart_id).delete()
    db.delete(db_cart)
    db.commit()
    return {"message": "Cart deleted"}
