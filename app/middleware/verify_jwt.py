from fastapi import Header, HTTPException
from jose import jwt, JWTError
from dotenv import load_dotenv
import os
#LOAD ENV VARIABLES
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def verify_jwt(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "Token missing")

    token = authorization.replace("Bearer ", "")
    print("Received JWT token:", token)
    try:
        #Decode JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("Decoded JWT payload:", payload)
        print("User ID from token:", payload.get("id"))
        print("User Email from token:", payload.get("sub"))
        return payload
    except JWTError:
        raise HTTPException(401, "Invalid or expired token")
