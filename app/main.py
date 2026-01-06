from fastapi import FastAPI
from app.api.v1.api import main_router
from app.db.db import check_db_connection, Base, engine
# from app.models.productmodel import ProductModel
# from app.models.usermodel import User
import app.models


app = FastAPI(
    title="FastAPI App Project",
    # docs_url=None, # this code is diabled in production
    # redoc_url=None, # this code is disabled in production
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    
)

@app.on_event("startup")
def startup_event():
    if check_db_connection():  
        print("✅ Database connected successfully")
    else:
        print("❌ Database connection error")



#app.include_router(api_router)
Base.metadata.create_all(bind=engine)
app.include_router(main_router, prefix="/api/v1")


# @app.get("/")
# def health():
#     return {"status": "OK"}

# @app.get("/db-status")
# def db_status():
#     return {"database": "connected" if check_db_connection() else "not connected"}
