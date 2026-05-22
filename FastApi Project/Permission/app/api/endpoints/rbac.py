from typing import Dict
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.schemas.rbac import (
    FieldMaskRequest, FieldMaskResponseItem,
    RecordAccessRequest, RecordAccessResponse,
    ModuleAccessRequest, ModuleAccessResponse
)
from app.services.rbac import RBACService

router = APIRouter()

@router.post("/field-mask", response_model=Dict[str, FieldMaskResponseItem])
async def get_field_mask(
    req: FieldMaskRequest,
    db: AsyncSession = Depends(deps.get_db)
):
    service = RBACService(db)
    return await service.get_field_mask(req)

@router.post("/record-access", response_model=RecordAccessResponse)
async def check_record_access(
    req: RecordAccessRequest,
    db: AsyncSession = Depends(deps.get_db)
):
    service = RBACService(db)
    return await service.check_record_access(req)

@router.post("/module-access", response_model=ModuleAccessResponse)
async def get_module_access(
    req: ModuleAccessRequest,
    db: AsyncSession = Depends(deps.get_db)
):
    service = RBACService(db)
    return await service.get_module_access(req)
