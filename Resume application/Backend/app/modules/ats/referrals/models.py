import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.database import Base

class Referral(Base):
    __tablename__ = 'referrals'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pipeline_id = Column(UUID(as_uuid=True), ForeignKey('pipelines.id', ondelete='CASCADE'), nullable=True)
    referrer_user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    referrer_employee_id = Column(String, nullable=False)
    relationship = Column(String, nullable=True)
    reason = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
