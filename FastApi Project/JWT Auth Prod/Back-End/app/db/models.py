from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class Role(Base):
    __tablename__ = "roles"

    # Admin can add roles like "HR", "Manager", etc.
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    
    # Relationship with User
    users = relationship("User", back_populates="role")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Optional fields
    full_name = Column(String, nullable=True)
    
    # Foreign key to Role
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=True)
    
    # Timestamps for auditing
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship with Role
    role = relationship("Role", back_populates="users")
