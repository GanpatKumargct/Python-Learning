from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create the SQLAlchemy engine. 
# In production, you might want to add connection pooling parameters here.
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)

# SessionLocal class will be used to create individual database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our SQLAlchemy models to inherit from
Base = declarative_base()

def get_db():
    """
    Dependency generator for FastAPI that yields a database session.
    Ensures the session is closed after the request is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
