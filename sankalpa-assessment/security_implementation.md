# Sankalpa Security Implementation Plan

## Overview

This document outlines the security implementation plan for the Sankalpa platform, focusing on authentication, authorization, data protection, and secure coding practices.

## 1. Authentication System

### JWT Authentication Implementation

```python
# backend/core/security.py
from datetime import datetime, timedelta
from typing import Optional, Union
from jose import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from backend.core.config import settings
from backend.db.models import User
from backend.db.repositories.user_repository import UserRepository

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# Token models
class Token(BaseModel):
    access_token: str
    token_type: str
    expires_at: datetime
    refresh_token: Optional[str] = None

class TokenData(BaseModel):
    username: Optional[str] = None
    scopes: list[str] = []

# Password utilities
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Token generation
def create_access_token(
    data: dict, 
    expires_delta: Optional[timedelta] = None
) -> str:
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt

def create_refresh_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
) -> str:
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        
    to_encode.update({"exp": expire, "refresh": True})
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.REFRESH_TOKEN_SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt

# Token validation and user extraction
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repo: UserRepository = Depends()
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
            
        token_data = TokenData(username=username, scopes=payload.get("scopes", []))
    except jwt.JWTError:
        raise credentials_exception
        
    user = await user_repo.get_by_username(token_data.username)
    if user is None:
        raise credentials_exception
        
    return user

# Role-based authentication
async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Check for admin role
async def get_current_admin_user(
    current_user: User = Depends(get_current_active_user),
) -> User:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user

# Check for specific permissions
def has_permission(required_permission: str):
    async def permission_checker(
        current_user: User = Depends(get_current_active_user),
    ) -> User:
        user_permissions = current_user.permissions or []
        if (not current_user.is_admin and 
            required_permission not in user_permissions):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing required permission: {required_permission}"
            )
        return current_user
    return permission_checker
```

### Authentication API Endpoints

```python
# backend/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel, EmailStr

from backend.core.security import (
    get_password_hash, verify_password, create_access_token,
    create_refresh_token, get_current_active_user
)
from backend.db.models import User
from backend.db.repositories.user_repository import UserRepository
from backend.core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

# Models
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    is_admin: bool
    permissions: List[str] = []
    
    class Config:
        orm_mode = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_at: datetime
    refresh_token: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str

# Endpoints
@router.post("/signup", response_model=UserResponse)
async def signup(
    user_create: UserCreate,
    user_repo: UserRepository = Depends()
):
    # Check if user already exists
    db_user = await user_repo.get_by_username(user_create.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
        
    db_user = await user_repo.get_by_email(user_create.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user with hashed password
    hashed_password = get_password_hash(user_create.password)
    new_user = User(
        username=user_create.username,
        email=user_create.email,
        hashed_password=hashed_password
    )
    
    created_user = await user_repo.create(new_user)
    return created_user

@router.post("/token", response_model=TokenResponse)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_repo: UserRepository = Depends()
):
    # Authenticate user
    user = await user_repo.get_by_username(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": user.permissions or []},
        expires_delta=access_token_expires
    )
    
    # Create refresh token
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = create_refresh_token(
        data={"sub": user.username},
        expires_delta=refresh_token_expires
    )
    
    # Calculate expiration time
    expires_at = datetime.utcnow() + access_token_expires
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_at": expires_at,
        "refresh_token": refresh_token
    }

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    user_repo: UserRepository = Depends()
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode refresh token
        payload = jwt.decode(
            refresh_data.refresh_token, 
            settings.REFRESH_TOKEN_SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        
        # Check if it's a refresh token
        if not payload.get("refresh"):
            raise credentials_exception
            
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.JWTError:
        raise credentials_exception
    
    # Get user
    user = await user_repo.get_by_username(username)
    if user is None or not user.is_active:
        raise credentials_exception
    
    # Create new tokens
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": user.permissions or []},
        expires_delta=access_token_expires
    )
    
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    new_refresh_token = create_refresh_token(
        data={"sub": user.username},
        expires_delta=refresh_token_expires
    )
    
    # Calculate expiration time
    expires_at = datetime.utcnow() + access_token_expires
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_at": expires_at,
        "refresh_token": new_refresh_token
    }

@router.get("/me", response_model=UserResponse)
async def read_users_me(
    current_user: User = Depends(get_current_active_user)
):
    return current_user
```

## 2. Role-Based Access Control

### User and Role Models

```python
# backend/db/models.py
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, JSON, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import datetime

from .base import Base

# Association table for user-role many-to-many relationship
user_role = Table(
    "user_role",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True)
)

# User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    permissions = Column(JSON, default=list)
    
    # Relationships
    roles = relationship("Role", secondary=user_role, back_populates="users")
    agent_runs = relationship("AgentRun", back_populates="user")
    sessions = relationship("Session", back_populates="user")

# Role model
class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    permissions = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    users = relationship("User", secondary=user_role, back_populates="roles")
```

### Role Management API

