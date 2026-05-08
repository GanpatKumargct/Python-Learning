from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.Database.database import get_db
from app.Model import models
from app.schema import schemas

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"]
)

@router.get("/", response_model=List[schemas.Job])
def read_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    jobs = db.query(models.Job).offset(skip).limit(limit).all()
    return jobs

@router.post("/", response_model=schemas.Job)
def create_job(job: schemas.JobCreate, db: Session = Depends(get_db)):
    db_job = models.Job(**job.model_dump())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@router.put("/{job_id}/status", response_model=schemas.Job)
def toggle_job_status(job_id: str, db: Session = Depends(get_db)):
    db_job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    db_job.is_active = not db_job.is_active
    db.commit()
    db.refresh(db_job)
    return db_job
