from pydantic import BaseModel, condecimal, Field
from typing import List, Optional
from datetime import datetime


class OrderBase(BaseModel):
    total_price: float
    status: str = "pending"
    created_at: datetime


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int


class OrderCreate(BaseModel):
    user_id: int
    total_price: float
    status: str = "pending"
    created_at: datetime
    items: List[OrderItemCreate]


class OrderUpdate(BaseModel):
    total_price: Optional[float] = None
    status: Optional[str] = None


class OrderInDB(OrderBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


class OrderItemBase(BaseModel):
    order_id: int
    product_id: int
    quantity: int


class OrderItemOut(OrderItemBase):
    id: int

    class Config:
        from_attributes = True


class OrderOut(OrderBase):
    id: int
    user_id: int
    items: List[OrderItemOut]

    class Config:
        from_attributes = True


class OrderItemUpdate(BaseModel):
    quantity: Optional[int] = None


class OrderItemInDB(OrderItemBase):
    id: int

    class Config:
        from_attributes = True
