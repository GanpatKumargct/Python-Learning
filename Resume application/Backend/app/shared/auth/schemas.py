from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    full_name: str
    role: str
    department: Optional[str] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class SendMagicLinkRequest(BaseModel):
    email: EmailStr
    purpose: str = "magic_link"

class VerifyMagicLinkRequest(BaseModel):
    email: EmailStr
    token: str
    purpose: str = "magic_link"

class CandidateMagicLinkVerifyResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
