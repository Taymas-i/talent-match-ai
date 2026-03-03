from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# --JOB SCHEMAS--

class jobBase(BaseModel):
    title: str
    company: str
    location: Optional[str] = None
    description: str
    link: str
    source: str

# Schema to be used when posting ads from Scraper to the API
class jobCreate(jobBase):
    pass # no needed ID or date, Base's area is enough

# Schema to be used when sending data from the API to the Streamlit interface (outbound)
class jobOut(jobBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True # Critical: Automatically converts SQLAlchemy objects to JSON!

# --USER SCHEMAS--

class UserCreate(BaseModel):
    email: str
    target_title: Optional[str] = None
    cv_text: Optional[str] = None

class UserOut(BaseModel):
    id: int
    email: str
    target_title: Optional[str] = None

    class Config:
        from_attributes = True 

# --MATCH SCHEMAS--

class MatchBase(BaseModel):
    match_score: Optional[float] = None
    is_applied: bool = False

# To be used when sending matching data from the API to Streamlit
class MatchOut(MatchBase):
    id: int
    user_id: int
    job_id: int

    class Config:
        from_attributes = True

# A small schema for our API to only accept text named cv_text from outside

class CVMatchRequest(BaseModel):
    cv_text: str

class ManualMatchRequest(BaseModel):
    cv_text: str
    job_text: str 