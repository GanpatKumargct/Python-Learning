from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.Database.database import engine
from app.Model import models
from app.Routers import jobs, applications

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mini-ATS API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(jobs.router)
app.include_router(applications.router)

@app.get("/")
def root():
    return {"message": "Welcome to Mini-ATS API. Access /docs for Swagger UI"}
