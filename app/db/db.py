import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

#LOAD ENV VARIABLES
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

#CHECK IF ENV VARIABLES ARE SET

if not all([DB_HOST, DB_USER, DB_NAME]):
    raise RuntimeError("Database environment variables not set")

#DATABASE URL
DATABASE_URL = (
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

#SQLALCHEMY SETUP
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

#FUNCTION TO CHECK DB CONNECTION
def check_db_connection():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except SQLAlchemyError as e:
        print("❌ Database connection failed:", e)
        return False
    

#DEPENDENCY TO GET DB SESSION    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()