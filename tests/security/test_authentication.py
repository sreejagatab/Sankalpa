"""
Security tests for authentication
"""

import pytest
import os
import sys
import time
import json
import requests
import jwt
from datetime import datetime, timedelta

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Skip these tests if the security tests are not enabled
pytestmark = pytest.mark.skipif(
    not os.environ.get("RUN_SECURITY_TESTS"),
    reason="Security tests are only run when RUN_SECURITY_TESTS environment variable is set"
)

@pytest.fixture(scope="module")
def api_url():
    """Get the API URL"""
    return "http://localhost:8000"

@pytest.fixture(scope="module")
def app_server():
    """Start the application server for testing"""
    import subprocess
    import time
    
    # Start the backend server
    backend_process = subprocess.Popen(
        ["python", "run_sankalpa.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for the server to start
    time.sleep(5)
    
    yield
    
    # Clean up
    backend_process.terminate()
    backend_process.wait()

@pytest.fixture
def valid_token():
    """Generate a valid JWT token"""
    # This should match the secret key used in the application
    secret_key = "your-secret-key"  # Replace with the actual secret key
    
    # Create a token payload
    payload = {
        "sub": "test_user",
        "name": "Test User",
        "scopes": ["user"],
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    
    # Encode the token
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    
    return token

@pytest.fixture
def expired_token():
    """Generate an expired JWT token"""
    # This should match the secret key used in the application
    secret_key = "your-secret-key"  # Replace with the actual secret key
    
    # Create a token payload with an expiration in the past
    payload = {
        "sub": "test_user",
        "name": "Test User",
        "scopes": ["user"],
        "exp": datetime.utcnow() - timedelta(hours=1)
    }
    
    # Encode the token
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    
    return token

def test_protected_endpoint_without_token(api_url, app_server):
    """Test accessing a protected endpoint without a token"""
    # Try to access a protected endpoint
    response = requests.get(f"{api_url}/api/me")
    
    # Should return 401 Unauthorized
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data

def test_protected_endpoint_with_valid_token(api_url, app_server, valid_token):
    """Test accessing a protected endpoint with a valid token"""
    # Set up the authorization header
    headers = {"Authorization": f"Bearer {valid_token}"}
    
    # Try to access a protected endpoint
    response = requests.get(f"{api_url}/api/me", headers=headers)
    
    # Should return 200 OK
    assert response.status_code == 200
    data = response.json()
    assert "sub" in data
    assert data["sub"] == "test_user"

def test_protected_endpoint_with_expired_token(api_url, app_server, expired_token):
    """Test accessing a protected endpoint with an expired token"""
    # Set up the authorization header
    headers = {"Authorization": f"Bearer {expired_token}"}
    
    # Try to access a protected endpoint
    response = requests.get(f"{api_url}/api/me", headers=headers)
    
    # Should return 401 Unauthorized
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data

def test_protected_endpoint_with_invalid_token(api_url, app_server):
    """Test accessing a protected endpoint with an invalid token"""
    # Set up the authorization header with an invalid token
    headers = {"Authorization": "Bearer invalid.token.here"}
    
    # Try to access a protected endpoint
    response = requests.get(f"{api_url}/api/me", headers=headers)
    
    # Should return 401 Unauthorized
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data

def test_token_refresh(api_url, app_server, valid_token):
    """Test refreshing a token"""
    # Set up the authorization header
    headers = {"Authorization": f"Bearer {valid_token}"}
    
    # Try to refresh the token
    response = requests.post(f"{api_url}/api/auth/refresh", headers=headers)
    
    # Should return 200 OK with a new token
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"

def test_logout(api_url, app_server, valid_token):
    """Test logging out"""
    # Set up the authorization header
    headers = {"Authorization": f"Bearer {valid_token}"}
    
    # Try to log out
    response = requests.post(f"{api_url}/api/auth/logout", headers=headers)
    
    # Should return 200 OK
    assert response.status_code == 200
    
    # Try to use the token again (should be invalidated)
    response = requests.get(f"{api_url}/api/me", headers=headers)
    
    # Should return 401 Unauthorized
    assert response.status_code == 401
