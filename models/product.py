from sqlalchemy import Column, Integer, String, Boolean, Numeric 
from sqlalchemy.ext.declarative import declarative_base
from config.db import engine

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    in_stock = Column(Boolean, default=True)


Base.metadata.create_all(engine)