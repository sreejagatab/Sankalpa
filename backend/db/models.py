
import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
import uuid
from datetime import datetime
from typing import Optional, List

from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text, JSON, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from backend.db.database import Base

class User(Base):
    """User model for authentication and authorization"""
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(100))
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    roles = relationship("UserRole", back_populates="user")
    api_keys = relationship("ApiKey", back_populates="user")
    chains = relationship("Chain", back_populates="owner")
    memory_sessions = relationship("MemorySession", back_populates="owner")

class Role(Base):
    """Role model for role-based access control"""
    __tablename__ = "roles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255))
    
    # Relationships
    users = relationship("UserRole", back_populates="role")
    permissions = relationship("RolePermission", back_populates="role")

class Permission(Base):
    """Permission model for fine-grained access control"""
    __tablename__ = "permissions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255))
    
    # Relationships
    roles = relationship("RolePermission", back_populates="permission")

class UserRole(Base):
    """User-role association table"""
    __tablename__ = "user_roles"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"), primary_key=True)
    
    # Relationships
    user = relationship("User", back_populates="roles")
    role = relationship("Role", back_populates="users")

class RolePermission(Base):
    """Role-permission association table"""
    __tablename__ = "role_permissions"
    
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"), primary_key=True)
    permission_id = Column(UUID(as_uuid=True), ForeignKey("permissions.id"), primary_key=True)
    
    # Relationships
    role = relationship("Role", back_populates="permissions")
    permission = relationship("Permission", back_populates="roles")

class ApiKey(Base):
    """API key model for API access"""
    __tablename__ = "api_keys"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    name = Column(String(100), nullable=False)
    key = Column(String(255), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_used_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="api_keys")

class Agent(Base):
    """Agent model for storing agent metadata"""
    __tablename__ = "agents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    category = Column(String(50), index=True)
    version = Column(String(20))
    input_schema = Column(JSON)
    output_schema = Column(JSON)
    
    # Relationships
    chain_links = relationship("ChainLink", back_populates="agent")
    executions = relationship("AgentExecution", back_populates="agent")

class Chain(Base):
    """Chain model for storing chain definitions"""
    __tablename__ = "chains"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    type = Column(String(20), default="sequential")  # sequential, parallel, conditional
    condition_key = Column(String(100), nullable=True)  # For conditional chains
    condition_branches = Column(JSON, nullable=True)  # For conditional chains
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    owner = relationship("User", back_populates="chains")
    links = relationship("ChainLink", back_populates="chain")
    executions = relationship("ChainExecution", back_populates="chain")

class ChainLink(Base):
    """Chain link model for storing agent order in chains"""
    __tablename__ = "chain_links"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chain_id = Column(UUID(as_uuid=True), ForeignKey("chains.id"), nullable=False)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id"), nullable=False)
    position = Column(Integer, nullable=False)
    config = Column(JSON, nullable=True)  # Agent-specific configuration
    
    # Relationships
    chain = relationship("Chain", back_populates="links")
    agent = relationship("Agent", back_populates="chain_links")

class MemorySession(Base):
    """Memory session model for persistent memory storage"""
    __tablename__ = "memory_sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_accessed_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    owner = relationship("User", back_populates="memory_sessions")
    items = relationship("MemoryItem", back_populates="session")
    chain_executions = relationship("ChainExecution", back_populates="memory_session")

class MemoryItem(Base):
    """Memory item model for storing key-value data"""
    __tablename__ = "memory_items"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("memory_sessions.id"), nullable=False)
    key = Column(String(255), nullable=False)
    value = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    session = relationship("MemorySession", back_populates="items")
    
    __table_args__ = (
        # Unique constraint for session_id + key
        {},
    )

class AgentExecution(Base):
    """Agent execution model for tracking agent runs"""
    __tablename__ = "agent_executions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id"), nullable=False)
    chain_execution_id = Column(UUID(as_uuid=True), ForeignKey("chain_executions.id"), nullable=True)
    input_data = Column(JSON)
    output_data = Column(JSON)
    status = Column(String(20), index=True)  # pending, running, success, failure
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    execution_time = Column(Float)  # In seconds
    error = Column(Text, nullable=True)
    
    # Relationships
    agent = relationship("Agent", back_populates="executions")
    chain_execution = relationship("ChainExecution", back_populates="agent_executions")

class ChainExecution(Base):
    """Chain execution model for tracking chain runs"""
    __tablename__ = "chain_executions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chain_id = Column(UUID(as_uuid=True), ForeignKey("chains.id"), nullable=False)
    memory_session_id = Column(UUID(as_uuid=True), ForeignKey("memory_sessions.id"), nullable=False)
    input_data = Column(JSON)
    output_data = Column(JSON)
    status = Column(String(20), index=True)  # pending, running, success, failure
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    execution_time = Column(Float)  # In seconds
    metrics = Column(JSON, nullable=True)
    
    # Relationships
    chain = relationship("Chain", back_populates="executions")
    memory_session = relationship("MemorySession", back_populates="chain_executions")
    agent_executions = relationship("AgentExecution", back_populates="chain_execution")