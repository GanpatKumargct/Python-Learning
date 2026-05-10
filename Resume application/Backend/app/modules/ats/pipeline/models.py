import uuid
import enum
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Enum as SQLEnum, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.database import Base

class HiringType(str, enum.Enum):
    inbound = 'inbound'
    outbound = 'outbound'
    referral = 'referral'

class PipelineStatus(str, enum.Enum):
    active = 'active'
    hired = 'hired'
    rejected = 'rejected'
    withdrawn = 'withdrawn'
    on_hold = 'on_hold'

class StageName(str, enum.Enum):
    screening = 'screening'
    fitment_evaluation = 'fitment_evaluation'
    technical_interview = 'technical_interview'
    ptc_round = 'ptc_round'
    founder_round = 'founder_round'

class StageOutcome(str, enum.Enum):
    approved = 'approved'
    rejected = 'rejected'
    pending = 'pending'

class Pipeline(Base):
    __tablename__ = 'pipelines'
    __table_args__ = (UniqueConstraint('candidate_id', 'requisition_id', name='uq_candidate_requisition'),)

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_id = Column(UUID(as_uuid=True), ForeignKey('candidates.id'), nullable=True)
    requisition_id = Column(UUID(as_uuid=True), ForeignKey('hiring_requisitions.id'), nullable=True)
    hiring_type = Column(SQLEnum(HiringType, name='hiring_type'), nullable=False, default=HiringType.inbound)
    current_stage = Column(SQLEnum(StageName, name='stage_name'), nullable=False, default=StageName.screening)
    status = Column(SQLEnum(PipelineStatus, name='pipeline_status'), default=PipelineStatus.active)
    referral_employee_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class StageHistory(Base):
    __tablename__ = 'stage_history'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pipeline_id = Column(UUID(as_uuid=True), ForeignKey('pipelines.id', ondelete='CASCADE'), nullable=False)
    stage = Column(SQLEnum(StageName, name='stage_name'), nullable=False)
    outcome = Column(SQLEnum(StageOutcome, name='stage_outcome'), default=StageOutcome.pending)
    remarks = Column(Text, nullable=True)
    actor_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    zoho_booking_id = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class FitmentTask(Base):
    __tablename__ = 'fitment_tasks'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    requisition_id = Column(UUID(as_uuid=True), ForeignKey('hiring_requisitions.id', ondelete='CASCADE'), nullable=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    file_url = Column(String, nullable=True)
    is_default = Column(Boolean, default=False)
    is_archived = Column(Boolean, default=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class CandidateSubmission(Base):
    __tablename__ = 'candidate_submissions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pipeline_id = Column(UUID(as_uuid=True), ForeignKey('pipelines.id', ondelete='CASCADE'), nullable=True)
    task_id = Column(UUID(as_uuid=True), ForeignKey('fitment_tasks.id'), nullable=True)
    s3_key = Column(String, nullable=False)
    s3_url = Column(String, nullable=False)
    original_name = Column(String, nullable=True)
    mime_type = Column(String, nullable=True)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
