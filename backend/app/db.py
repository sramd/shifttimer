import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Get backend/ folder path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load backend/.env
load_dotenv(os.path.join(BASE_DIR, ".env"))

print(">>> Loaded DATABASE_URL =", os.getenv("DATABASE_URL"))

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
