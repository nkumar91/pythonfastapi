
from fastapi import APIRouter
from app.api.v1.endpoints import users
from app.api.v1.endpoints import auth
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
