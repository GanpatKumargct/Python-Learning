from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import uuid

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_roles
from app.modules.auth.models import User
from app.modules.forms import schemas, service

router = APIRouter()

@router.post("/", response_model=schemas.FormOut, status_code=status.HTTP_201_CREATED)
async def create_new_form(
    payload: schemas.FormCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles('admin', 'hiring_manager'))
):
    try:
        return await service.create_form(db, payload, current_user.id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create form and table: {str(e)}"
        )

@router.get("/", response_model=List[schemas.FormOut])
async def list_forms(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await service.get_forms(db)

@router.get("/{form_id}", response_model=schemas.FormOut)
async def get_form(
    form_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    form = await service.get_form_by_id(db, form_id)
    if not form:
        raise HTTPException(status_code=404, detail="Form not found")
    return form
