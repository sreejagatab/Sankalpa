
import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from agents.base import BaseAgent

class AuthBuilderAgent(BaseAgent):
    def run(self, input_data):
        files = {
            "backend/services/auth.py": """
import hashlib
from fastapi import HTTPException

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    return hash_password(password) == hashed

def authenticate_user(db, username, password):
    user = db.get(username)
    if not user or not verify_password(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user
"""
        }

        return {
            "message": "Auth service module generated.",
            "files": files
        }