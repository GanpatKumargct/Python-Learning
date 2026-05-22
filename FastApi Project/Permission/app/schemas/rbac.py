from pydantic import BaseModel
from typing import List, Dict, Optional

# --- Form Engine -> RBAC Engine (Field Mask) ---

class FieldMaskRequest(BaseModel):
    entity_name: str
    actor_id: str
    role: str
    fields: List[str]

class FieldMaskResponseItem(BaseModel):
    read: bool
    write: bool
    hidden: bool

# The response is Dict[str, FieldMaskResponseItem]

# --- Workflow Engine -> RBAC Engine (Record Access) ---

class RecordAccessRequest(BaseModel):
    actor_id: str
    actor_role: str
    entity_name: str
    record_id: str
    check_type: str = "record_access"

class RecordAccessResponse(BaseModel):
    allowed: bool
    reason: Optional[str] = None

# --- Page Orchestrator -> RBAC Engine (Module + Entity Access) ---

class ModuleAccessRequest(BaseModel):
    actor_id: str
    role: str
    module_name: str

class EntityAccessResponse(BaseModel):
    can_list: bool
    can_view: bool
    can_create: bool
    can_edit: bool
    can_delete: bool
    can_amend: bool
    can_export: bool

class ModuleAccessResponse(BaseModel):
    can_access: bool
    entities: Dict[str, EntityAccessResponse]
