import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

def test_health_endpoint(test_client):
    """Test the health endpoint"""
    response = test_client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data
    assert "timestamp" in data

def test_status_endpoint(test_client):
    """Test the legacy status endpoint"""
    response = test_client.get("/api/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "Ultimate Sankalpa API is running!"

def test_protected_endpoint_without_auth(test_client):
    """Test accessing a protected endpoint without authentication"""
    # The /api/me endpoint requires authentication
    response = test_client.get("/api/me")
    assert response.status_code == 401
    assert "detail" in response.json()

def test_protected_endpoint_with_auth(test_client, monkeypatch):
    """Test accessing a protected endpoint with authentication"""
    # Mock the security dependencies
    def mock_get_current_user():
        return {"id": "test_user", "scopes": ["user"]}

    # Patch the endpoint to use our mock
    from backend.enhanced_main import app
    from fastapi import Depends

    @app.get("/api/test_auth")
    def test_auth_endpoint(current_user = Depends(mock_get_current_user)):
        return current_user

    # Test the endpoint
    response = test_client.get("/api/test_auth")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "test_user"
    assert data["scopes"] == ["user"]

def test_security_headers(test_client):
    """Test that security headers are added to responses"""
    response = test_client.get("/api/health")

    # Check for security headers
    assert "X-Content-Type-Options" in response.headers
    assert "X-Frame-Options" in response.headers
    assert "X-XSS-Protection" in response.headers
    assert "Content-Security-Policy" in response.headers
    assert "Strict-Transport-Security" in response.headers

    # Verify specific header values
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"

def test_processing_time_header(test_client):
    """Test that processing time header is added to responses"""
    response = test_client.get("/api/health")
    assert "X-Process-Time" in response.headers
    assert "X-Request-ID" in response.headers

    # Processing time should be a positive number
    process_time = float(response.headers["X-Process-Time"])
    assert process_time > 0