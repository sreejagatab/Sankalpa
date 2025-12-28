
import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from agents.loader import load_agent
from memory.memory_manager import MemoryManager
from agents.chain_manager import ChainManager

class ExecutionManager:
    def __init__(self):
        self.memory = MemoryManager()

    def run_chain(self, agent_names, prompt=""):
        chain = [load_agent(name) for name in agent_names if load_agent(name)]
        runner = ChainManager(chain, self.memory)
        return runner.run({"prompt": prompt})

    def run_prompt_with_planner(self, prompt):
        planner = load_agent("orchestration.planner_agent")
        plan = planner.run({"prompt": prompt})
        return self.run_chain(plan.get("chain", []), prompt)