
import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from typing import List, Optional
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field

from core import get_logger
from core.security import (
    get_current_user, create_access_token, create_refresh_token,
    verify_password, get_password_hash, decode_token
)

# Initialize router
router = APIRouter()
logger = get_logger("api.users")

# Pydantic models
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class User(UserBase):
    id: str
    is_active: bool
    scopes: List[str]

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int

class RefreshRequest(BaseModel):
    refresh_token: str

# Routes
@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate):
    """Register a new user
    
    In a real implementation, this would create a new user in the database
    """
    # Simple demonstration of password hashing
    hashed_password = get_password_hash(user_data.password)
    
    # Mock user creation - in a real implementation, this would save to a database
    new_user = {
        "id": "123",  # This would be a database-generated ID
        "email": user_data.email,
        "username": user_data.username,
        "full_name": user_data.full_name,
        "is_active": True,
        "scopes": ["user"]
    }
    
    logger.info(f"User registered: {user_data.username}")
    return new_user

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login to get access token
    
    In a real implementation, this would validate credentials against a database
    """
    # Mock authentication - in a real implementation, this would query a database
    user = {
        "id": "123",
        "username": "demo",
        "password_hash": get_password_hash("password"),  # For demonstration only
        "scopes": ["user"]
    }
    
    # Verify password
    if form_data.username != user["username"] or not verify_password(form_data.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create tokens
    access_token = create_access_token(
        subject=user["id"],
        scopes=user["scopes"]
    )
    
    refresh_token = create_refresh_token(subject=user["id"])
    
    logger.info(f"User logged in: {form_data.username}")
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": 3600  # 1 hour
    }

@router.post("/refresh", response_model=Token)
async def refresh_access_token(refresh_request: RefreshRequest = Body(...)):
    """Refresh an access token using a refresh token"""
    try:
        # Decode the refresh token
        payload = decode_token(refresh_request.refresh_token)
        
        # Check if it's a refresh token
        if payload.get("token_type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Get the user ID from the token
        user_id = payload.get("sub")
        
        # In a real implementation, you would validate the refresh token against a database
        # and fetch the user's current scopes
        
        # Mock user data
        user = {
            "id": user_id,
            "scopes": ["user"]
        }
        
        # Create a new access token
        access_token = create_access_token(
            subject=user["id"],
            scopes=user["scopes"]
        )
        
        # Create a new refresh token
        refresh_token = create_refresh_token(subject=user["id"])
        
        logger.info(f"Token refreshed for user: {user_id}")
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": 3600  # 1 hour
        }
    except Exception as e:
        logger.warning(f"Token refresh failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.get("/me", response_model=User)
async def read_users_me(current_user = Depends(get_current_user)):
    """Get current user information"""
    # In a real implementation, you would fetch complete user data from a database
    return {
        "id": current_user["id"],
        "email": "user@example.com",  # This would come from the database
        "username": "demo",  # This would come from the database
        "full_name": "Demo User",  # This would come from the database
        "is_active": True,
        "scopes": current_user["scopes"]
    }