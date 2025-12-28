from pydantic import BaseModel, Field, validator, EmailStr
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid
import re

# Tenant schemas
class TenantBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    slug: str = Field(..., min_length=3, max_length=50, regex=r'^[a-z0-9-]+$')
    domain: Optional[str] = None
    logo: Optional[str] = None
    primary_color: Optional[str] = Field(None, max_length=20)
    description: Optional[str] = None
    features: Optional[Dict[str, Any]] = None
    limits: Optional[Dict[str, Any]] = None

class TenantCreate(TenantBase):
    set_as_default: bool = False

class TenantUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    domain: Optional[str] = None
    logo: Optional[str] = None
    primary_color: Optional[str] = Field(None, max_length=20)
    description: Optional[str] = None
    features: Optional[Dict[str, Any]] = None
    limits: Optional[Dict[str, Any]] = None
    set_as_default: bool = False

class TenantResponse(TenantBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    user_role: Optional[str] = None
    is_default: Optional[bool] = None
    
    class Config:
        orm_mode = True

# Tenant User schemas
class TenantUserBase(BaseModel):
    tenant_id: uuid.UUID
    user_id: uuid.UUID
    role: str
    is_default: bool

class TenantUserResponse(TenantUserBase):
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

# Tenant Invitation schemas
class TenantInvitationBase(BaseModel):
    email: EmailStr
    role: str = Field("member", regex=r'^(owner|admin|member)$')

class TenantInvitationCreate(TenantInvitationBase):
    pass

class TenantInvitationResponse(TenantInvitationBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    token: str
    expires_at: datetime
    created_by: uuid.UUID
    created_at: datetime
    
    class Config:
        orm_mode = True

# Tenant API Key schemas
class TenantApiKeyBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    scopes: Optional[List[str]] = None
    expires_in_days: Optional[int] = Field(None, ge=1, le=365)

class TenantApiKeyCreate(TenantApiKeyBase):
    pass

class TenantApiKeyResponse(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    name: str
    key: str
    scopes: Optional[List[str]] = None
    expires_at: Optional[datetime] = None
    created_by: uuid.UUID
    created_at: datetime
    last_used_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True