```python
# backend/routers/admin/roles.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from pydantic import BaseModel

from backend.core.security import get_current_admin_user
from backend.db.models import User, Role
from backend.db.repositories.role_repository import RoleRepository
from backend.db.repositories.user_repository import UserRepository

router = APIRouter(prefix="/admin/roles", tags=["admin", "roles"])

# Models
class RoleCreate(BaseModel):
    name: str
    description: Optional[str] = None
    permissions: List[str] = []

class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    permissions: Optional[List[str]] = None

class RoleResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    permissions: List[str] = []
    
    class Config:
        orm_mode = True

class AssignRoleRequest(BaseModel):
    user_id: int
    role_id: int

# Endpoints
@router.post("/", response_model=RoleResponse)
async def create_role(
    role_create: RoleCreate,
    role_repo: RoleRepository = Depends(),
    _: User = Depends(get_current_admin_user)
):
    # Check if role already exists
    existing_role = await role_repo.get_by_name(role_create.name)
    if existing_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Role with name '{role_create.name}' already exists"
        )
    
    # Create role
    new_role = Role(
        name=role_create.name,
        description=role_create.description,
        permissions=role_create.permissions
    )
    
    created_role = await role_repo.create(new_role)
    return created_role

@router.get("/", response_model=List[RoleResponse])
async def list_roles(
    skip: int = 0,
    limit: int = 100,
    role_repo: RoleRepository = Depends(),
    _: User = Depends(get_current_admin_user)
):
    roles = await role_repo.get_all(skip=skip, limit=limit)
    return roles

@router.get("/{role_id}", response_model=RoleResponse)
async def get_role(
    role_id: int,
    role_repo: RoleRepository = Depends(),
    _: User = Depends(get_current_admin_user)
):
    role = await role_repo.get_by_id(role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role with ID {role_id} not found"
        )
    return role

@router.put("/{role_id}", response_model=RoleResponse)
async def update_role(
    role_id: int,
    role_update: RoleUpdate,
    role_repo: RoleRepository = Depends(),
    _: User = Depends(get_current_admin_user)
):
    # Check if role exists
    role = await role_repo.get_by_id(role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role with ID {role_id} not found"
        )
    
    # Check if name is being changed and already exists
    if role_update.name and role_update.name != role.name:
        existing_role = await role_repo.get_by_name(role_update.name)
        if existing_role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Role with name '{role_update.name}' already exists"
            )
    
    # Update role
    updated_data = role_update.dict(exclude_unset=True)
    updated_role = await role_repo.update(role_id, updated_data)
    return updated_role

@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(
    role_id: int,
    role_repo: RoleRepository = Depends(),
    _: User = Depends(get_current_admin_user)
):
    # Check if role exists
    role = await role_repo.get_by_id(role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role with ID {role_id} not found"
        )
    
    # Delete role
    await role_repo.delete(role_id)
    return {"message": "Role deleted successfully"}

@router.post("/assign", status_code=status.HTTP_200_OK)
async def assign_role_to_user(
    assign_request: AssignRoleRequest,
    role_repo: RoleRepository = Depends(),
    user_repo: UserRepository = Depends(),
    _: User = Depends(get_current_admin_user)
):
    # Check if user exists
    user = await user_repo.get_by_id(assign_request.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {assign_request.user_id} not found"
        )
    
    # Check if role exists
    role = await role_repo.get_by_id(assign_request.role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role with ID {assign_request.role_id} not found"
        )
    
    # Assign role to user
    await role_repo.assign_role_to_user(user.id, role.id)
    
    # Update user's permissions with role's permissions
    user_permissions = set(user.permissions or [])
    role_permissions = set(role.permissions or [])
    updated_permissions = list(user_permissions.union(role_permissions))
    
    await user_repo.update(user.id, {"permissions": updated_permissions})
    
    return {"message": f"Role '{role.name}' assigned to user '{user.username}'"}

@router.post("/revoke", status_code=status.HTTP_200_OK)
async def revoke_role_from_user(
    assign_request: AssignRoleRequest,
    role_repo: RoleRepository = Depends(),
    user_repo: UserRepository = Depends(),
    _: User = Depends(get_current_admin_user)
):
    # Check if user exists
    user = await user_repo.get_by_id(assign_request.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {assign_request.user_id} not found"
        )
    
    # Check if role exists
    role = await role_repo.get_by_id(assign_request.role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role with ID {assign_request.role_id} not found"
        )
    
    # Revoke role from user
    await role_repo.revoke_role_from_user(user.id, role.id)
    
    # Recalculate user's permissions based on remaining roles
    user_roles = await role_repo.get_roles_for_user(user.id)
    all_permissions = set()
    for r in user_roles:
        if r.id != role.id:  # Skip the revoked role
            all_permissions.update(r.permissions or [])
    
    await user_repo.update(user.id, {"permissions": list(all_permissions)})
    
    return {"message": f"Role '{role.name}' revoked from user '{user.username}'"}
```

## 3. Secure API Configuration

