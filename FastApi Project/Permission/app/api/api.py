from fastapi import APIRouter
from app.api.endpoints import rbac, admin

api_router = APIRouter()
api_router.include_router(rbac.router, prefix="/rbac", tags=["rbac"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin-rbac"])
