from sqlalchemy.orm import Session
from app.models.productmodel import ProductModel
from math import ceil
def get_products(db:Session,page):
    limit: int = 6
    offset: int = (page - 1) * limit
    print(f"Limit: {limit}, Offset: {offset}")
    total_items = db.query(ProductModel).count()
    total_pages = ceil(total_items / limit)
    return {"total_pages": total_pages, "products": db.query(ProductModel).limit(limit).offset(offset).all()}

