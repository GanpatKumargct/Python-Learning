import uuid
from typing import Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_, and_

from app.models.role import Role, RoleHierarchy
from app.models.permission import ModuleAccess, EntityPermission, FieldPermission
from app.models.assignment import RecordAssignment
from app.schemas.rbac import (
    FieldMaskRequest, FieldMaskResponseItem,
    RecordAccessRequest, RecordAccessResponse,
    ModuleAccessRequest, ModuleAccessResponse, EntityAccessResponse
)

class RBACService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_role_by_name(self, role_name: str) -> Optional[Role]:
        result = await self.db.execute(select(Role).where(Role.name == role_name))
        return result.scalars().first()

    async def get_field_mask(self, req: FieldMaskRequest) -> Dict[str, FieldMaskResponseItem]:
        role = await self.get_role_by_name(req.role)
        if not role:
            # Default everything to false if role not found
            return {field: FieldMaskResponseItem(read=False, write=False, hidden=True) for field in req.fields}
            
        stmt = select(FieldPermission).where(
            and_(
                FieldPermission.role_id == role.id,
                FieldPermission.entity_name == req.entity_name,
                FieldPermission.field_name.in_(req.fields)
            )
        )
        result = await self.db.execute(stmt)
        permissions = {p.field_name: p for p in result.scalars().all()}
        
        response = {}
        for field in req.fields:
            if field in permissions:
                p = permissions[field]
                response[field] = FieldMaskResponseItem(
                    read=p.can_read and not p.is_hidden,
                    write=p.can_write and not p.is_hidden,
                    hidden=p.is_hidden
                )
            else:
                response[field] = FieldMaskResponseItem(read=False, write=False, hidden=True)
                
        return response

    async def get_child_roles_recursive(self, parent_role_id: uuid.UUID) -> List[uuid.UUID]:
        # Simple flat hierarchy as requested in specification
        stmt = select(RoleHierarchy.child_role_id).where(RoleHierarchy.parent_role_id == parent_role_id)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def check_record_access(self, req: RecordAccessRequest) -> RecordAccessResponse:
        role = await self.get_role_by_name(req.actor_role)
        if not role:
             return RecordAccessResponse(allowed=False, reason="role_not_found")

        # Step 1: Check entity-level permission first
        stmt = select(EntityPermission).where(
            and_(
                EntityPermission.role_id == role.id,
                EntityPermission.entity_name == req.entity_name
            )
        )
        result = await self.db.execute(stmt)
        entity_perm = result.scalars().first()
        
        if not entity_perm or not entity_perm.can_view:
            return RecordAccessResponse(allowed=False, reason="no_entity_permission")

        # Parse actor_id and record_id to UUID if possible, assuming they are UUIDs for DB lookup
        try:
            actor_uuid = uuid.UUID(req.actor_id)
            record_uuid = uuid.UUID(req.record_id)
        except ValueError:
            return RecordAccessResponse(allowed=False, reason="invalid_uuid_format")

        # Step 2: Check direct assignment
        stmt = select(RecordAssignment).where(
            and_(
                RecordAssignment.entity_name == req.entity_name,
                RecordAssignment.record_id == record_uuid,
                RecordAssignment.assigned_to == actor_uuid,
                RecordAssignment.is_active == True
            )
        )
        result = await self.db.execute(stmt)
        direct = result.scalars().first()
        if direct:
            return RecordAccessResponse(allowed=True, reason=None)

        # Step 3: Check hierarchy — can actor's role see records owned by child roles?
        child_role_ids = await self.get_child_roles_recursive(role.id)
        
        if not child_role_ids:
            return RecordAccessResponse(allowed=False, reason="no_assignment")
            
        # We need the role names of these child roles to check assigned_role in record_assignments
        stmt = select(Role.name).where(Role.id.in_(child_role_ids))
        result = await self.db.execute(stmt)
        child_role_names = list(result.scalars().all())
        
        if not child_role_names:
            return RecordAccessResponse(allowed=False, reason="no_assignment")

        stmt = select(RecordAssignment).where(
            and_(
                RecordAssignment.entity_name == req.entity_name,
                RecordAssignment.record_id == record_uuid,
                RecordAssignment.assigned_role.in_(child_role_names),
                RecordAssignment.is_active == True
            )
        )
        result = await self.db.execute(stmt)
        hierarchy_match = result.scalars().first()
        if hierarchy_match:
            return RecordAccessResponse(allowed=True, reason=None)
            
        return RecordAccessResponse(allowed=False, reason="no_assignment")

    async def get_module_access(self, req: ModuleAccessRequest) -> ModuleAccessResponse:
        role = await self.get_role_by_name(req.role)
        if not role:
             return ModuleAccessResponse(can_access=False, entities={})

        stmt = select(ModuleAccess).where(
            and_(
                ModuleAccess.role_id == role.id,
                ModuleAccess.module_name == req.module_name
            )
        )
        result = await self.db.execute(stmt)
        module_access = result.scalars().first()
        
        if not module_access or not module_access.can_access:
            return ModuleAccessResponse(can_access=False, entities={})

        # Get all entity permissions for this role to return with module access
        stmt = select(EntityPermission).where(EntityPermission.role_id == role.id)
        result = await self.db.execute(stmt)
        entity_perms = result.scalars().all()
        
        entities = {}
        for ep in entity_perms:
            entities[ep.entity_name] = EntityAccessResponse(
                can_list=ep.can_list,
                can_view=ep.can_view,
                can_create=ep.can_create,
                can_edit=ep.can_edit,
                can_delete=ep.can_delete,
                can_amend=ep.can_amend,
                can_export=ep.can_export
            )
            
        return ModuleAccessResponse(can_access=True, entities=entities)
