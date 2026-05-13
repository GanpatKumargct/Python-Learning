from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import uuid

from app.core.database import get_db
from app.core.dependencies import require_roles
from app.shared.auth.models import User
from app.modules.admin import schemas, service

router = APIRouter()

# Only Admin and PTC can access the user management dashboard
# Get all users (Admin/PTC access)
@router.get("/users", response_model=List[schemas.UserOut])
async def list_users(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles('admin', 'ptc'))
):
    return await service.get_all_users(db)

# Create a new user (Admin/PTC access)
@router.post("/users", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
async def create_new_user(
    payload: schemas.UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles('admin', 'ptc'))
):
    return await service.create_user(db, payload)

# Update an existing user's details (Admin/PTC access)
@router.patch("/users/{user_id}", response_model=schemas.UserOut)
async def update_existing_user(
    user_id: uuid.UUID,
    payload: schemas.UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles('admin', 'ptc'))
):
    return await service.update_user(db, user_id, payload)

# Delete a user entirely from the system (Admin only access)
@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles('admin'))
):
    await service.delete_user(db, user_id)
    return None

# Get all email templates (Admin access)
@router.get("/email-templates")
async def list_email_templates(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles('admin'))
):
    return await service.get_all_email_templates(db)

# Update or create an email template (Admin access)
@router.post("/email-templates")
async def save_email_template(
    payload: schemas.EmailTemplateCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles('admin'))
):
    return await service.save_email_template(db, payload)
