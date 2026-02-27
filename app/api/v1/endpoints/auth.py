from fastapi import APIRouter ,Depends, HTTPException,status,Form
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.schema.user import UserCreate, UserRead as UserResponse, UserLogin
from app.db.db import get_db
from app.repositories.user_service import create_user,login_user,blacklist_token
from app.schema.response import ApiResponse
from app.middleware.verify_jwt import verify_jwt
router = APIRouter()

@router.post("/login",response_model=ApiResponse[UserLogin])
def login(
     email: str=Form(...),
     password: str = Form(...), 
     db: Session = Depends(get_db)
     ):
    print("Login attempt for email:", email)
    user,generated_jwt = login_user(db, email, password)
    if(not user):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return ApiResponse(
        success=True,
        status_code=status.HTTP_200_OK,
        message="Login successful",
        data=UserLogin(
            id=user.id,
            name=user.name,
            email=user.email,
            access_token=generated_jwt  # Replace with actual token generation logic
        )
    )
    # return JSONResponse(
    #     status_code=status.HTTP_200_OK,
    #     content = {  # content is a arguments of JSONResponse
    #     "id" : user.id,
    #     "name" : user.name,
    #     "email" : user.email
    #     }
    #     )

@router.post("/signup", response_model=ApiResponse[UserResponse])
async def create(name: str = Form(...),
                 email: str = Form(...),
                 password: str = Form(...),
                 db: Session = Depends(get_db)
                 ):
    try:
        data =  UserCreate(name=name, email=email, password=password)
        print("Received user data for signup:", data)
        user = create_user(db, data)
        return ApiResponse(
                success=True,
                status_code=status.HTTP_200_OK,
                message="User created successfully",
                data=UserResponse(
                    id=user.id,
                    name=user.name,
                    email=user.email
                )
            )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ApiResponse(
                success=False,
                message="User creation failed",
                error=str(e)
            ).dict()
        )

@router.post("/logout", response_model=ApiResponse[None],dependencies=[Depends(verify_jwt)])  
def logout(db:Session=Depends(get_db),current_user: dict = Depends(verify_jwt)):
    is_blaclisted = blacklist_token(db,current_user)
    if not is_blaclisted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Logout failed"
        )
    
    print("User logged out successfully")
    # Invalidate the token on client side by simply not using it anymore
    return ApiResponse(
        success=True,
        status_code=status.HTTP_200_OK,
        message="Logout successful",
        data=None
    )

# @router.post("/signup", response_model=UserResponse)
# def create(
#         name: str = Form(...),
#         email: str = Form(...),
#         password: str = Form(...),
#         db: Session = Depends(get_db)):
#     data = UserCreate(name=name, email=email, password=password)
#     print("Received user data for signup:")
#     return create_user(db, data)
