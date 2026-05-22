import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base

class ModuleAccess(Base):
    __tablename__ = "module_access"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"), nullable=False)
    module_name = Column(Text, nullable=False)
    can_access = Column(Boolean, default=False)


class EntityPermission(Base):
    __tablename__ = "entity_permissions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"), nullable=False)
    entity_name = Column(Text, nullable=False)
    can_list = Column(Boolean, default=False)
    can_view = Column(Boolean, default=False)
    can_create = Column(Boolean, default=False)
    can_edit = Column(Boolean, default=False)
    can_delete = Column(Boolean, default=False)
    can_amend = Column(Boolean, default=False)
    can_export = Column(Boolean, default=False)


class FieldPermission(Base):
    __tablename__ = "field_permissions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"), nullable=False)
    entity_name = Column(Text, nullable=False)
    field_name = Column(Text, nullable=False)
    can_read = Column(Boolean, default=False)
    can_write = Column(Boolean, default=False)
    is_hidden = Column(Boolean, default=False)
