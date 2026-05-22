from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid

# --- Roles ---
class RoleCreate(BaseModel):
    name: str
    label: Optional[str] = None
    parent_role: Optional[uuid.UUID] = None
    is_system: bool = False

class RoleResponse(RoleCreate):
    id: uuid.UUID
    created_at: datetime
    class Config:
        from_attributes = True

# --- Module Access ---
class ModuleAccessCreate(BaseModel):
    role_id: uuid.UUID
    module_name: str
    can_access: bool = False

class ModuleAccessResponse(ModuleAccessCreate):
    id: uuid.UUID
    class Config:
        from_attributes = True

# --- Entity Permissions ---
class EntityPermissionCreate(BaseModel):
    role_id: uuid.UUID
    entity_name: str
    can_list: bool = False
    can_view: bool = False
    can_create: bool = False
    can_edit: bool = False
    can_delete: bool = False
    can_amend: bool = False
    can_export: bool = False

class EntityPermissionResponse(EntityPermissionCreate):
    id: uuid.UUID
    class Config:
        from_attributes = True

# --- Field Permissions ---
class FieldPermissionCreate(BaseModel):
    role_id: uuid.UUID
    entity_name: str
    field_name: str
    can_read: bool = False
    can_write: bool = False
    is_hidden: bool = False

class FieldPermissionResponse(FieldPermissionCreate):
    id: uuid.UUID
    class Config:
        from_attributes = True

# --- Record Assignments ---
class RecordAssignmentCreate(BaseModel):
    entity_name: str
    record_id: uuid.UUID
    assigned_to: uuid.UUID
    assigned_role: str
    assigned_by: uuid.UUID
    is_active: bool = True

class RecordAssignmentResponse(RecordAssignmentCreate):
    id: uuid.UUID
    assigned_at: datetime
    class Config:
        from_attributes = True
