import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import auth, roles, users
from app.db.database import engine, Base
from app.utils.logger import logger

# Create all database tables based on SQLAlchemy models
# In a true production environment with existing data, you'd use Alembic migrations instead.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="JWT Auth Production API",
    description="Role Based Access Control API using FastAPI and PostgreSQL",
    version="1.0.0"
)

# CORS configuration for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], # Vite frontend default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(roles.router, prefix="/api/roles", tags=["Roles"])

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up FastAPI application...")
    
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down FastAPI application...")

@app.get("/")
def root():
    return {"message": "Welcome to the JWT Auth API"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
