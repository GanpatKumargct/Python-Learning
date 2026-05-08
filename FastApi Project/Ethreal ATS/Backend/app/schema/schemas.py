from pydantic import BaseModel
from typing import List, Optional

class JobBase(BaseModel):
    title: str
    description: str
    location: str
    openings_count: int
    is_active: bool = True

class JobCreate(JobBase):
    id: str

class Job(JobBase):
    id: str

    class Config:
        from_attributes = True

class ApplicationHistoryBase(BaseModel):
    stage: str
    date: str

class ApplicationHistory(ApplicationHistoryBase):
    id: int
    application_id: str

    class Config:
        from_attributes = True

class ApplicationBase(BaseModel):
    job_id: str
    full_name: str
    email: str
    phone: str
    resume_link: str
    skills: List[str]
    education: str
    current_stage: str

class ApplicationCreate(ApplicationBase):
    id: str

class Application(ApplicationBase):
    id: str
    history: List[ApplicationHistoryBase] = []

    class Config:
        from_attributes = True
