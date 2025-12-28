
import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from agents.base import BaseAgent

class ProjectArchitectAgent(BaseAgent):
    def run(self, input_data):
        project_name = input_data.get("project", "sankalpa_project")
        structure = {
            f"projects/{project_name}/backend/__init__.py": "",
            f"projects/{project_name}/frontend/pages/index.tsx": "",
            f"projects/{project_name}/tests/__init__.py": ""
        }
        return {
            "message": f"Project structure initialized for '{project_name}'",
            "files": structure
        }