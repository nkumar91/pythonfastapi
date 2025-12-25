from fastapi import APIRouter,Depends,HTTPException, Header,status
from app.middleware.verify_jwt import verify_jwt
from app.schema.product_response import ProductRead
from app.schema.response import ApiResponse
from app.db.db import get_db
from typing import List
from sqlalchemy.orm import Session
from app.repositories.product_service import get_products
from jose import JWTError, jwt
#from fastapi.security import OAuth2PasswordBearer
#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter(dependencies=[Depends(verify_jwt)]) # Apply JWT verification to all endpoints in this router


@router.get("/",response_model=ApiResponse[List[ProductRead]],dependencies=[Depends(verify_jwt)])
async def get_all_products(db:Session=Depends(get_db)):
    print("Fetching all products")
    products = get_products(db)
    # if not products:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="No products found"
    #     )
    if not products:
        return ApiResponse(
            success=False,
            status_code=404,
            message="No products found",
            data=[]
        )
    return ApiResponse(
        success=True,
        status_code=200,
        message="Products retrieved successfully",
        data=products
    )