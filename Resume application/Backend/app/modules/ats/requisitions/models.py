import uuid
import enum
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum as SQLEnum, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from app.core.database import Base

class RequisitionStatus(str, enum.Enum):
    draft = 'draft'
    pending_director = 'pending_director'
    pending_cos = 'pending_cos'
    pending_founder = 'pending_founder'
    pending_ptc = 'pending_ptc'
    approved = 'approved'
    rejected = 'rejected'
    cancelled = 'cancelled'

class ApprovalStage(str, enum.Enum):
    director = 'director'
    chief_of_staff = 'chief_of_staff'
    founder = 'founder'
    ptc = 'ptc'

class ApprovalDecision(str, enum.Enum):
    approved = 'approved'
    rejected = 'rejected'

class HiringRequisition(Base):
    __tablename__ = 'hiring_requisitions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    job_description = Column(Text, nullable=False)
    scope_of_work = Column(Text, nullable=False)
    department = Column(String, nullable=True)
    status = Column(SQLEnum(RequisitionStatus, name='requisition_status'), default=RequisitionStatus.draft)
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    screening_form_id = Column(UUID(as_uuid=True), ForeignKey('forms.id'), nullable=True)
    min_rejection_chars = Column(JSONB, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class RequisitionSupportingMember(Base):
    __tablename__ = 'requisition_supporting_members'

    requisition_id = Column(UUID(as_uuid=True), ForeignKey('hiring_requisitions.id', ondelete='CASCADE'), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True)

class RequisitionApproval(Base):
    __tablename__ = 'requisition_approvals'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    requisition_id = Column(UUID(as_uuid=True), ForeignKey('hiring_requisitions.id', ondelete='CASCADE'), nullable=False)
    stage = Column(SQLEnum(ApprovalStage, name='approval_stage'), nullable=False)
    decision = Column(SQLEnum(ApprovalDecision, name='approval_decision'), nullable=True)
    remarks = Column(Text, nullable=True)
    decided_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    decided_at = Column(DateTime(timezone=True), nullable=True)
    notified_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
