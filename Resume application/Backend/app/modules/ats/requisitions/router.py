from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import uuid

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_roles
from app.modules.auth.models import User
from app.modules.ats.requisitions import schemas, service

router = APIRouter()

@router.post("/", response_model=schemas.RequisitionOut, status_code=status.HTTP_201_CREATED)
async def create_requisition(
    payload: schemas.RequisitionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles('hiring_manager', 'admin'))
):
    return await service.create_requisition(db, payload, current_user.id)

@router.get("/", response_model=List[schemas.RequisitionOut])
async def list_requisitions(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await service.get_requisitions(db)

@router.post("/{req_id}/submit", response_model=schemas.RequisitionOut)
async def submit_requisition(
    req_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await service.submit_for_approval(db, req_id)
