
import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
import os
import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, Optional, List, Union

import bcrypt
import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, SecurityScopes

# Direct imports
from .logging import get_logger
from .config import config

logger = get_logger("security")

# Configure password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 setup
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="api/auth/token",
    scopes={
        "user": "Standard user access",
        "admin": "Administrator access",
        "agent": "Agent execution access",
    }
)


class SecurityError(Exception):
    """Base class for security-related exceptions"""
    pass


class InvalidTokenError(SecurityError):
    """Raised when a token is invalid"""
    pass


class PermissionDeniedError(SecurityError):
    """Raised when a user lacks required permissions"""
    pass


class RateLimitExceededError(SecurityError):
    """Raised when a user exceeds rate limits"""
    pass


def get_password_hash(password: str) -> str:
    """Hash a password for storage
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash
    
    Args:
        plain_password: Plain text password
        hashed_password: Hashed password
        
    Returns:
        True if the password matches
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    subject: str, 
    scopes: List[str] = None,
    expires_delta: Optional[timedelta] = None
) -> str:
    """Create a JWT access token
    
    Args:
        subject: Subject of the token (usually user ID)
        scopes: Permission scopes to include in the token
        expires_delta: Optional expiration time override
        
    Returns:
        Encoded JWT token
    """
    if scopes is None:
        scopes = ["user"]
        
    if expires_delta is None:
        expires_delta = timedelta(minutes=config.get("security.token_expire_minutes", 60))
        
    expire = datetime.utcnow() + expires_delta
    
    to_encode = {
        "sub": subject,
        "scopes": scopes,
        "exp": expire,
        "iat": datetime.utcnow(),
        "jti": str(uuid.uuid4())
    }
    
    token = jwt.encode(
        to_encode,
        config.get("security.jwt_secret", os.environ.get("SANKALPA_JWT_SECRET", "")),
        algorithm=config.get("security.jwt_algorithm", "HS256")
    )
    
    logger.debug(f"Created access token for {subject} with scopes {scopes}")
    return token


def create_refresh_token(subject: str) -> str:
    """Create a JWT refresh token
    
    Args:
        subject: Subject of the token (usually user ID)
        
    Returns:
        Encoded JWT refresh token
    """
    refresh_expire = timedelta(days=config.get("security.refresh_token_expire_days", 7))
    
    expire = datetime.utcnow() + refresh_expire
    
    to_encode = {
        "sub": subject,
        "exp": expire,
        "iat": datetime.utcnow(),
        "jti": str(uuid.uuid4()),
        "token_type": "refresh"
    }
    
    token = jwt.encode(
        to_encode,
        config.get("security.jwt_secret", os.environ.get("SANKALPA_JWT_SECRET", "")),
        algorithm=config.get("security.jwt_algorithm", "HS256")
    )
    
    logger.debug(f"Created refresh token for {subject}")
    return token


def decode_token(token: str) -> Dict:
    """Decode a JWT token
    
    Args:
        token: JWT token to decode
        
    Returns:
        Decoded token payload
        
    Raises:
        InvalidTokenError: If the token is invalid
    """
    try:
        payload = jwt.decode(
            token,
            config.get("security.jwt_secret", os.environ.get("SANKALPA_JWT_SECRET", "")),
            algorithms=[config.get("security.jwt_algorithm", "HS256")]
        )
        return payload
    except jwt.PyJWTError as e:
        logger.warning(f"Invalid token: {str(e)}")
        raise InvalidTokenError(f"Invalid token: {str(e)}")


async def get_current_user(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
    """Get the current user from a token
    
    Args:
        security_scopes: Security scopes required for the endpoint
        token: JWT access token
        
    Returns:
        User information extracted from the token
        
    Raises:
        HTTPException: If authentication fails
    """
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
        
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    
    try:
        payload = decode_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
            
        token_scopes = payload.get("scopes", [])
        for scope in security_scopes.scopes:
            if scope not in token_scopes:
                logger.warning(f"User {user_id} lacks required scope: {scope}")
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Not enough permissions. Required: {security_scopes.scope_str}",
                    headers={"WWW-Authenticate": authenticate_value},
                )
        
        # In a real implementation, you would fetch the user from a database here
        # For now, we just return the user ID and scopes
        user_info = {
            "id": user_id,
            "scopes": token_scopes
        }
        
        return user_info
    except InvalidTokenError:
        raise credentials_exception


class RateLimiter:
    """Simple in-memory rate limiter"""
    
    def __init__(self, requests_per_minute: int = 60):
        """Initialize the rate limiter
        
        Args:
            requests_per_minute: Maximum requests allowed per minute
        """
        self.requests_per_minute = requests_per_minute
        self.window_seconds = 60
        self.request_records = {}
        
    async def check_rate_limit(self, request: Request) -> bool:
        """Check if the request exceeds rate limits
        
        Args:
            request: FastAPI request object
            
        Returns:
            True if the request is allowed, False if rate limited
            
        Raises:
            RateLimitExceededError: If the rate limit is exceeded
        """
        now = time.time()
        client_ip = request.client.host
        
        # Clean up old records
        self._clean_old_records(now)
        
        # Initialize record for this IP if not exists
        if client_ip not in self.request_records:
            self.request_records[client_ip] = []
            
        # Count recent requests
        recent_requests = [ts for ts in self.request_records[client_ip] if now - ts < self.window_seconds]
        
        if len(recent_requests) >= self.requests_per_minute:
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            raise RateLimitExceededError(f"Rate limit exceeded: {self.requests_per_minute} requests per minute")
            
        # Add this request to the record
        self.request_records[client_ip].append(now)
        return True
        
    def _clean_old_records(self, now: float) -> None:
        """Clean up old rate limit records
        
        Args:
            now: Current timestamp
        """
        for ip, timestamps in list(self.request_records.items()):
            self.request_records[ip] = [ts for ts in timestamps if now - ts < self.window_seconds]
            
            # Remove empty records
            if not self.request_records[ip]:
                del self.request_records[ip]


class SecurityHeaders:
    """Security headers helper"""
    
    @staticmethod
    def get_secure_headers() -> Dict[str, str]:
        """Get recommended security headers
        
        Returns:
            Dictionary of security headers
        """
        return {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Content-Security-Policy": "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'self'",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Permissions-Policy": "camera=(), microphone=(), geolocation=(), interest-cohort=()"
        }