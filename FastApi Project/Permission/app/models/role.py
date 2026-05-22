import uuid
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.base import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Text, unique=True, nullable=False)
    label = Column(Text, nullable=True)
    parent_role = Column(UUID(as_uuid=True), ForeignKey("roles.id"), nullable=True)
    is_system = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class RoleHierarchy(Base):
    __tablename__ = "role_hierarchy"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    parent_role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"), nullable=False)
    child_role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"), nullable=False)