### Environment Configuration

```python
# backend/core/config.py
import os
import secrets
from typing import List, Optional, Union
from pydantic import BaseSettings, validator, AnyHttpUrl

class Settings(BaseSettings):
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Sankalpa"
    
    # CORS settings
    CORS_ORIGINS: List[AnyHttpUrl] = []
    
    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # Database settings
    DATABASE_URL: str
    
    # Security settings
    SECRET_KEY: str
    REFRESH_TOKEN_SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = ENVIRONMENT == "development"
    
    # Rate limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_DEFAULT_LIMIT: int = 100
    RATE_LIMIT_DEFAULT_PERIOD: int = 60  # seconds
    
    # Agent settings
    AGENT_TIMEOUT_SECONDS: int = 600  # 10 minutes
    
    # File storage
    PROJECTS_DIR: str = "projects"
    
    @validator("SECRET_KEY", "REFRESH_TOKEN_SECRET_KEY", pre=True)
    def generate_secret_key(cls, v: Optional[str]) -> str:
        return v or secrets.token_urlsafe(32)
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

### API Rate Limiting

```python
# backend/middleware/rate_limit.py
from fastapi import FastAPI, Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
import time
import redis
from typing import Optional, Tuple, Dict, Any

from backend.core.config import settings

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(
        self, 
        app: FastAPI, 
        redis_client: redis.Redis,
        limit: int = settings.RATE_LIMIT_DEFAULT_LIMIT,
        period: int = settings.RATE_LIMIT_DEFAULT_PERIOD,
        enabled: bool = settings.RATE_LIMIT_ENABLED,
        exclude_paths: Tuple[str, ...] = ("/docs", "/openapi.json", "/redoc")
    ):
        super().__init__(app)
        self.redis_client = redis_client
        self.limit = limit
        self.period = period
        self.enabled = enabled
        self.exclude_paths = exclude_paths

    async def dispatch(self, request: Request, call_next):
        if not self.enabled or request.url.path in self.exclude_paths:
            return await call_next(request)
        
        # Generate a rate limit key based on IP and endpoint
        client_ip = request.client.host
        key = f"rate_limit:{client_ip}:{request.url.path}"
        
        # Check if custom rate limits apply for this path
        path_limit, path_period = self._get_path_specific_limits(request.url.path)
        
        # Apply rate limiting
        current_count = self._increment_counter(key, path_period or self.period)
        
        # Set headers
        response = await call_next(request)
        
        # Add rate limit headers to response
        response.headers["X-RateLimit-Limit"] = str(path_limit or self.limit)
        response.headers["X-RateLimit-Remaining"] = str(max(0, (path_limit or self.limit) - current_count))
        response.headers["X-RateLimit-Reset"] = str(self._get_counter_ttl(key))
        
        # If limit exceeded, return 429 Too Many Requests
        if current_count > (path_limit or self.limit):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded"
            )
        
        return response
    
    def _increment_counter(self, key: str, period: int) -> int:
        pipeline = self.redis_client.pipeline()
        pipeline.incr(key)
        pipeline.expire(key, period)
        result = pipeline.execute()
        return result[0]
    
    def _get_counter_ttl(self, key: str) -> int:
        ttl = self.redis_client.ttl(key)
        return max(0, ttl)
    
    def _get_path_specific_limits(self, path: str) -> Tuple[Optional[int], Optional[int]]:
        # Define custom rate limits for specific paths
        path_specific_limits: Dict[str, Tuple[int, int]] = {
            "/api/v1/agents/run": (5, 60),  # 5 requests per minute
            "/api/v1/chains/run": (3, 60),  # 3 requests per minute
            "/api/v1/auth/token": (10, 60),  # 10 login attempts per minute
        }
        
        # Find the matching path pattern (can be enhanced with regex)
        for pattern, (limit, period) in path_specific_limits.items():
            if path.startswith(pattern):
                return limit, period
                
        return None, None
```

## 4. API Input Validation

### Pydantic Models for Request Validation

```python
# backend/schemas/agents.py
from pydantic import BaseModel, validator, constr
from typing import Dict, Any, List, Optional

class AgentInput(BaseModel):
    prompt: str
    context: Optional[Dict[str, Any]] = {}
    
    @validator('prompt')
    def prompt_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Prompt cannot be empty')
        return v
    
    @validator('context')
    def validate_context(cls, v):
        # Ensure that the context doesn't contain potential security issues
        # For example, by checking for specific keys that might cause problems
        dangerous_keys = ['exec', 'eval', 'system', 'os', '__']
        for key in v.keys():
            for d_key in dangerous_keys:
                if d_key in key.lower():
                    raise ValueError(f'Context contains potentially dangerous key: {key}')
        return v

class AgentOutput(BaseModel):
    message: str
    files: Optional[Dict[str, str]] = {}
    data: Optional[Dict[str, Any]] = {}
    error: Optional[str] = None

