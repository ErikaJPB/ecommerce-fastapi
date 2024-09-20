from pydantic import BaseModel
from typing import List, Optional


class CartItemBase(BaseModel):
    product_id: int
    quantity: int


class CartItemCreate(CartItemBase):
    pass

class CartItemUpdate(CartItemBase):
    quantity: Optional[int] = None

class CartItemOut(CartItemBase):
    id: int

    class Config:
        from_attributes = True


class CartBase(BaseModel):
    user_id: int

class CartCreate(CartBase):
    items: List[CartItemCreate]


class CartOut(CartBase):
    id:int
    items: List[CartItemOut]

    class Config:
        from_attributes = True