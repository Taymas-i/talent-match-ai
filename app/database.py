from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# The main engine communicating with the database
engine = create_engine(DATABASE_URL)
# The structure that enables us to perform operations on the database (log in)
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# The base class we will inherit our tables from
Base = declarative_base()

# The function required for FastAPI to open and close a new DB session for each request
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
