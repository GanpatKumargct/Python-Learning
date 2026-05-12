from pydantic import BaseModel, ConfigDict
from typing import Dict, Any, Optional
from datetime import datetime
from uuid import UUID

class SubmissionBase(BaseModel):
    submission_data: Dict[str, Any]
    metadata_: Optional[Dict[str, Any]] = None

class SubmissionCreate(SubmissionBase):
    pass

class SubmissionResponse(SubmissionBase):
    id: UUID
    form_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
