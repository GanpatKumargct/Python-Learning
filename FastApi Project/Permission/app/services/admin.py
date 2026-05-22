import uuid
from typing import List, TypeVar, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete

from app.db.base import Base
from app.models.role import Role
from app.models.permission import ModuleAccess, EntityPermission, FieldPermission
from app.models.assignment import RecordAssignment

from app.schemas.admin import (
    RoleCreate, ModuleAccessCreate, EntityPermissionCreate, 
    FieldPermissionCreate, RecordAssignmentCreate
)

ModelType = TypeVar("ModelType", bound=Base)

class AdminService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def _create_and_return(self, model: Type[ModelType], schema_obj) -> ModelType:
        db_obj = model(**schema_obj.model_dump())
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def _get_all(self, model: Type[ModelType]) -> List[ModelType]:
        result = await self.db.execute(select(model))
        return list(result.scalars().all())

    async def _delete(self, model: Type[ModelType], item_id: uuid.UUID) -> bool:
        result = await self.db.execute(delete(model).where(model.id == item_id))
        await self.db.commit()
        return result.rowcount > 0

    # Role Operations
    async def create_role(self, schema_obj: RoleCreate) -> Role:
        return await self._create_and_return(Role, schema_obj)
        
    async def get_roles(self) -> List[Role]:
        return await self._get_all(Role)
        
    async def delete_role(self, role_id: uuid.UUID) -> bool:
        return await self._delete(Role, role_id)

    # Module Access Operations
    async def create_module_access(self, schema_obj: ModuleAccessCreate) -> ModuleAccess:
        return await self._create_and_return(ModuleAccess, schema_obj)
        
    async def get_module_accesses(self) -> List[ModuleAccess]:
        return await self._get_all(ModuleAccess)
        
    async def delete_module_access(self, item_id: uuid.UUID) -> bool:
        return await self._delete(ModuleAccess, item_id)

    # Entity Permission Operations
    async def create_entity_permission(self, schema_obj: EntityPermissionCreate) -> EntityPermission:
        return await self._create_and_return(EntityPermission, schema_obj)
        
    async def get_entity_permissions(self) -> List[EntityPermission]:
        return await self._get_all(EntityPermission)
        
    async def delete_entity_permission(self, item_id: uuid.UUID) -> bool:
        return await self._delete(EntityPermission, item_id)

    # Field Permission Operations
    async def create_field_permission(self, schema_obj: FieldPermissionCreate) -> FieldPermission:
        return await self._create_and_return(FieldPermission, schema_obj)
        
    async def get_field_permissions(self) -> List[FieldPermission]:
        return await self._get_all(FieldPermission)
        
    async def delete_field_permission(self, item_id: uuid.UUID) -> bool:
        return await self._delete(FieldPermission, item_id)

    # Record Assignment Operations
    async def create_record_assignment(self, schema_obj: RecordAssignmentCreate) -> RecordAssignment:
        return await self._create_and_return(RecordAssignment, schema_obj)
        
    async def get_record_assignments(self) -> List[RecordAssignment]:
        return await self._get_all(RecordAssignment)
        
    async def delete_record_assignment(self, item_id: uuid.UUID) -> bool:
        return await self._delete(RecordAssignment, item_id)
