from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.modules.auth.models import UserRole

class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    role: UserRole
    department: Optional[str] = None
    password: str # Temporary password assigned by admin

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    department: Optional[str] = None
    is_active: Optional[bool] = None

class UserOut(BaseModel):
    id: UUID
    email: str
    full_name: str
    role: UserRole
    department: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
