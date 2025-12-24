from sqlalchemy import Column, Integer, String, Float,DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from app.db.db import Base


class ProductModel(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate =func.now())
    def __repr__(self):
        return f"<Product(name={self.name}, price={self.price}, stock={self.stock})>"