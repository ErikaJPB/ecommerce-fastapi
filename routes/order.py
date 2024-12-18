from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from config.db import get_db
from models.order import Order as OrderModel, OrderItem as OrderItemModel
from schemas.order import OrderCreate, OrderUpdate, OrderOut, OrderItemCreate, OrderItemOut
from models.product import Product as ProductModel
from models.user import User as UserModel
from utils.auth import get_current_user, is_admin_user


order = APIRouter(prefix="/orders", tags=["orders"])


# Create a new order
@order.post("/", response_model=OrderOut)
async def create_order(order_data: OrderCreate,current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):

    db_order = OrderModel(
        user_id=current_user.id, 
        total_price=order_data.total_price,
        status=order_data.status,
        created_at=order_data.created_at
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # Add order items
    for item in order_data.items:
        db_product = db.query(ProductModel).filter(ProductModel.id == item.product_id).first()
        if not db_product:
            raise HTTPException(status_code=404, detail=f"Product with ID {item.product_id} not found")
        
        db_order_item = OrderItemModel(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(db_order_item)

    db.commit()
    db.refresh(db_order)

    return db_order
    
   
# Admin only, get all orders
@order.get("/", response_model=List[OrderOut], dependencies=[Depends(is_admin_user)])
async def get_orders(db: Session = Depends(get_db)):
    orders = db.query(OrderModel).all()
    return orders


# User or admin, get order by id
@order.get("/{order_id}", response_model=OrderOut)
async def get_order(order_id: int, current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    db_order = db.query(OrderModel).filter(OrderModel.id == order_id).first()

    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    if db_order.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to view this order")

    return db_order


# Admin only, update order
@order.put("/{order_id}", response_model=OrderOut, dependencies=[Depends(is_admin_user)])
async def update_order(order_id: int, order_update: OrderUpdate, db: Session = Depends(get_db)):
    db_order = db.query(OrderModel).filter(OrderModel.id == order_id).first()  

    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order_update.total_price is not None:
        db_order.total_price = order_update.total_price

    if order_update.status is not None:
        db_order.status = order_update.status

    db.commit()
    db.refresh(db_order)

    return db_order

# user only, cancel their own order
@order.put("/{order_id}/cancel", response_model=OrderOut)
async def cancel_order(order_id: int, current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    db_order = db.query(OrderModel).filter(OrderModel.id == order_id, OrderModel.user_id == current_user.id).first()

    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if db_order.status == "cancelled": 
        raise HTTPException(status_code = 400, detail="Order already cancelled")

    db_order.status = "cancelled"
    db.commit()
    db.refresh(db_order)

    return db_order


# Admin only, delete order
@order.delete("/{order_id}", response_model=dict, dependencies=[Depends(is_admin_user)])
async def delete_order(order_id:int, db: Session = Depends(get_db)):
    db_order = db.query(OrderModel).filter(OrderModel.id == order_id).first()

    if not db_order: 
        raise HTTPException(status_code = 404, detail="Order not found")

    db.delete(db_order)
    db.commit()

    return {"message": "Order deleted"}



