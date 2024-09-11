from sqlalchemy import Column, Integer, String, Boolean, Numeric 
from sqlalchemy.ext.declarative import declarative_base
from config.db import Base




class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    in_stock = Column(Boolean, default=True)


