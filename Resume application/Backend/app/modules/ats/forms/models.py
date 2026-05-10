import uuid
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from app.core.database import Base

class Form(Base):
    __tablename__ = 'forms'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    department = Column(String, nullable=True)
    module = Column(String, nullable=False, default='ats')
    response_table = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    version = Column(Integer, default=1)
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class FormField(Base):
    __tablename__ = 'form_fields'
    __table_args__ = (UniqueConstraint('form_id', 'field_key', name='uq_form_field_key'),)

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    form_id = Column(UUID(as_uuid=True), ForeignKey('forms.id', ondelete='CASCADE'), nullable=False)
    field_key = Column(String, nullable=False)
    label = Column(String, nullable=False)
    field_type = Column(String, nullable=False)
    is_required = Column(Boolean, default=False)
    options = Column(JSONB, nullable=True)
    validation = Column(JSONB, nullable=True)
    display_order = Column(Integer, nullable=False)
    column_type = Column(String, default='TEXT')
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class FormFileUpload(Base):
    __tablename__ = 'form_file_uploads'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    form_id = Column(UUID(as_uuid=True), ForeignKey('forms.id'), nullable=True)
    response_row_id = Column(UUID(as_uuid=True), nullable=False)
    field_key = Column(String, nullable=False)
    original_name = Column(String, nullable=False)
    s3_key = Column(String, nullable=False)
    s3_url = Column(String, nullable=False)
    file_size_bytes = Column(Integer, nullable=True)
    mime_type = Column(String, nullable=True)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
