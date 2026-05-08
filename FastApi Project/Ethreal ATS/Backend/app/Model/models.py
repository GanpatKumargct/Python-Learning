from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.Database.database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    location = Column(String)
    openings_count = Column(Integer)
    is_active = Column(Boolean, default=True)

    applications = relationship("Application", back_populates="job")


class Application(Base):
    __tablename__ = "applications"

    id = Column(String, primary_key=True, index=True)
    job_id = Column(String, ForeignKey("jobs.id"))
    full_name = Column(String)
    email = Column(String)
    phone = Column(String)
    resume_link = Column(String)
    skills = Column(String) # Stored as comma separated string
    education = Column(String)
    current_stage = Column(String)

    job = relationship("Job", back_populates="applications")
    history = relationship("ApplicationHistory", back_populates="application", cascade="all, delete-orphan")


class ApplicationHistory(Base):
    __tablename__ = "application_history"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    application_id = Column(String, ForeignKey("applications.id"))
    stage = Column(String)
    date = Column(String)

    application = relationship("Application", back_populates="history")