class ChainConfig(BaseModel):
    name: constr(min_length=1, max_length=100)
    type: str = "sequential"
    agents: List[str]
    conditions: Optional[Dict[str, Dict[str, str]]] = {}
    
    @validator('type')
    def validate_chain_type(cls, v):
        valid_types = ["sequential", "parallel", "conditional"]
        if v not in valid_types:
            raise ValueError(f'Chain type must be one of: {", ".join(valid_types)}')
        return v
    
    @validator('agents')
    def validate_agents(cls, v):
        if not v:
            raise ValueError('Chain must contain at least one agent')
        
        # Check for potentially dangerous agent names
        dangerous_patterns = ['exec', 'shell', 'system', 'os', '__']
        for agent in v:
            for pattern in dangerous_patterns:
                if pattern in agent.lower():
                    raise ValueError(f'Agent name contains potentially dangerous pattern: {agent}')
        
        return v
```

## 5. Secure Deployment Practices

### HTTPS Configuration

```python
# backend/main.py with HTTPS redirect middleware
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.sessions import SessionMiddleware
from contextlib import asynccontextmanager

from backend.core.config import settings
from backend.routers import api, agents, auth, memory
from backend.middleware.rate_limit import RateLimitMiddleware
from backend.core.logging import setup_logging
from backend.db.base import init_db
from backend.core.redis import get_redis_client

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup logging
    setup_logging()
    
    # Initialize the database
    await init_db()
    
    yield
    # Cleanup resources

app = FastAPI(
    title="Sankalpa API",
    description="API for AI-powered software development automation",
    version="1.0.0",
    lifespan=lifespan,
)

# Add HTTPS redirect in production
if settings.ENVIRONMENT == "production":
    app.add_middleware(HTTPSRedirectMiddleware)

# Add session middleware for stateful sessions
app.add_middleware(
    SessionMiddleware, 
    secret_key=settings.SECRET_KEY,
    max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
)

# Add rate limiting
redis_client = get_redis_client()
app.add_middleware(
    RateLimitMiddleware,
    redis_client=redis_client
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api.router)
app.include_router(agents.router)
app.include_router(auth.router)
app.include_router(memory.router)

@app.get("/")
async def root():
    return {"message": "Sankalpa API is running", "version": "1.0.0"}
```

### Security Headers Middleware

```python
# backend/middleware/security_headers.py
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self' data:; connect-src 'self'"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "accelerometer=(), camera=(), geolocation=(), gyroscope=(), magnetometer=(), microphone=(), payment=(), usb=()"
        
        return response
```

## 6. Data Protection

### Sensitive Data Handling

```python
# backend/utils/data_protection.py
import re
from typing import Dict, Any, List, Set

class DataProtection:
    @staticmethod
    def sanitize_output(data: Dict[str, Any], sensitive_keys: Set[str] = None) -> Dict[str, Any]:
        """
        Sanitize output data by removing or masking sensitive information
        """
        if sensitive_keys is None:
            sensitive_keys = {
                'password', 'token', 'key', 'secret', 'auth', 'credential', 'api_key',
                'apikey', 'private', 'hash', 'ssn', 'social', 'credit', 'card'
            }
            
        result = {}
        
        for key, value in data.items():
            # Check if key might contain sensitive information
            key_lower = key.lower()
            is_sensitive = any(sk in key_lower for sk in sensitive_keys)
            
            if is_sensitive:
                # Mask sensitive values
                if isinstance(value, str):
                    result[key] = DataProtection._mask_string(value)
                else:
                    result[key] = "[REDACTED]"
            elif isinstance(value, dict):
                # Recursively sanitize nested dictionaries
                result[key] = DataProtection.sanitize_output(value, sensitive_keys)
            elif isinstance(value, list):
                # Recursively sanitize lists
                result[key] = [
                    DataProtection.sanitize_output(item, sensitive_keys) if isinstance(item, dict)
                    else item for item in value
                ]
            else:
                # Pass through other values
                result[key] = value
                
        return result
    
    @staticmethod
    def _mask_string(value: str) -> str:
        """
        Mask a sensitive string value
        """
        if not value:
            return ""
            
        # Keep first 2 and last 2 characters visible
        visible_chars = 4
        if len(value) <= visible_chars:
            return "*" * len(value)
            
        visible_prefix = 2
        visible_suffix = 2
        
        masked_part = "*" * (len(value) - visible_prefix - visible_suffix)
        return value[:visible_prefix] + masked_part + value[-visible_suffix:]
    
    @staticmethod
    def detect_pii(text: str) -> List[str]:
        """
        Detect potential PII (Personally Identifiable Information) in text
        """
        pii_patterns = {
            "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "ssn": r'\b\d{3}[-]?\d{2}[-]?\d{4}\b',
            "credit_card": r'\b(?:\d{4}[-]?){3}\d{4}\b',
            "phone": r'\b(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b',
            "ip_address": r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
        }
        
        found_pii = []
        
        for pii_type, pattern in pii_patterns.items():
            matches = re.findall(pattern, text)
            if matches:
                found_pii.append(f"{pii_type}: {len(matches)} instance(s)")
                
        return found_pii
    
    @staticmethod
    def sanitize_file_content(content: str) -> str:
        """
        Sanitize file content by removing potentially sensitive information
        """
        # Patterns for sensitive data
        patterns = {
            "aws_key": r'(?:ACCESS|SECRET)_KEY(?:_ID)?[\s]*=[\s]*[\'"][0-9a-zA-Z/+]{20,}[\'"]',
            "password": r'(?:password|passwd|pwd)[\s]*=[\s]*[\'"][^\'"]{3,}[\'"]',
            "connection_string": r'(?:mongodb|mysql|postgresql|jdbc):.*:.*@.*',
            "api_key": r'api[-_]?key[\s]*=[\s]*[\'"][0-9a-zA-Z]{16,}[\'"]',
            "private_key": r'-----BEGIN (?:RSA )?PRIVATE KEY-----[^-]*-----END (?:RSA )?PRIVATE KEY-----',
            "token": r'(?:auth|jwt|token|access|refresh)[\s]*:[\s]*[\'"][0-9a-zA-Z._-]{8,}[\'"]'
        }
        
        sanitized = content
        
        for pattern_name, pattern in patterns.items():
            sanitized = re.sub(
                pattern, 
                f"[REDACTED {pattern_name.upper()}]", 
                sanitized, 
                flags=re.IGNORECASE
            )
            
        return sanitized
