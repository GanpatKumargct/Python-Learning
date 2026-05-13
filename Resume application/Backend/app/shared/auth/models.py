import uuid
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class UserRole(str, enum.Enum):
    admin = 'admin'
    ptc = 'ptc'
    founder = 'founder'
    project_director = 'project_director'
    chief_of_staff = 'chief_of_staff'
    hiring_manager = 'hiring_manager'
    supporting_member = 'supporting_member'

class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    password_hash = Column(String, nullable=True)
    role = Column(SQLEnum(UserRole, name='user_role'), nullable=False)
    department = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

class AuthOTP(Base):
    __tablename__ = 'auth_otp'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, nullable=False)
    otp_hash = Column(String, nullable=False)
    purpose = Column(String, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    used_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    token_hash = Column(String, unique=True, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    revoked_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
