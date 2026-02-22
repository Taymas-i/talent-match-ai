from fastapi import FastAPI, Depends, HTTPException
from app.database import get_db
from sqlalchemy.orm import Session
import app.models as models
import app.schemas as schemas


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

@app.post("/jobs/", response_model=schemas.jobOut)
def create_job(job: schemas.jobCreate, db: Session = Depends(get_db)):
    """
    adds a new job posting on the system
    if the same job (links) already exists, throws an error to prevent duplication
    """
    # check if the job already exists based on the unique link
    db_job = db.query(models.Job).filter(models.Job.link == job.link).first()
    if db_job:
        raise HTTPException(status_code=400, detail="Job with this link already exists")
    
    # convert the data from the pydantic schema (JSON) to an SQLAlchemy table
    # We use model_dump() instead of dict() according to Pydantic v2 standards
    
    new_job = models.Job(**job.model_dump())

    # 3. Add to the database, commit, and refresh to get the new ID.
    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return new_job

@app.get("/jobs/", response_model=list[schemas.jobOut])
def read_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    LIST ALL JOBS IN THE SYSTEM
    Accepts skip and limit parameters for pagination.
    """
    jobs = db.query(models.Job).filter(models.Job.is_active == True).offset(skip).limit(limit).all()
    return jobs
    


