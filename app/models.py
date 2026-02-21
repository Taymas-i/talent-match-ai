from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    target_title = Column(String, nullable=True)
    cv_text = Column(Text, nullable=True)
    
    # a relationship that holds multiple job postings
    matches = relationship("UserJobMatch", back_populates="user")

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    company = Column(String, index=True)
    location = Column(String, nullable=True)
    description = Column(Text)
    link = Column(String, unique=True) #to prevent data duplication
    source = Column(String) # to track where the job posting came from
    is_active = Column(Boolean, default=True) # to mark if the job posting is still active
    created_at = Column(DateTime, default=datetime.utcnow) 

    matches = relationship("UserJobMatch", back_populates="job")

class UserJobMatch(Base):
    __tablename__ = "user_job_matches"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))

    match_score = Column(Float, nullable=True) # NLP score
    is_applied = Column(Boolean, default=False) # to track if the user has applied to the job

    user = relationship("User", back_populates="matches")
    job = relationship("Job", back_populates="matches")



