from pydantic import BaseModel, condecimal, Field
from typing import Optional

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    in_stock: bool


class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price:Optional[float]
    in_stock: Optional[bool]

    class Config:
        from_attributes = True


class ProductInDB(ProductBase):
    id: int

    class Config:
        from_attributes = True


class ProductOut(ProductBase):
    id: int

    class Config:
        from_attributes = True
