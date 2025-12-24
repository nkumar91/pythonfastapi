from fastapi import FastAPI
from app.api.v1.api import main_router
from app.db.db import check_db_connection, Base, engine
import app.models


app = FastAPI(title="FastAPI App")


@app.on_event("startup")
def startup_event():
    if check_db_connection():  
        print("✅ Database connected successfully")
    else:
        print("❌ Database connection error")



#app.include_router(api_router)
Base.metadata.create_all(bind=engine)
app.include_router(main_router, prefix="/api/v1")


@app.get("/")
def health():
    return {"status": "OK"}

@app.get("/db-status")
def db_status():
    return {"database": "connected" if check_db_connection() else "not connected"}
