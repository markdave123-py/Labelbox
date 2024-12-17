from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import DATABASE_URL
import os

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as connection:
        print("Database connection successful!")
except Exception as e:
    print("Error connecting to database:", e)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
