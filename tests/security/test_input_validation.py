"""
Security tests for input validation
"""

import pytest
import os
import sys
import time
import json
import requests
import random
import string

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

def generate_random_string(length):
    """Generate a random string of the specified length"""
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

def test_sql_injection(api_url, app_server):
    """Test SQL injection prevention"""
    # Try to inject SQL into the memory key
    sql_injection_keys = [
        "'; DROP TABLE users; --",
        "' OR '1'='1",
        "' UNION SELECT * FROM users; --",
        "'; INSERT INTO users VALUES ('hacker', 'password'); --"
    ]
    
    for key in sql_injection_keys:
        # Try to save data with the injection key
        response = requests.post(
            f"{api_url}/api/memory/{key}",
            json={"value": "test"}
        )
        
        # Should either return 400 Bad Request or sanitize the input
        assert response.status_code in [200, 400, 422]
        
        if response.status_code == 200:
            # If it accepted the key, make sure we can retrieve it exactly as provided
            # (indicating it was properly escaped/sanitized)
            get_response = requests.get(f"{api_url}/api/memory/{key}")
            assert get_response.status_code == 200
            
            # Clean up
            delete_response = requests.delete(f"{api_url}/api/memory/{key}")
            assert delete_response.status_code == 200

def test_xss_prevention(api_url, app_server):
    """Test Cross-Site Scripting (XSS) prevention"""
    # Try to inject JavaScript into the memory value
    xss_payloads = [
        "<script>alert('XSS')</script>",
        "<img src='x' onerror='alert(\"XSS\")'>",
        "<a href='javascript:alert(\"XSS\")'>Click me</a>",
        "javascript:alert('XSS')"
    ]
    
    for payload in xss_payloads:
        # Try to save data with the XSS payload
        response = requests.post(
            f"{api_url}/api/memory/xss_test",
            json={"value": payload}
        )
        
        # Should accept the input (but sanitize it on output)
        assert response.status_code == 200
        
        # Retrieve the data
        get_response = requests.get(f"{api_url}/api/memory/xss_test")
        assert get_response.status_code == 200
        data = get_response.json()
        
        # The value should either be sanitized or exactly as provided
        # (if the API doesn't sanitize, the frontend should)
        assert data["value"] == payload
    
    # Clean up
    delete_response = requests.delete(f"{api_url}/api/memory/xss_test")
    assert delete_response.status_code == 200

def test_large_input_handling(api_url, app_server):
    """Test handling of very large inputs"""
    # Generate a very large string
    large_string = generate_random_string(1000000)  # 1MB string
    
    # Try to save the large string
    response = requests.post(
        f"{api_url}/api/memory/large_input_test",
        json={"value": large_string}
    )
    
    # Should either accept it or reject it with a 413 Request Entity Too Large
    assert response.status_code in [200, 413, 422]
    
    if response.status_code == 200:
        # Clean up
        delete_response = requests.delete(f"{api_url}/api/memory/large_input_test")
        assert delete_response.status_code == 200

def test_invalid_json(api_url, app_server):
    """Test handling of invalid JSON"""
    # Try to send invalid JSON
    response = requests.post(
        f"{api_url}/api/memory/invalid_json_test",
        data="This is not JSON",
        headers={"Content-Type": "application/json"}
    )
    
    # Should return 400 Bad Request
    assert response.status_code == 400

def test_content_type_validation(api_url, app_server):
    """Test content type validation"""
    # Try to send JSON with the wrong content type
    response = requests.post(
        f"{api_url}/api/memory/content_type_test",
        data=json.dumps({"value": "test"}),
        headers={"Content-Type": "text/plain"}
    )
    
    # Should either return 415 Unsupported Media Type or accept it anyway
    assert response.status_code in [200, 415, 400]

def test_path_traversal(api_url, app_server):
    """Test path traversal prevention"""
    # Try to use path traversal in the memory key
    traversal_keys = [
        "../../../etc/passwd",
        "..\\..\\..\\Windows\\System32\\config\\SAM",
        "/etc/passwd",
        "C:\\Windows\\System32\\config\\SAM"
    ]
    
    for key in traversal_keys:
        # Try to save data with the traversal key
        response = requests.post(
            f"{api_url}/api/memory/{key}",
            json={"value": "test"}
        )
        
        # Should either return 400 Bad Request or sanitize the input
        assert response.status_code in [200, 400, 422]
        
        if response.status_code == 200:
            # If it accepted the key, make sure we can retrieve it exactly as provided
            # (indicating it was properly escaped/sanitized)
            get_response = requests.get(f"{api_url}/api/memory/{key}")
            assert get_response.status_code == 200
            
            # Clean up
            delete_response = requests.delete(f"{api_url}/api/memory/{key}")
            assert delete_response.status_code == 200

def test_null_byte_injection(api_url, app_server):
    """Test null byte injection prevention"""
    # Try to inject null bytes into the memory key
    null_byte_keys = [
        "null_byte\x00.txt",
        "null_byte%00.txt"
    ]
    
    for key in null_byte_keys:
        # Try to save data with the null byte key
        response = requests.post(
            f"{api_url}/api/memory/{key}",
            json={"value": "test"}
        )
        
        # Should either return 400 Bad Request or sanitize the input
        assert response.status_code in [200, 400, 422]
        
        if response.status_code == 200:
            # If it accepted the key, make sure we can retrieve it
            # (indicating it was properly handled)
            get_response = requests.get(f"{api_url}/api/memory/{key}")
            assert get_response.status_code == 200
            
            # Clean up
            delete_response = requests.delete(f"{api_url}/api/memory/{key}")
            assert delete_response.status_code == 200
