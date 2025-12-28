
import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from agents.base import BaseAgent

class PlannerAgent(BaseAgent):
    def run(self, input_data):
        prompt = input_data.get("prompt", "")

        # Example logic based on keywords
        steps = []
        if "frontend" in prompt:
            steps.append("frontend_builder")
        if "backend" in prompt:
            steps.append("backend_builder")
        if "auth" in prompt:
            steps.append("auth_builder")
        if "database" in prompt or "schema" in prompt:
            steps.append("db_schema")
        if "markdown" in prompt:
            steps.append("markdown_editor")
        if "test" in prompt:
            steps.extend(["test_suite", "integration_test"])
        if "secure" in prompt:
            steps.append("security_scanner")

        return {
            "message": "Plan generated from prompt.",
            "chain": steps
        }
