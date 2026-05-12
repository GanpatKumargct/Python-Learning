from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import uuid

from app.core.database import get_db
from app.core.dependencies import require_roles
from app.modules.auth.models import User
from app.modules.admin import schemas, service

router = APIRouter()

# Only Admin and PTC can access the user management dashboard
@router.get("/users", response_model=List[schemas.UserOut])
async def list_users(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles('admin', 'ptc'))
):
    return await service.get_all_users(db)

@router.post("/users", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
async def create_new_user(
    payload: schemas.UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles('admin', 'ptc'))
):
    return await service.create_user(db, payload)

@router.patch("/users/{user_id}", response_model=schemas.UserOut)
async def update_existing_user(
    user_id: uuid.UUID,
    payload: schemas.UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles('admin', 'ptc'))
):
    return await service.update_user(db, user_id, payload)
