from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base #type:ignore
from sqlalchemy.orm import sessionmaker     #type:ignore


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:0000@localhost/ToDo"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit =False, autoflush=False, bind=engine)

Base = declarative_base()   #it is use to create the table schema 


#Dependency injection 
def get_db():
    db = SessionLocal()
    try:
        yield db    #Waiting for other to use my db 
    finally: 
        db.close()