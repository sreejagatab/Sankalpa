
import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from agents.loader import load_agent
from memory.memory_manager import MemoryManager

class CliRunnerAgent:
    def run(self, input_data):
        agent_name = input_data.get("agent")
        prompt = input_data.get("prompt", "")

        agent = load_agent(agent_name)
        if not agent:
            return {"error": f"Agent {agent_name} could not be loaded."}

        result = agent.run({"prompt": prompt})
        MemoryManager().save(agent_name, result)
        return {"message": f"{agent_name} run via CLI.", "result": result}