
import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from agents.base import BaseAgent
from memory.memory_manager import MemoryManager

class CopilotAgent(BaseAgent):
    def run(self, input_data):
        prompt = input_data.get("prompt", "")
        memory = MemoryManager()
        last_outputs = memory.get_all()

        recent_agents = list(last_outputs.keys())[-3:]
        suggestion = "Based on your recent activity with: " + ", ".join(recent_agents)
        suggestion += f"\nTo proceed from '{prompt}', you might consider running: test_suite or deploy_executor."

        return {
            "message": "Copilot contextual suggestion generated.",
            "output": suggestion
        }