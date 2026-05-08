from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .config import settings
DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit =False, autoflush=False, bind=engine)

Base = declarative_base()   #it is use to create the table schema 

#Dependency injection 
def get_db():
    db = SessionLocal()
    try:
        yield db    #Waiting for other to use my db 
    finally: 
        db.close()
