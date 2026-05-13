from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    role: str
    department: Optional[str] = None

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[str] = None
    department: Optional[str] = None
    is_active: Optional[bool] = None

class UserOut(BaseModel):
    id: UUID
    email: str
    full_name: str
    role: str
    department: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class EmailTemplateCreate(BaseModel):
    name: str
    subject: str
    body_html: str
    is_active: Optional[bool] = True

class EmailTemplateOut(BaseModel):
    id: UUID
    name: str
    subject: str
    body_html: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
