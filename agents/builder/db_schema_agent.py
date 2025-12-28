
import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from agents.base import BaseAgent

class DbSchemaAgent(BaseAgent):
    def run(self, input_data):
        files = {
            "backend/models/user.py": """
from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str
""",
            "backend/models/__init__.py": ""
        }

        return {
            "message": "Database schema generated.",
            "files": files
        }
