from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from app.modules.ats.requisitions.models import RequisitionStatus, ApprovalStage, ApprovalDecision

class RequisitionCreate(BaseModel):
    title: str
    job_description: str
    scope_of_work: str
    department: str
    screening_form_id: Optional[UUID] = None
    supporting_members: Optional[List[UUID]] = None

class RequisitionOut(BaseModel):
    id: UUID
    title: str
    job_description: str
    scope_of_work: str
    department: Optional[str]
    status: RequisitionStatus
    created_by: Optional[UUID]
    screening_form_id: Optional[UUID]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ApprovalOut(BaseModel):
    id: UUID
    requisition_id: UUID
    stage: ApprovalStage
    decision: Optional[ApprovalDecision]
    remarks: Optional[str]
    decided_by: Optional[UUID]
    decided_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True

class RequisitionAction(BaseModel):
    decision: ApprovalDecision
    remarks: Optional[str] = None
