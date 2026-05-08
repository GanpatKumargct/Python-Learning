from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.Model import model
from app.database.database import engine
from app.router import task, user, auth

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(task.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def home():
    return {"message": "Welcome to Task Management API"}