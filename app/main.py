from fastapi import FastAPI, Depends
from app.database import get_db
from sqlalchemy.orm import Session
import app.models as models

app = FastAPI(
    title="TalentMatch AI API",
    description= "Artificial Intelligence-Powered Job Matching Engine",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the TalentMatch AI API!"}

@app.get("/db-test")
def test_db_connection(db: Session = Depends(get_db)):
    return {
        "status": "Database connection successful!",
        "message" : "Connected to the PostgreSQL database without any issues"
    }



