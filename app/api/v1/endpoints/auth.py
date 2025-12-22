from fastapi import APIRouter ,Depends, HTTPException,status,Form
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.schema.user import UserCreate, UserRead as UserResponse, UserLogin
from app.db.db import get_db
from app.repositories.user_service import create_user,login_user
from app.schema.response import ApiResponse
router = APIRouter()

@router.post("/login",response_model=ApiResponse[UserLogin])
def login(email: str=Form(...), password: str = Form(...), db: Session = Depends(get_db)):
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
def create(data: UserCreate, db: Session = Depends(get_db)):
    try:
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
     

# @router.post("/signup", response_model=UserResponse)
# def create(
#         name: str = Form(...),
#         email: str = Form(...),
#         password: str = Form(...),
#         db: Session = Depends(get_db)):
#     data = UserCreate(name=name, email=email, password=password)
#     print("Received user data for signup:")
#     return create_user(db, data)