```

## 7. Secure Agent Execution

### Agent Sandbox

```python
# backend/services/agent_sandbox.py
import asyncio
import resource
import os
import subprocess
import tempfile
import uuid
import json
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger("agent_sandbox")

class AgentSandbox:
    """
    A sandbox for safely executing agent code with resource limitations
    """
    
    def __init__(
        self,
        max_memory_mb: int = 500,
        max_cpu_time_seconds: int = 60,
        max_processes: int = 10,
        allow_network: bool = False,
    ):
        self.max_memory_mb = max_memory_mb
        self.max_cpu_time_seconds = max_cpu_time_seconds
        self.max_processes = max_processes
        self.allow_network = allow_network
        
    async def run_agent(
        self, 
        agent_module: str, 
        input_data: Dict[str, Any],
        timeout: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Run an agent in a sandboxed environment with resource limits
        """
        # Create a unique ID for this run
        run_id = str(uuid.uuid4())
        
        # Create temporary files for input and output
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as input_file, \
             tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as output_file:
            
            input_path = input_file.name
            output_path = output_file.name
            
            # Write input data to file
            json.dump(input_data, input_file)
            input_file.flush()
            
        try:
            # Prepare the command to run the agent in a subprocess
            cmd = [
                "python", "-c",
                f"""
import sys
import json
import resource
from importlib import import_module

# Set resource limits
resource.setrlimit(resource.RLIMIT_AS, ({self.max_memory_mb * 1024 * 1024}, {self.max_memory_mb * 1024 * 1024}))
resource.setrlimit(resource.RLIMIT_CPU, ({self.max_cpu_time_seconds}, {self.max_cpu_time_seconds}))
resource.setrlimit(resource.RLIMIT_NPROC, ({self.max_processes}, {self.max_processes}))

# Import the agent module
try:
    module_path = "{agent_module}"
    module_parts = module_path.split('.')
    agent_name = module_parts[-1].title().replace('_', '') + 'Agent'
    
    # Import the module
    module = import_module(module_path)
    agent_class = getattr(module, agent_name)
    
    # Load input data
    with open("{input_path}", "r") as f:
        input_data = json.load(f)
    
    # Initialize and run the agent
    agent = agent_class(module_parts[-1])
    result = agent.run(input_data)
    
    # Save the result
    with open("{output_path}", "w") as f:
        json.dump(result, f)
    
    sys.exit(0)
except Exception as e:
    with open("{output_path}", "w") as f:
        json.dump({{"error": str(e), "message": "Agent execution failed"}}, f)
    sys.exit(1)
                """
            ]
            
            # Network restrictions (if not allowed)
            env = os.environ.copy()
            if not self.allow_network:
                # This is a simplified approach; in production, you'd use 
                # containerization or more robust network blocking
                env["PYTHONNOUSERSITE"] = "1"
                env["http_proxy"] = "http://localhost:1"  # Invalid proxy to block network
                env["https_proxy"] = "http://localhost:1"
            
            # Execute the subprocess with a timeout
            timeout_secs = timeout or self.max_cpu_time_seconds + 10
            
            logger.info(f"Running agent {agent_module} in sandbox (run_id: {run_id})")
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                env=env,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(), timeout=timeout_secs
                )
                
                # Log the output for debugging
                if stdout:
                    logger.debug(f"Agent stdout (run_id: {run_id}): {stdout.decode()}")
                if stderr:
                    logger.warning(f"Agent stderr (run_id: {run_id}): {stderr.decode()}")
                
                # Read the result
                with open(output_path, 'r') as f:
                    result = json.load(f)
                    
                return result
                
            except asyncio.TimeoutError:
                # Kill the process if it times out
                try:
                    process.kill()
                except:
                    pass
                
                logger.error(f"Agent execution timed out after {timeout_secs}s (run_id: {run_id})")
                return {
                    "error": f"Execution timed out after {timeout_secs} seconds",
                    "message": "Agent execution failed due to timeout"
                }
                
        except Exception as e:
            logger.error(f"Error running agent in sandbox: {str(e)}", exc_info=True)
            return {
                "error": str(e),
                "message": "Failed to execute agent in sandbox"
            }
            
        finally:
            # Clean up temporary files
            try:
                os.unlink(input_path)
                os.unlink(output_path)
            except:
                pass
```

## 8. Security Best Practices for the Frontend

### React Context for Authentication

```tsx
// frontend/contexts/AuthContext.tsx
import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

// Types
interface User {
  id: number;
  username: string;
  email: string;
  isAdmin: boolean;
  permissions: string[];
}

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  refreshToken: () => Promise<boolean>;
  hasPermission: (permission: string) => boolean;
}

interface AuthProviderProps {
  children: ReactNode;
}

interface TokenData {
  sub: string;
  exp: number;
  scopes: string[];
}

// Create context
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Provider component
export const AuthProvider = ({ children }: AuthProviderProps) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Check token validity on mount
  useEffect(() => {
    const initAuth = async () => {
      const token = localStorage.getItem('access_token');
      
      if (token) {
        try {
          // Check if token is expired
          const decodedToken = jwtDecode<TokenData>(token);
          const currentTime = Date.now() / 1000;
          
          if (decodedToken.exp < currentTime) {
            // Token expired, try to refresh
            const refreshed = await refreshToken();
            if (!refreshed) {
              // Refresh failed, clear storage
              localStorage.removeItem('access_token');
              localStorage.removeItem('refresh_token');
              setIsAuthenticated(false);
              setUser(null);
            }
          } else {
            // Token valid, set axios default header
            axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
            
            // Fetch user data
            const response = await axios.get('/api/auth/me');
            setUser(response.data);
            setIsAuthenticated(true);
          }
        } catch (error) {
          console.error('Error initializing auth:', error);
          // Clear invalid tokens
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          setIsAuthenticated(false);
          setUser(null);
        }
      }
      
      setIsLoading(false);
    };
    
    initAuth();
  }, []);

  // Login function
  const login = async (username: string, password: string) => {
    setIsLoading(true);
    
    try {
      // Get tokens
      const response = await axios.post('/api/auth/token', {
        username,
        password
      });
      
      const { access_token, refresh_token } = response.data;
      
      // Store tokens
      localStorage.setItem('access_token', access_token);
      localStorage.setItem('refresh_token', refresh_token);
      
      // Set default auth header
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      
      // Get user data
      const userResponse = await axios.get('/api/auth/me');
      setUser(userResponse.data);
      setIsAuthenticated(true);
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  // Logout function
  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    delete axios.defaults.headers.common['Authorization'];
    setUser(null);
    setIsAuthenticated(false);
  };

  // Refresh token function
  const refreshToken = async (): Promise<boolean> => {
    const storedRefreshToken = localStorage.getItem('refresh_token');
    
    if (!storedRefreshToken) {
      return false;
    }
    
    try {
      const response = await axios.post('/api/auth/refresh', {
        refresh_token: storedRefreshToken
      });
      
      const { access_token, refresh_token } = response.data;
      
      // Update tokens
      localStorage.setItem('access_token', access_token);
      localStorage.setItem('refresh_token', refresh_token);
      
      // Update auth header
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      
      // Get updated user data
      const userResponse = await axios.get('/api/auth/me');
      setUser(userResponse.data);
      setIsAuthenticated(true);
      
      return true;
    } catch (error) {
      console.error('Token refresh failed:', error);
      return false;
    }
  };

  // Permission check helper
  const hasPermission = (permission: string): boolean => {
    if (!user) return false;
    
    // Admin has all permissions
    if (user.isAdmin) return true;
    
    return user.permissions.includes(permission);
  };

  // Axios response interceptor for automatic token refresh
  useEffect(() => {
    const interceptor = axios.interceptors.response.use(
      (response) => response,
      async (error) => {
        const originalRequest = error.config;
        
        // If error is 401 and not already retrying
        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;
          
          try {
            // Try to refresh token
            const refreshed = await refreshToken();
            
            if (refreshed) {
              // Retry the original request
              return axios(originalRequest);
            } else {
              // Refresh failed, logout
              logout();
              return Promise.reject(error);
            }
          } catch (refreshError) {
            logout();
            return Promise.reject(refreshError);
          }
        }
        
        return Promise.reject(error);
      }
    );
    
    // Clean up interceptor on unmount
    return () => {
      axios.interceptors.response.eject(interceptor);
    };
  }, []);

  return (
    <AuthContext.Provider value={{
      user,
      isLoading,
      isAuthenticated,
      login,
      logout,
      refreshToken,
      hasPermission
    }}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook for consuming the auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  
  return context;
};
```

### Protected Route Component

```tsx
// frontend/components/ProtectedRoute.tsx
import { useEffect } from 'react';
import { useRouter } from 'next/router';
import { useAuth } from '../contexts/AuthContext';

interface ProtectedRouteProps {
  children: React.ReactNode;
  requiredPermission?: string;
}

const ProtectedRoute = ({ children, requiredPermission }: ProtectedRouteProps) => {
  const { isAuthenticated, isLoading, hasPermission } = useAuth();
  const router = useRouter();

  useEffect(() => {
    // Skip redirect during initial load
    if (isLoading) return;
    
    // If not authenticated, redirect to login
    if (!isAuthenticated) {
      router.push(`/login?redirect=${encodeURIComponent(router.asPath)}`);
      return;
    }
    
    // If permission is required but not granted, redirect to forbidden page
    if (requiredPermission && !hasPermission(requiredPermission)) {
      router.push('/forbidden');
    }
  }, [isAuthenticated, isLoading, router, requiredPermission, hasPermission]);

  // Show loading or nothing while checking auth
  if (isLoading) {
    return <div className="loading">Loading...</div>;
  }
  
  // If authentication check is complete and user is authenticated
  // (and has required permission if specified), render children
  if (isAuthenticated && (!requiredPermission || hasPermission(requiredPermission))) {
    return <>{children}</>;
  }
  
  // Don't render anything during redirect
  return null;
};

export default ProtectedRoute;
```

## 9. Deployment Security

### Docker Security Configuration

```dockerfile
# Dockerfile with security best practices
FROM python:3.9-slim AS build

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.9-slim AS runtime

# Create non-root user
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser

# Copy installed dependencies from build stage
COPY --from=build /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=build /usr/local/bin /usr/local/bin

WORKDIR /app

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p memory/sessions projects && \
    chown -R appuser:appgroup /app

# Set permissions
RUN chmod -R 755 /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/api/health || exit 1

# Run the application
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 10. Testing Strategy

### Security Testing

```python
# tests/security/test_auth.py
import pytest
from fastapi.testclient import TestClient
import jwt
from datetime import datetime, timedelta

from backend.main import app
from backend.core.config import settings

client = TestClient(app)

def test_auth_flow():
    # Test user registration
    signup_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "securePassword123!"
    }
    signup_response = client.post("/auth/signup", json=signup_data)
    assert signup_response.status_code == 200
    
    # Test login with created user
    login_data = {
        "username": "testuser",
        "password": "securePassword123!"
    }
    token_response = client.post("/auth/token", data=login_data)
    assert token_response.status_code == 200
    assert "access_token" in token_response.json()
    assert "refresh_token" in token_response.json()
    
    # Test accessing protected endpoint with token
    access_token = token_response.json()["access_token"]
    me_response = client.get(
        "/auth/me", 
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert me_response.status_code == 200
    assert me_response.json()["username"] == "testuser"

def test_invalid_credentials():
    login_data = {
        "username": "nonexistent",
        "password": "wrongpassword"
    }
    response = client.post("/auth/token", data=login_data)
    assert response.status_code == 401

def test_unauthorized_access():
    response = client.get("/auth/me")
    assert response.status_code == 401

def test_expired_token():
    # Create an expired token
    expire = datetime.utcnow() - timedelta(minutes=30)
    payload = {
        "sub": "testuser",
        "exp": expire
    }
    expired_token = jwt.encode(
        payload, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    
    # Try to access protected endpoint with expired token
    response = client.get(
        "/auth/me", 
        headers={"Authorization": f"Bearer {expired_token}"}
    )
    assert response.status_code == 401

def test_token_refresh():
    # First login to get tokens
    login_data = {
        "username": "testuser",
        "password": "securePassword123!"
    }
    token_response = client.post("/auth/token", data=login_data)
    refresh_token = token_response.json()["refresh_token"]
    
    # Refresh token
    refresh_data = {"refresh_token": refresh_token}
    refresh_response = client.post("/auth/refresh", json=refresh_data)
    assert refresh_response.status_code == 200
    assert "access_token" in refresh_response.json()
    assert "refresh_token" in refresh_response.json()
    
    # Ensure new access token works
    new_access_token = refresh_response.json()["access_token"]
    me_response = client.get(
        "/auth/me", 
        headers={"Authorization": f"Bearer {new_access_token}"}
    )
    assert me_response.status_code == 200

def test_invalid_refresh_token():
    # Try with a fake refresh token
    refresh_data = {"refresh_token": "invalid-token"}
    response = client.post("/auth/refresh", json=refresh_data)
    assert response.status_code == 401
```

### Input Validation Testing

```python
# tests/security/test_input_validation.py
import pytest
from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)

def test_agent_input_validation():
    # Test with valid input
    valid_input = {
        "prompt": "Build a blog",
        "context": {"project_type": "blog"}
    }
    
    response = client.post("/api/agents/run/planner", json=valid_input)
    assert response.status_code == 200
    
    # Test with empty prompt
    invalid_input = {
        "prompt": "",
        "context": {"project_type": "blog"}
    }
    
    response = client.post("/api/agents/run/planner", json=invalid_input)
    assert response.status_code == 422  # Validation error
    
    # Test with potentially dangerous context
    dangerous_input = {
        "prompt": "Build a blog",
        "context": {"exec_command": "rm -rf /"}
    }
    
    response = client.post("/api/agents/run/planner", json=dangerous_input)
    assert response.status_code == 422  # Validation error

def test_chain_config_validation():
    # Test with valid chain config
    valid_config = {
        "name": "Test Chain",
        "type": "sequential",
        "agents": ["planner", "frontend_builder"]
    }
    
    response = client.post("/api/chains/validate", json=valid_config)
    assert response.status_code == 200
    
    # Test with invalid chain type
    invalid_type = {
        "name": "Test Chain",
        "type": "invalid_type",
        "agents": ["planner", "frontend_builder"]
    }
    
    response = client.post("/api/chains/validate", json=invalid_type)
    assert response.status_code == 422  # Validation error
    
    # Test with empty agents list
    empty_agents = {
        "name": "Test Chain",
        "type": "sequential",
        "agents": []
    }
    
    response = client.post("/api/chains/validate", json=empty_agents)
    assert response.status_code == 422  # Validation error
    
    # Test with potentially dangerous agent name
    dangerous_agents = {
        "name": "Test Chain",
        "type": "sequential",
        "agents": ["planner", "exec_commands"]
    }
    
    response = client.post("/api/chains/validate", json=dangerous_agents)
    assert response.status_code == 422  # Validation error
```

## 11. Monitoring and Logging

### Secure Logging Setup

```python
# backend/core/logging.py
import logging
import logging.handlers
import os
import json
from datetime import datetime
from typing import Any, Dict

class SensitiveDataFilter(logging.Filter):
    """Filter for removing sensitive information from logs"""
    
    def __init__(self, patterns=None):
        super().__init__()
        self.patterns = patterns or [
            "password", "token", "key", "secret", "auth", 
            "credential", "api_key", "apikey", "private"
        ]
    
    def filter(self, record):
        if record.getMessage():
            # Check if any sensitive data pattern is in the message
            message = record.getMessage().lower()
            for pattern in self.patterns:
                if pattern in message:
                    # Redact sensitive data from the message
                    parts = record.getMessage().split(":")
                    if len(parts) > 1:
                        record.msg = parts[0] + ": [REDACTED]"
                    else:
                        # If no colon, just indicate it contains sensitive data
                        record.msg = "[Contains sensitive data]"
        return True

class JSONFormatter(logging.Formatter):
    """Formatter that outputs JSON strings after gathering all available log record info"""
    
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add exception info if available
        if record.exc_info:
            log_data["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "traceback": self.formatException(record.exc_info)
            }
        
        # Add extra fields
        for key, value in record.__dict__.items():
            if key not in {
                "args", "asctime", "created", "exc_info", "exc_text", "filename",
                "funcName", "id", "levelname", "levelno", "lineno", "module",
                "msecs", "message", "msg", "name", "pathname", "process",
                "processName", "relativeCreated", "stack_info", "thread", "threadName"
            }:
                log_data[key] = value
        
        return json.dumps(log_data)

def setup_logging():
    """Configure logging for the application"""
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    # Set up root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # Clear existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Create a sensitive data filter
    sensitive_filter = SensitiveDataFilter()
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(console_formatter)
    console_handler.addFilter(sensitive_filter)
    
    # Create file handler for general logs
    general_log_file = os.path.join(log_dir, "app.log")
    file_handler = logging.handlers.RotatingFileHandler(
        general_log_file, maxBytes=10485760, backupCount=10
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(JSONFormatter())
    file_handler.addFilter(sensitive_filter)
    
    # Create file handler for error logs
    error_log_file = os.path.join(log_dir, "error.log")
    error_handler = logging.handlers.RotatingFileHandler(
        error_log_file, maxBytes=10485760, backupCount=10
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(JSONFormatter())
    error_handler.addFilter(sensitive_filter)
    
    # Add handlers to root logger
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(error_handler)
    
    # Set up security logger
    security_logger = logging.getLogger("security")
    security_log_file = os.path.join(log_dir, "security.log")
    security_handler = logging.handlers.RotatingFileHandler(
        security_log_file, maxBytes=10485760, backupCount=10
    )
    security_handler.setLevel(logging.INFO)
    security_handler.setFormatter(JSONFormatter())
    security_logger.addHandler(security_handler)
    
    # Set SQLAlchemy logging to warning level
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    
    # Set uvicorn access logs to warning level (reduce noise)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    
    return root_logger
```