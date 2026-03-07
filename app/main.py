from fastapi import FastAPI, Depends, HTTPException
from app.database import get_db
from sqlalchemy.orm import Session
import app.models as models
import app.schemas as schemas
from app.services.matcher import NLPJobMatcher
from app.services.scrapers.weworkremotely import WWRScraper
from apscheduler.schedulers.background import BackgroundScheduler
from app.services.llm_analyzer import analyze_skill_gap
from app.database import sessionLocal


app = FastAPI(
    title="TalentMatch AI API",
    description= "Artificial Intelligence-Powered Job Matching Engine",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the TalentMatch AI API!"}

# JOB ENDPOINTS

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
    

# WeWorkRemotely Scraper Endpoint
    
@app.post("/scrape/weworkremotely")
def trigger_wwr_scraper(db: Session = Depends(get_db)):
    try:
        bot = WWRScraper(db)
        bot.scrape()
        return {
            "status": "success",
            "message": "WeWorkRemotely scraping completed and data saved to the database."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scraping WeWorkRemotely: {str(e)}")


    
# NLP MATCHER ENDPOINT

@app.post("/match/")
def match_cv_to_jobs(request: schemas.CVMatchRequest, db: Session = Depends(get_db)):
    """
    Accepts a CV text and returns a list of job matches with their scores.
    """
    try:
        matcher = NLPJobMatcher(db)
        results = matcher.calculate_match_scores(request.cv_text)

        return {
            "status": "success",
            "total_number_of_ads": len(results),
            "matches": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during matching: {e}")
    
# scrap automatically nightly at 3:00 AM

def run_night_shift_scraper():
    print("[*] Night shift scraper is running...")
    db = sessionLocal()
    try:
        bot = WWRScraper(db)
        bot.scrape()
    except Exception as e:
        print(f"Error in night shift scraper: {e}")
    finally:
        db.close()

@app.on_event("startup")
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_night_shift_scraper, 'cron', hour=3, minute=0)
    scheduler.start()
    print("[*] Scheduler started for night shift scraping.")

@app.post("/match/manual")
def match_manual_job(request: schemas.ManualMatchRequest, db: Session = Depends(get_db)):
    try:
        matcher = NLPJobMatcher(db)
        score = matcher.calculate_manual_match_score(request.cv_text, request.job_text)

        llm_analysis = analyze_skill_gap(request.cv_text, request.job_text)

        return {
            "status": "success",
            "match_score": score,
            "analysis": llm_analysis,
            "message": "Analiz başarıyla tamamlandı."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during manual matching: {e}")
    

       

    

    

        
    








