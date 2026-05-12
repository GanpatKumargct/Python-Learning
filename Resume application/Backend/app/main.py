from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

from app.modules.auth.router import router as auth_router
from app.modules.admin.router import router as admin_router
from app.modules.forms.router import router as forms_router
from app.modules.ats.requisitions.router import router as req_router
# from app.modules.ats.pipeline.router import router as pipeline_router
# from app.modules.ats.candidates.router import router as candidate_router
# from app.modules.ats.emails.router import router as email_router

app = FastAPI(title="ERP – ATS API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex="https?://localhost:.*", # Allow any localhost port during development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers with prefix
app.include_router(auth_router,      prefix="/api/v1/auth",        tags=["Auth"])
app.include_router(admin_router,     prefix="/api/v1/admin",       tags=["Admin"])
app.include_router(forms_router,     prefix="/api/v1/forms",       tags=["Forms"])
app.include_router(req_router,       prefix="/api/v1/requisitions", tags=["Requisitions"])
# app.include_router(pipeline_router,  prefix="/api/v1/pipelines",   tags=["Pipeline"])
# app.include_router(candidate_router, prefix="/api/v1/candidates",  tags=["Candidates"])
# app.include_router(email_router,     prefix="/api/v1/email-templates", tags=["Email Templates"])

@app.get("/health")
def health():
    return {"status": "ok"}
