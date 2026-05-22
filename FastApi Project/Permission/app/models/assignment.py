import uuid
from sqlalchemy import Column, Boolean, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.base import Base

class RecordAssignment(Base):
    __tablename__ = "record_assignments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_name = Column(Text, nullable=False)
    record_id = Column(UUID(as_uuid=True), nullable=False)
    assigned_to = Column(UUID(as_uuid=True), nullable=False) # External user id
    assigned_role = Column(Text, nullable=False)
    assigned_by = Column(UUID(as_uuid=True), nullable=False) # External user id
    assigned_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
