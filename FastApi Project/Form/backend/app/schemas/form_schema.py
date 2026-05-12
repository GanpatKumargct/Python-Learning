from pydantic import BaseModel, ConfigDict, Field
from typing import Dict, Any, Optional
from datetime import datetime
from uuid import UUID

class FormBase(BaseModel):
    title: str
    description: Optional[str] = None
    slug: Optional[str] = None
    status: str = "draft"
    form_schema: Dict[str, Any] = Field(default_factory=dict)
    settings: Optional[Dict[str, Any]] = Field(default_factory=dict)
    theme: Optional[Dict[str, Any]] = Field(default_factory=dict)

class FormCreate(FormBase):
    pass

class FormUpdate(FormBase):
    title: Optional[str] = None
    version: Optional[int] = None

class FormResponse(FormBase):
    id: UUID
    version: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
