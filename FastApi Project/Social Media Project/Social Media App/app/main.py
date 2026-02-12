from fastapi import FastAPI
from . import model
from .database import engine 
from .router import post, user, auth


app = FastAPI()

model.Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return "Welcome to Social Media Project"

# Including the routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

