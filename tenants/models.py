from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

from sankalpa.backend.db.database import Base

class Tenant(Base):
    """Model for multi-tenant organizations"""
    __tablename__ = "tenants"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    slug = Column(String(50), unique=True, nullable=False, index=True)
    domain = Column(String(255), unique=True, nullable=True)
    logo = Column(String(255), nullable=True)
    primary_color = Column(String(20), nullable=True, default="#3B82F6")  # Default is blue-500
    description = Column(Text, nullable=True)
    features = Column(JSON, nullable=True)  # Enabled features
    limits = Column(JSON, nullable=True)  # Resource limits
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    users = relationship("TenantUser", back_populates="tenant")
    invitations = relationship("TenantInvitation", back_populates="tenant")
    api_keys = relationship("TenantApiKey", back_populates="tenant")

class TenantUser(Base):
    """Association table between tenants and users with roles"""
    __tablename__ = "tenant_users"
    
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    role = Column(String(20), default="member")  # owner, admin, member
    is_default = Column(Boolean, default=False)  # Is this the user's default tenant
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="users")
    user = relationship("User", back_populates="tenants")

class TenantInvitation(Base):
    """Model for tenant invitations"""
    __tablename__ = "tenant_invitations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    email = Column(String(255), nullable=False)
    role = Column(String(20), default="member")
    token = Column(String(100), unique=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="invitations")
    inviter = relationship("User", foreign_keys=[created_by])

class TenantApiKey(Base):
    """Model for tenant-specific API keys"""
    __tablename__ = "tenant_api_keys"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    name = Column(String(100), nullable=False)
    key = Column(String(100), unique=True, nullable=False)
    scopes = Column(JSON, nullable=True)  # Allowed scopes for this key
    expires_at = Column(DateTime, nullable=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_used_at = Column(DateTime, nullable=True)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="api_keys")
    creator = relationship("User", foreign_keys=[created_by])