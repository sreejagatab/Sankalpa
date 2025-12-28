
import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from agents.base import BaseAgent

class TestSuiteAgent(BaseAgent):
    def run(self, input_data):
        files = {
            "tests/test_auth.py": """
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_signup():
    response = client.post("/auth/signup", json={"username": "test", "password": "testpass"})
    assert response.status_code == 200

def test_login():
    response = client.post("/auth/login", json={"username": "test", "password": "testpass"})
    assert response.status_code == 200
""",
            "tests/test_api.py": """
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Sankalpa Backend Running"
"""
        }

        return {
            "message": "Test suite generated.",
            "files": files
        }