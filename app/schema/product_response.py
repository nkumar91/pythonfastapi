
from datetime import datetime
from pydantic import BaseModel,Field
#from typing import Optional

class ProductBase(BaseModel):
    """Shared fields for a product"""
    name: str = Field(..., example="Sample Product")
    description: str = Field(None, example="This is a sample product.")
    price: float = Field(..., example=19.99)
    stock: int = Field(..., example=100)

    # created_at: Optional[str] = None``
    # updated_at: Optional[str] = None
    # model_config = {"from_attributes": True}

class ProductCreate(ProductBase):
    """Fields required when creating a product"""
    name:str
    description:str
    price:float
    stock:int
    # No additional fields for now
    model_config = {"from_attributes": True} 

class ProductRead(ProductBase):
    """Fields returned to clients"""
    id: int
    name:str
    description:str
    price:float
    stock:int
    created_at:datetime =  Field(default_factory=datetime.utcnow)
    updated_at:datetime = Field(default_factory=datetime.utcnow)
    model_config = {"from_attributes": True}