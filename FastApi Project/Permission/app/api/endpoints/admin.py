from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.api import deps
from app.schemas.admin import (
    RoleCreate, RoleResponse,
    ModuleAccessCreate, ModuleAccessResponse,
    EntityPermissionCreate, EntityPermissionResponse,
    FieldPermissionCreate, FieldPermissionResponse,
    RecordAssignmentCreate, RecordAssignmentResponse
)
from app.services.admin import AdminService

router = APIRouter()

# --- Roles ---
@router.post("/roles", response_model=RoleResponse)
async def create_role(req: RoleCreate, db: AsyncSession = Depends(deps.get_db)):
    return await AdminService(db).create_role(req)

@router.get("/roles", response_model=List[RoleResponse])
async def get_roles(db: AsyncSession = Depends(deps.get_db)):
    return await AdminService(db).get_roles()

@router.delete("/roles/{role_id}")
async def delete_role(role_id: uuid.UUID, db: AsyncSession = Depends(deps.get_db)):
    deleted = await AdminService(db).delete_role(role_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Role not found")
    return {"status": "deleted"}

# --- Module Access ---
@router.post("/module-access", response_model=ModuleAccessResponse)
async def create_module_access(req: ModuleAccessCreate, db: AsyncSession = Depends(deps.get_db)):
    return await AdminService(db).create_module_access(req)

@router.get("/module-access", response_model=List[ModuleAccessResponse])
async def get_module_access(db: AsyncSession = Depends(deps.get_db)):
    return await AdminService(db).get_module_accesses()

@router.delete("/module-access/{item_id}")
async def delete_module_access(item_id: uuid.UUID, db: AsyncSession = Depends(deps.get_db)):
    deleted = await AdminService(db).delete_module_access(item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Not found")
    return {"status": "deleted"}

# --- Entity Permissions ---
@router.post("/entity-permissions", response_model=EntityPermissionResponse)
async def create_entity_permission(req: EntityPermissionCreate, db: AsyncSession = Depends(deps.get_db)):
    return await AdminService(db).create_entity_permission(req)

@router.get("/entity-permissions", response_model=List[EntityPermissionResponse])
async def get_entity_permissions(db: AsyncSession = Depends(deps.get_db)):
    return await AdminService(db).get_entity_permissions()

@router.delete("/entity-permissions/{item_id}")
async def delete_entity_permission(item_id: uuid.UUID, db: AsyncSession = Depends(deps.get_db)):
    deleted = await AdminService(db).delete_entity_permission(item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Not found")
    return {"status": "deleted"}

# --- Field Permissions ---
@router.post("/field-permissions", response_model=FieldPermissionResponse)
async def create_field_permission(req: FieldPermissionCreate, db: AsyncSession = Depends(deps.get_db)):
    return await AdminService(db).create_field_permission(req)

@router.get("/field-permissions", response_model=List[FieldPermissionResponse])
async def get_field_permissions(db: AsyncSession = Depends(deps.get_db)):
    return await AdminService(db).get_field_permissions()

@router.delete("/field-permissions/{item_id}")
async def delete_field_permission(item_id: uuid.UUID, db: AsyncSession = Depends(deps.get_db)):
    deleted = await AdminService(db).delete_field_permission(item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Not found")
    return {"status": "deleted"}

# --- Record Assignments ---
@router.post("/record-assignments", response_model=RecordAssignmentResponse)
async def create_record_assignment(req: RecordAssignmentCreate, db: AsyncSession = Depends(deps.get_db)):
    return await AdminService(db).create_record_assignment(req)

@router.get("/record-assignments", response_model=List[RecordAssignmentResponse])
async def get_record_assignments(db: AsyncSession = Depends(deps.get_db)):
    return await AdminService(db).get_record_assignments()

@router.delete("/record-assignments/{item_id}")
async def delete_record_assignment(item_id: uuid.UUID, db: AsyncSession = Depends(deps.get_db)):
    deleted = await AdminService(db).delete_record_assignment(item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Not found")
    return {"status": "deleted"}
