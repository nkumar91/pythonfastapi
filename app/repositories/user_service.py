from datetime import datetime, timedelta
from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from app.models.usermodel import User
from app.schema.user import UserCreate, UserRead
from passlib.context import CryptContext
from jose import jwt, JWTError
import os
from dotenv import load_dotenv
from app.db.redis import redis_client

#LOAD ENV VARIABLES
load_dotenv()
jwt_secret = os.getenv("SECRET_KEY")
jwt_algorithm = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


def login_user(db:Session,email:str,password:str):
    user = db.query(User).filter(User.email == email).first()
    # print("User found during login:", user)
    if(not user):
        return None
    # Check password
    pwd_context = CryptContext(
        schemes=["bcrypt"],
        deprecated="auto"
    )
    print("User found during login:", user)
    # Verify password
    if(not pwd_context.verify(password,user.password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    # Generate JWT Token
    #print("Generated JWT:", generate_jwt)
    generate_jwt = jwt.encode({"email": user.email,"id":user.id,"exp":datetime.utcnow() + timedelta(minutes=30)}, jwt_secret, algorithm=jwt_algorithm)
    # retuern user and jwt
    return user,generate_jwt



# def login_user(db: Session, email: str, password: str):
#     user = db.query(User).filter(User.email == email).first()
#     if not user:
#         return None
#     pwd_context = CryptContext(
#         schemes=["bcrypt"],
#         deprecated="auto"
#     )
#     if not pwd_context.verify(password, user.password):
#         return None
#     return user

def create_user(db: Session, user: UserCreate):
    existing_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )
    print("Is existing user:", existing_user)

    if existing_user:
        raise ValueError("EMAIL_ALREADY_EXISTS")
    pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
    )
    db_user = User(
        name=user.name, 
        email=user.email,
        password=pwd_context.hash(user.password)
        )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# def get_users(db: Session):
#     return db.query(User).all() 


# def get_user(db: Session, user_id: int):
#     return db.query(User).filter(User.id == user_id).first()


# def update_user(db: Session, user_id: int, user:UserCreate):
#     db_user = get_user(db, user_id)
#     if not db_user:
#         return None
#     db_user.name = user.name
#     db_user.email = user.email
#     db.commit()
#     db.refresh(db_user)
#     return db_user


# def delete_user(db: Session, user_id: int):
#     db_user = get_user(db, user_id)
#     if not db_user:
#         return None
#     db.delete(db_user)
#     db.commit()
#     return db_user

def blacklist_token(db: Session,payload: dict):
    # Placeholder for any server-side logout operations if needed
    # Store the token in Redis to invalidate it
    exp = payload.get("exp")
    if exp is None:
        return False
    current_time = int(datetime.utcnow().timestamp())
    ttl = exp - current_time
    redis_client.setex(payload["token"], ttl, "blacklisted")  # Set token as blacklisted for 1 hour
    return True