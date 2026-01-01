from fastapi import APIRouter,Depends,Query,HTTPException, Header,status
from app.middleware.verify_jwt import verify_jwt
from app.schema.product_response import ProductRead
#from fastapi.responses import JSONResponse
from app.schema.response import ApiResponse,ApiResponseProduct  
from app.db.db import get_db
from typing import List
from sqlalchemy.orm import Session
from app.repositories.product_service import get_products
# from jose import JWTError, jwt
#from fastapi.security import OAuth2PasswordBearer
#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# router = APIRouter(dependencies=[Depends(verify_jwt)]) # Apply JWT verification to all endpoints in this router

router = APIRouter()
#@app.get("/products/{product_id}")
@router.get("/",response_model=ApiResponseProduct[List[ProductRead]],dependencies=[Depends(verify_jwt)])
async def get_all_products(page:int=Query(1,ge=1,le=500),db:Session=Depends(get_db)):
    print("Fetching all products",page)
    all_data = get_products(db,page)
    # if not products:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="No products found"
    #     )
    if not all_data["products"]:
        return ApiResponseProduct(
            success=False,
            status_code=404,
            message="No products found",
            data=[],
            total_pages=0
        )
    return ApiResponseProduct(
        success=True,
        status_code=200,
        message="Products retrieved successfully",
        total_pages=all_data["total_pages"],
        data=all_data["products"]
    )