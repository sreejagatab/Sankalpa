
import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from agents.base import BaseAgent

class IntegrationTestAgent(BaseAgent):
    def run(self, input_data):
        files = {
            "tests/integration/test_end_to_end.py": """
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_signup_and_login():
    signup = client.post("/auth/signup", json={"username": "flow", "password": "chain"})
    assert signup.status_code == 200

    login = client.post("/auth/login", json={"username": "flow", "password": "chain"})
    assert login.status_code == 200
"""
        }

        return {
            "message": "Integration test suite generated.",
            "files": files
        }
