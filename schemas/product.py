from pydantic import BaseModel, condecimal, Field
from typing import Optional

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: Optional[condecimal] = Field(None, max_digits=10, decimal_places=2)
    in_stock: bool


class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[condecimal] = Field(None, max_digits=10, decimal_places=2)
    in_stock: Optional[bool] = None


class ProductInDB(ProductBase):
    id: int

    class Config:
        from_attributes = True


class ProductOut(ProductBase):
    id: int

    class Config:
        from_attributes = True
