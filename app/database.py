from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load environment variables from .env file
load_dotenv()

# Get the database URL 
DATABASE_URL = os.getenv("DATABASE_URL")

# create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# create Base class for models
Base = declarative_base()

# create configured Session class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# set dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()


