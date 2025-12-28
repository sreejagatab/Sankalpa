from fastapi import APIRouter, Depends, HTTPException, Path, Body, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from datetime import datetime, timedelta
import secrets
import re
from sqlalchemy import desc

from sankalpa.backend.db.database import get_db
from sankalpa.core.security import get_current_user
from sankalpa.tenants.models import Tenant, TenantUser, TenantInvitation, TenantApiKey
from sankalpa.tenants.schemas import (
    TenantCreate, TenantUpdate, TenantResponse, TenantUserResponse,
    TenantInvitationCreate, TenantInvitationResponse, TenantApiKeyCreate,
    TenantApiKeyResponse
)
from sankalpa.core import get_logger
from sankalpa.core.caching import cache

router = APIRouter()
logger = get_logger("tenants")

# Dependency to get the current tenant based on header or subdomain
async def get_current_tenant(
    x_tenant_id: Optional[str] = Header(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get the current tenant based on request header or user's default tenant"""
    user_id = current_user["id"]
    
    if x_tenant_id:
        # Tenant specified in header
        tenant_user = db.query(TenantUser).filter(
            TenantUser.tenant_id == uuid.UUID(x_tenant_id),
            TenantUser.user_id == uuid.UUID(user_id)
        ).first()
        
        if not tenant_user:
            raise HTTPException(status_code=403, detail="You don't have access to this tenant")
            
        tenant = db.query(Tenant).filter(Tenant.id == uuid.UUID(x_tenant_id)).first()
        
        if not tenant:
            raise HTTPException(status_code=404, detail="Tenant not found")
            
        return tenant
    else:
        # Use default tenant
        tenant_user = db.query(TenantUser).filter(
            TenantUser.user_id == uuid.UUID(user_id),
            TenantUser.is_default == True
        ).first()
        
        if not tenant_user:
            # No default tenant, try to get any tenant
            tenant_user = db.query(TenantUser).filter(
                TenantUser.user_id == uuid.UUID(user_id)
            ).first()
            
            if not tenant_user:
                raise HTTPException(status_code=404, detail="No tenant found for user")
        
        tenant = db.query(Tenant).filter(Tenant.id == tenant_user.tenant_id).first()
        
        if not tenant:
            raise HTTPException(status_code=404, detail="Tenant not found")
            
        return tenant

# Create a new tenant
@router.post("/", response_model=TenantResponse, status_code=status.HTTP_201_CREATED)
async def create_tenant(
    tenant_data: TenantCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new tenant organization"""
    # Normalize and validate the slug
    slug = tenant_data.slug.lower()
    if not re.match(r'^[a-z0-9-]+$', slug):
        raise HTTPException(status_code=400, detail="Slug can only contain lowercase letters, numbers, and hyphens")
    
    # Check if slug is already taken
    existing_tenant = db.query(Tenant).filter(Tenant.slug == slug).first()
    if existing_tenant:
        raise HTTPException(status_code=400, detail="Slug is already taken")
    
    # Check if domain is already taken
    if tenant_data.domain:
        existing_domain = db.query(Tenant).filter(Tenant.domain == tenant_data.domain).first()
        if existing_domain:
            raise HTTPException(status_code=400, detail="Domain is already taken")
    
    # Create the tenant
    new_tenant = Tenant(
        name=tenant_data.name,
        slug=slug,
        domain=tenant_data.domain,
        logo=tenant_data.logo,
        primary_color=tenant_data.primary_color,
        description=tenant_data.description,
        features=tenant_data.features,
        limits=tenant_data.limits
    )
    
    db.add(new_tenant)
    db.flush()  # Flush to get the ID
    
    # Add the current user as the owner
    tenant_user = TenantUser(
        tenant_id=new_tenant.id,
        user_id=uuid.UUID(current_user["id"]),
        role="owner",
        is_default=tenant_data.set_as_default
    )
    
    db.add(tenant_user)
    
    # If this is the default tenant, update other tenants
    if tenant_data.set_as_default:
        db.query(TenantUser).filter(
            TenantUser.user_id == uuid.UUID(current_user["id"]),
            TenantUser.tenant_id != new_tenant.id
        ).update({"is_default": False})
    
    db.commit()
    db.refresh(new_tenant)
    
    logger.info(f"Tenant created: {new_tenant.id} ({new_tenant.name})")
    
    return new_tenant

# Get all tenants for the current user
@router.get("/", response_model=List[TenantResponse])
async def get_tenants(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all tenants for the current user"""
    tenant_users = db.query(TenantUser).filter(
        TenantUser.user_id == uuid.UUID(current_user["id"])
    ).all()
    
    tenant_ids = [tu.tenant_id for tu in tenant_users]
    
    tenants = db.query(Tenant).filter(Tenant.id.in_(tenant_ids)).all()
    
    # Enhance with role and default status
    for tenant in tenants:
        tu = next(tu for tu in tenant_users if tu.tenant_id == tenant.id)
        tenant.user_role = tu.role
        tenant.is_default = tu.is_default
    
    return tenants

# Get a specific tenant
@router.get("/{tenant_id}", response_model=TenantResponse)
async def get_tenant(
    tenant_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific tenant by ID"""
    # Check if user has access to this tenant
    tenant_user = db.query(TenantUser).filter(
        TenantUser.tenant_id == uuid.UUID(tenant_id),
        TenantUser.user_id == uuid.UUID(current_user["id"])
    ).first()
    
    if not tenant_user:
        raise HTTPException(status_code=403, detail="You don't have access to this tenant")
    
    tenant = db.query(Tenant).filter(Tenant.id == uuid.UUID(tenant_id)).first()
    
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    # Add role and default status
    tenant.user_role = tenant_user.role
    tenant.is_default = tenant_user.is_default
    
    return tenant

# Update a tenant
@router.put("/{tenant_id}", response_model=TenantResponse)
async def update_tenant(
    tenant_id: str,
    tenant_data: TenantUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a tenant"""
    # Check if user has access to this tenant
    tenant_user = db.query(TenantUser).filter(
        TenantUser.tenant_id == uuid.UUID(tenant_id),
        TenantUser.user_id == uuid.UUID(current_user["id"])
    ).first()
    
    if not tenant_user or tenant_user.role not in ["owner", "admin"]:
        raise HTTPException(status_code=403, detail="You don't have permission to update this tenant")
    
    tenant = db.query(Tenant).filter(Tenant.id == uuid.UUID(tenant_id)).first()
    
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    # Update fields
    if tenant_data.name is not None:
        tenant.name = tenant_data.name
    
    if tenant_data.domain is not None:
        # Check if domain is already taken
        if tenant_data.domain:
            existing_domain = db.query(Tenant).filter(
                Tenant.domain == tenant_data.domain,
                Tenant.id != uuid.UUID(tenant_id)
            ).first()
            if existing_domain:
                raise HTTPException(status_code=400, detail="Domain is already taken")
        tenant.domain = tenant_data.domain
    
    if tenant_data.logo is not None:
        tenant.logo = tenant_data.logo
    
    if tenant_data.primary_color is not None:
        tenant.primary_color = tenant_data.primary_color
    
    if tenant_data.description is not None:
        tenant.description = tenant_data.description
    
    if tenant_data.features is not None:
        tenant.features = tenant_data.features
    
    if tenant_data.limits is not None:
        tenant.limits = tenant_data.limits
    
    # Handle default tenant setting
    if tenant_data.set_as_default:
        db.query(TenantUser).filter(
            TenantUser.user_id == uuid.UUID(current_user["id"]),
            TenantUser.tenant_id != uuid.UUID(tenant_id)
        ).update({"is_default": False})
        
        tenant_user.is_default = True
    
    db.commit()
    db.refresh(tenant)
    
    # Add role and default status
    tenant.user_role = tenant_user.role
    tenant.is_default = tenant_user.is_default
    
    logger.info(f"Tenant updated: {tenant.id} ({tenant.name})")
    
    return tenant

# Delete a tenant
@router.delete("/{tenant_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tenant(
    tenant_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a tenant"""
    # Check if user has access to this tenant
    tenant_user = db.query(TenantUser).filter(
        TenantUser.tenant_id == uuid.UUID(tenant_id),
        TenantUser.user_id == uuid.UUID(current_user["id"])
    ).first()
    
    if not tenant_user or tenant_user.role != "owner":
        raise HTTPException(status_code=403, detail="Only the owner can delete a tenant")
    
    tenant = db.query(Tenant).filter(Tenant.id == uuid.UUID(tenant_id)).first()
    
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    # Delete tenant and all related records
    db.delete(tenant)
    db.commit()
    
    logger.info(f"Tenant deleted: {tenant_id}")
    
    return None

# Get users for a tenant
@router.get("/{tenant_id}/users", response_model=List[TenantUserResponse])
async def get_tenant_users(
    tenant_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all users for a tenant"""
    # Check if user has access to this tenant
    tenant_user = db.query(TenantUser).filter(
        TenantUser.tenant_id == uuid.UUID(tenant_id),
        TenantUser.user_id == uuid.UUID(current_user["id"])
    ).first()
    
    if not tenant_user:
        raise HTTPException(status_code=403, detail="You don't have access to this tenant")
    
    # Get all tenant users
    tenant_users = db.query(TenantUser).filter(
        TenantUser.tenant_id == uuid.UUID(tenant_id)
    ).all()
    
    return tenant_users

# Update a user's role in a tenant
@router.put("/{tenant_id}/users/{user_id}", response_model=TenantUserResponse)
async def update_tenant_user(
    tenant_id: str,
    user_id: str,
    role: str = Body(..., embed=True),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a user's role in a tenant"""
    # Check if current user is owner or admin
    current_tenant_user = db.query(TenantUser).filter(
        TenantUser.tenant_id == uuid.UUID(tenant_id),
        TenantUser.user_id == uuid.UUID(current_user["id"])
    ).first()
    
    if not current_tenant_user or current_tenant_user.role not in ["owner", "admin"]:
        raise HTTPException(status_code=403, detail="You don't have permission to update user roles")
    
    # Validate role
    if role not in ["admin", "member"]:
        raise HTTPException(status_code=400, detail="Invalid role. Must be 'admin' or 'member'")
    
    # Cannot change owner's role
    target_tenant_user = db.query(TenantUser).filter(
        TenantUser.tenant_id == uuid.UUID(tenant_id),
        TenantUser.user_id == uuid.UUID(user_id)
    ).first()
    
    if not target_tenant_user:
        raise HTTPException(status_code=404, detail="User not found in this tenant")
    
    if target_tenant_user.role == "owner":
        raise HTTPException(status_code=400, detail="Cannot change the owner's role")
    
    # Only owner can promote to admin
    if role == "admin" and current_tenant_user.role != "owner":
        raise HTTPException(status_code=403, detail="Only the owner can promote users to admin")
    
    # Update role
    target_tenant_user.role = role
    db.commit()
    db.refresh(target_tenant_user)
    
    logger.info(f"User role updated in tenant {tenant_id}: {user_id} is now {role}")
    
    return target_tenant_user

# Remove a user from a tenant
@router.delete("/{tenant_id}/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_tenant_user(
    tenant_id: str,
    user_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove a user from a tenant"""
    # Check if current user is owner or admin
    current_tenant_user = db.query(TenantUser).filter(
        TenantUser.tenant_id == uuid.UUID(tenant_id),
        TenantUser.user_id == uuid.UUID(current_user["id"])
    ).first()
    
    if not current_tenant_user or current_tenant_user.role not in ["owner", "admin"]:
        raise HTTPException(status_code=403, detail="You don't have permission to remove users")
    
    # Cannot remove owner
    target_tenant_user = db.query(TenantUser).filter(
        TenantUser.tenant_id == uuid.UUID(tenant_id),
        TenantUser.user_id == uuid.UUID(user_id)
    ).first()
    
    if not target_tenant_user:
        raise HTTPException(status_code=404, detail="User not found in this tenant")
    
    if target_tenant_user.role == "owner":
        raise HTTPException(status_code=400, detail="Cannot remove the owner from the tenant")
    
    # Only owner can remove admins
    if target_tenant_user.role == "admin" and current_tenant_user.role != "owner":
        raise HTTPException(status_code=403, detail="Only the owner can remove admins")
    
    # Cannot remove yourself
    if str(target_tenant_user.user_id) == current_user["id"]:
        raise HTTPException(status_code=400, detail="Cannot remove yourself from the tenant")
    
    # Remove user
    db.delete(target_tenant_user)
    db.commit()
    
    logger.info(f"User removed from tenant {tenant_id}: {user_id}")
    
    return None

# Create a tenant invitation
@router.post("/{tenant_id}/invitations", response_model=TenantInvitationResponse, status_code=status.HTTP_201_CREATED)
async def create_invitation(
    tenant_id: str,
    invitation_data: TenantInvitationCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create an invitation to join a tenant"""
    # Check if current user is owner or admin
    current_tenant_user = db.query(TenantUser).filter(
        TenantUser.tenant_id == uuid.UUID(tenant_id),
        TenantUser.user_id == uuid.UUID(current_user["id"])
    ).first()
    
    if not current_tenant_user or current_tenant_user.role not in ["owner", "admin"]:
        raise HTTPException(status_code=403, detail="You don't have permission to invite users")
    
    # Validate role
    if invitation_data.role not in ["admin", "member"]:
        raise HTTPException(status_code=400, detail="Invalid role. Must be 'admin' or 'member'")
    
    # Only owner can invite admins
    if invitation_data.role == "admin" and current_tenant_user.role != "owner":
        raise HTTPException(status_code=403, detail="Only the owner can invite admins")
    
    # Generate a secure token
    token = secrets.token_urlsafe(32)
    
    # Set expiration (48 hours from now)
    expires_at = datetime.utcnow() + timedelta(hours=48)
    
    # Create invitation
    invitation = TenantInvitation(
        tenant_id=uuid.UUID(tenant_id),
        email=invitation_data.email,
        role=invitation_data.role,
        token=token,
        expires_at=expires_at,
        created_by=uuid.UUID(current_user["id"])
    )
    
    db.add(invitation)
    db.commit()
    db.refresh(invitation)
    
    logger.info(f"Invitation created for {invitation_data.email} to join tenant {tenant_id}")
    
    return invitation

# List invitations for a tenant
@router.get("/{tenant_id}/invitations", response_model=List[TenantInvitationResponse])
async def list_invitations(
    tenant_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all pending invitations for a tenant"""
    # Check if current user is a member of the tenant
    current_tenant_user = db.query(TenantUser).filter(
        TenantUser.tenant_id == uuid.UUID(tenant_id),
        TenantUser.user_id == uuid.UUID(current_user["id"])
    ).first()
    
    if not current_tenant_user:
        raise HTTPException(status_code=403, detail="You don't have access to this tenant")
    
    # Get invitations that haven't expired
    invitations = db.query(TenantInvitation).filter(
        TenantInvitation.tenant_id == uuid.UUID(tenant_id),
        TenantInvitation.expires_at > datetime.utcnow()
    ).all()
    
    return invitations

# Delete an invitation
@router.delete("/{tenant_id}/invitations/{invitation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_invitation(
    tenant_id: str,
    invitation_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a pending invitation"""
    # Check if current user is owner or admin
    current_tenant_user = db.query(TenantUser).filter(
        TenantUser.tenant_id == uuid.UUID(tenant_id),
        TenantUser.user_id == uuid.UUID(current_user["id"])
    ).first()
    
    if not current_tenant_user or current_tenant_user.role not in ["owner", "admin"]:
        raise HTTPException(status_code=403, detail="You don't have permission to manage invitations")
    
    # Find the invitation
    invitation = db.query(TenantInvitation).filter(
        TenantInvitation.id == uuid.UUID(invitation_id),
        TenantInvitation.tenant_id == uuid.UUID(tenant_id)
    ).first()
    
    if not invitation:
        raise HTTPException(status_code=404, detail="Invitation not found")
    
    # Delete invitation
    db.delete(invitation)
    db.commit()
    
    logger.info(f"Invitation {invitation_id} deleted from tenant {tenant_id}")
    
    return None

# Accept an invitation
@router.post("/invitations/accept", response_model=TenantResponse)
async def accept_invitation(
    token: str = Body(..., embed=True),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Accept a tenant invitation"""
    # Find the invitation
    invitation = db.query(TenantInvitation).filter(
        TenantInvitation.token == token,
        TenantInvitation.expires_at > datetime.utcnow()
    ).first()
    
    if not invitation:
        raise HTTPException(status_code=404, detail="Invitation not found or expired")
    
    # Check if user email matches invitation email
    # In a real implementation, you'd query the user's email from the database
    # For this example, we'll allow any user to accept any invitation
    
    # Check if user is already a member
    existing_user = db.query(TenantUser).filter(
        TenantUser.tenant_id == invitation.tenant_id,
        TenantUser.user_id == uuid.UUID(current_user["id"])
    ).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="You are already a member of this tenant")
    
    # Add user to tenant
    tenant_user = TenantUser(
        tenant_id=invitation.tenant_id,
        user_id=uuid.UUID(current_user["id"]),
        role=invitation.role
    )
    
    db.add(tenant_user)
    
    # Delete the invitation
    db.delete(invitation)
    db.commit()
    
    # Get the tenant
    tenant = db.query(Tenant).filter(Tenant.id == invitation.tenant_id).first()
    
    # Add role and default status
    tenant.user_role = invitation.role
    tenant.is_default = False
    
    logger.info(f"User {current_user['id']} joined tenant {tenant.id} ({tenant.name})")
    
    return tenant

# Create an API key for a tenant
@router.post("/{tenant_id}/api-keys", response_model=TenantApiKeyResponse, status_code=status.HTTP_201_CREATED)
async def create_api_key(
    tenant_id: str,
    api_key_data: TenantApiKeyCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new API key for a tenant"""
    # Check if current user is owner or admin
    current_tenant_user = db.query(TenantUser).filter(
        TenantUser.tenant_id == uuid.UUID(tenant_id),
        TenantUser.user_id == uuid.UUID(current_user["id"])
    ).first()
    
    if not current_tenant_user or current_tenant_user.role not in ["owner", "admin"]:
        raise HTTPException(status_code=403, detail="You don't have permission to create API keys")
    
    # Generate a secure API key
    api_key = f"sk-{secrets.token_urlsafe(32)}"
    
    # Calculate expiration if provided
    expires_at = None
    if api_key_data.expires_in_days:
        expires_at = datetime.utcnow() + timedelta(days=api_key_data.expires_in_days)
    
    # Create API key
    new_api_key = TenantApiKey(
        tenant_id=uuid.UUID(tenant_id),
        name=api_key_data.name,
        key=api_key,
        scopes=api_key_data.scopes,
        expires_at=expires_at,
        created_by=uuid.UUID(current_user["id"])
    )
    
    db.add(new_api_key)
    db.commit()
    db.refresh(new_api_key)
    
    logger.info(f"API key created for tenant {tenant_id}: {new_api_key.id} ({new_api_key.name})")
    
    return new_api_key

# List API keys for a tenant
@router.get("/{tenant_id}/api-keys", response_model=List[TenantApiKeyResponse])
async def list_api_keys(
    tenant_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all API keys for a tenant"""
    # Check if current user is a member of the tenant
    current_tenant_user = db.query(TenantUser).filter(
        TenantUser.tenant_id == uuid.UUID(tenant_id),
        TenantUser.user_id == uuid.UUID(current_user["id"])
    ).first()
    
    if not current_tenant_user:
        raise HTTPException(status_code=403, detail="You don't have access to this tenant")
    
    # Get API keys for tenant
    api_keys = db.query(TenantApiKey).filter(
        TenantApiKey.tenant_id == uuid.UUID(tenant_id)
    ).order_by(desc(TenantApiKey.created_at)).all()
    
    return api_keys

# Delete an API key
@router.delete("/{tenant_id}/api-keys/{api_key_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_api_key(
    tenant_id: str,
    api_key_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete an API key"""
    # Check if current user is owner or admin
    current_tenant_user = db.query(TenantUser).filter(
        TenantUser.tenant_id == uuid.UUID(tenant_id),
        TenantUser.user_id == uuid.UUID(current_user["id"])
    ).first()
    
    if not current_tenant_user or current_tenant_user.role not in ["owner", "admin"]:
        raise HTTPException(status_code=403, detail="You don't have permission to delete API keys")
    
    # Find the API key
    api_key = db.query(TenantApiKey).filter(
        TenantApiKey.id == uuid.UUID(api_key_id),
        TenantApiKey.tenant_id == uuid.UUID(tenant_id)
    ).first()
    
    if not api_key:
        raise HTTPException(status_code=404, detail="API key not found")
    
    # Delete API key
    db.delete(api_key)
    db.commit()
    
    logger.info(f"API key {api_key_id} deleted from tenant {tenant_id}")
    
    return None