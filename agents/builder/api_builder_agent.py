
import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from agents.base import BaseAgent

class ApiBuilderAgent(BaseAgent):
    def run(self, input_data):
        files = {
            "backend/routes/user.py": """
from fastapi import APIRouter

router = APIRouter()

@router.get("/users")
def list_users():
    return [{"username": "test_user"}]

@router.post("/users")
def create_user(user: dict):
    return {"message": "User created", "user": user}
"""
        }
        return {
            "message": "User API endpoints scaffolded.",
            "files": files
        }
