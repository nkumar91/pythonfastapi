from sqlalchemy.orm import Session
from app.models.productmodel import ProductModel
def get_products(db:Session):
    return db.query(ProductModel).all()