import uuid
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.database import Base

class EmailTemplate(Base):
    __tablename__ = 'email_templates'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    subject = Column(String, nullable=False)
    body_html = Column(Text, nullable=False)
    version = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    updated_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class EmailTemplateHistory(Base):
    __tablename__ = 'email_template_history'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    template_id = Column(UUID(as_uuid=True), ForeignKey('email_templates.id'), nullable=True)
    subject = Column(String, nullable=False)
    body_html = Column(Text, nullable=False)
    version = Column(Integer, nullable=False)
    saved_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    saved_at = Column(DateTime(timezone=True), server_default=func.now())
