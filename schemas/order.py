from pydantic import BaseModel, condecimal, Field
from typing import List, Optional
from datetime import datetime


class OrderBase(BaseModel):
    total_price: float
    status: str = "pending"
    created_at: datetime


class OrderCreate(OrderBase):
    user_id: int


class OrderUpdate(BaseModel):
    total_price: Optional[float] = None
    status: Optional[str] = None


class OrderInDB(OrderBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


class OrderOut(OrderBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


class OrderItemBase(BaseModel):
    order_id: int
    product_id: int
    quantity: int


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemUpdate(BaseModel):
    quantity: Optional[int] = None


class OrderItemInDB(OrderItemBase):
    id: int

    class Config:
        from_attributes = True


class OrderItemOut(OrderItemBase):
    id: int

    class Config:
        from_attributes = True
