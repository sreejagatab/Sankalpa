
import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from agents.base import BaseAgent

class BackendBuilderAgent(BaseAgent):
    def run(self, input_data):
        files = {
            "backend/main.py": """
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Sankalpa Backend Running"}
""",
            "backend/routes/auth.py": """
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.post("/auth/signup")
def signup(user: dict):
    return {"message": "User signed up", "user": user}

@router.post("/auth/login")
def login(user: dict):
    return {"message": "User logged in", "user": user}
""",
            "backend/routes/__init__.py": "",
            "backend/utils/__init__.py": ""
        }

        return {
            "message": "Backend API scaffold generated.",
            "files": files
        }
