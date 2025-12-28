
import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from agents.base import BaseAgent
import json

class MultiAgentMemoryManager(BaseAgent):
    def run(self, input_data):
        session_path = input_data.get("session_file", "memory/sessions/session_log.json")
        try:
            with open(session_path, "r") as f:
                memory = json.load(f)
        except:
            return {"error": "Failed to read memory session."}

        agent_summary = {agent: list(result.keys()) for agent, result in memory.items()}

        return {
            "message": "Multi-agent memory summary generated.",
            "summary": agent_summary
        }
