from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime
from app.schemas.role import Role

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    is_active: Optional[bool] = True

class UserCreate(UserBase):
    password: str

class UserUpdateRole(BaseModel):
    role_id: int

class User(UserBase):
    id: int
    role_id: Optional[int] = None
    role: Optional[Role] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
