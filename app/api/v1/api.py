
from fastapi import APIRouter
from app.api.v1.endpoints import users
from app.api.v1.endpoints import auth 
from app.api.v1.endpoints import product
main_router = APIRouter()

main_router.include_router(
    users.router,
    prefix="/users",
    tags=["Users"]
)

main_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Auth"]
)


main_router.include_router(
    product.router,
    prefix="/product",
    tags=["Product"]
)