from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.Database.database import get_db
from app.Model import models
from app.schema import schemas
import datetime

router = APIRouter(
    prefix="/applications",
    tags=["applications"]
)

@router.get("/", response_model=List[schemas.Application])
def read_applications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_apps = db.query(models.Application).offset(skip).limit(limit).all()
    apps = []
    for app in db_apps:
        app_dict = {
            "id": app.id,
            "job_id": app.job_id,
            "full_name": app.full_name,
            "email": app.email,
            "phone": app.phone,
            "resume_link": app.resume_link,
            "skills": app.skills.split(",") if app.skills else [],
            "education": app.education,
            "current_stage": app.current_stage,
            "history": app.history
        }
        apps.append(schemas.Application(**app_dict))
    return apps

@router.post("/", response_model=schemas.Application)
def create_application(app: schemas.ApplicationCreate, db: Session = Depends(get_db)):
    db_app = models.Application(
        id=app.id,
        job_id=app.job_id,
        full_name=app.full_name,
        email=app.email,
        phone=app.phone,
        resume_link=app.resume_link,
        skills=",".join(app.skills),
        education=app.education,
        current_stage=app.current_stage
    )
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    
    history = models.ApplicationHistory(
        application_id=db_app.id,
        stage=app.current_stage,
        date=datetime.date.today().isoformat()
    )
    db.add(history)
    db.commit()

    return read_application(db_app.id, db)

def read_application(app_id: str, db: Session):
    app = db.query(models.Application).filter(models.Application.id == app_id).first()
    return schemas.Application(
        id=app.id,
        job_id=app.job_id,
        full_name=app.full_name,
        email=app.email,
        phone=app.phone,
        resume_link=app.resume_link,
        skills=app.skills.split(",") if app.skills else [],
        education=app.education,
        current_stage=app.current_stage,
        history=app.history
    )

class StageUpdate(schemas.BaseModel):
    stage: str

@router.put("/{app_id}/stage", response_model=schemas.Application)
def update_application_stage(app_id: str, stage_update: StageUpdate, db: Session = Depends(get_db)):
    db_app = db.query(models.Application).filter(models.Application.id == app_id).first()
    if not db_app:
        raise HTTPException(status_code=404, detail="Application not found")
    
    db_app.current_stage = stage_update.stage
    history = models.ApplicationHistory(
        application_id=db_app.id,
        stage=stage_update.stage,
        date=datetime.date.today().isoformat()
    )
    db.add(history)
    db.commit()
    
    return read_application(app_id, db)
