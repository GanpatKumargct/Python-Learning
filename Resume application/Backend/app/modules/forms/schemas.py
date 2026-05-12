from pydantic import BaseModel, constr
from typing import List, Optional, Any, Dict
from uuid import UUID
from datetime import datetime

class FormFieldCreate(BaseModel):
    field_key: str
    label: str
    field_type: str  # text, number, date, select, file, etc.
    is_required: bool = False
    options: Optional[List[str]] = None
    validation: Optional[Dict[str, Any]] = None
    display_order: int
    column_type: str = 'TEXT' # SQL column type

class FormCreate(BaseModel):
    title: str
    description: Optional[str] = None
    department: Optional[str] = None
    module: str = 'ats'
    fields: List[FormFieldCreate]

class FormFieldOut(BaseModel):
    id: UUID
    field_key: str
    label: str
    field_type: str
    is_required: bool
    options: Optional[List[str]]
    display_order: int

    class Config:
        from_attributes = True

class FormOut(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    department: Optional[str]
    response_table: str
    is_active: bool
    created_at: datetime
    fields: List[FormFieldOut]

    class Config:
        from_attributes = True
