import uuid
from sqlalchemy import Column, String, Text, Integer, DateTime, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.db.database import Base

class Form(Base):
    __tablename__ = "forms"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    slug = Column(String(255), unique=True, nullable=True)
    status = Column(String(50), default="draft")
    form_schema = Column(JSONB, nullable=False, default={})
    settings = Column(JSONB, nullable=True, default={})
    theme = Column(JSONB, nullable=True, default={})
    version = Column(Integer, default=1)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
