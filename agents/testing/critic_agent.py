
import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from agents.base import BaseAgent

class CriticAgent(BaseAgent):
    def run(self, input_data):
        suggestions = []

        if 'print(' in str(input_data):
            suggestions.append("Consider using logging instead of print statements for better maintainability.")
        if 'test_' not in str(input_data):
            suggestions.append("Add test functions following the 'test_' naming convention for better test coverage.")

        return {
            "message": "Code review complete.",
            "suggestions": suggestions if suggestions else ["Code looks clean."]
        }
