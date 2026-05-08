from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Literal

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Literal["completed", "not completed"] = "not completed"

class TaskCreate(TaskBase):
    pass

class TaskOut(TaskBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None