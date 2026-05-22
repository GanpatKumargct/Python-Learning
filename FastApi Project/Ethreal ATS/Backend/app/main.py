from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.Database.database import engine
from app.Model import models
from app.Routers import entity, workflow, form, page

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Aerospace ERP API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(entity.router)
app.include_router(workflow.router)
app.include_router(form.router)
app.include_router(page.router)

@app.get("/")
def root():
    return {"message": "Welcome to Aerospace ERP API. Access /docs for Swagger UI"}
