import sys
import os
import importlib
import json
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from agents.base import BaseAgent
from agents.enhanced.self_replicator_agent import SelfReplicatorAgent

# Create a simple memory manager
class MemoryManager:
    def __init__(self, filename="memory/sessions/test_session.json"):
        self.filename = filename
        self.memory = {}
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        self._load_from_file()

    def save(self, key, value):
        self.memory[key] = value
        with open(self.filename, "w") as f:
            json.dump(self.memory, f, indent=2)
        return True

    def load(self, key):
        return self.memory.get(key, None)

    def get_all(self):
        return self.memory

    def _load_from_file(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    self.memory = json.load(f)
            except Exception:
                self.memory = {}

def main():
    # Create memory manager
    memory = MemoryManager()
    
    # Create self-replicator agent
    agent = SelfReplicatorAgent("self_replicator", memory)
    
    # Create a new calculator agent
    agent_data = {
        "name": "custom_calculator",
        "description": "A simple calculator agent that performs arithmetic operations",
        "category": "utility",
        "logic": '''result = {}

        # Get operation type
        operation = input_data.get("operation", "add")
        num1 = input_data.get("num1", 0)
        num2 = input_data.get("num2", 0)
        
        # Perform the calculation
        if operation == "add":
            result["calculation"] = num1 + num2
        elif operation == "subtract":
            result["calculation"] = num1 - num2
        elif operation == "multiply":
            result["calculation"] = num1 * num2
        elif operation == "divide":
            if num2 == 0:
                return {"error": "Cannot divide by zero", "status": "error"}
            result["calculation"] = num1 / num2
        else:
            return {"error": f"Unknown operation: {operation}", "status": "error"}''',
        "inputs": [
            {"name": "operation", "type": "string"},
            {"name": "num1", "type": "number"},
            {"name": "num2", "type": "number"}
        ],
        "outputs": [
            {"name": "calculation", "type": "number"}
        ]
    }
    
    print("=== Creating Calculator Agent ===")
    result = agent.run(agent_data)
    print(json.dumps(result, indent=2))
    
    # Check if files were created
    if os.path.exists(f"agents/custom/custom_calculator.py"):
        print("\n✅ Agent file created successfully!")
        
        # Try to import and instantiate the new agent
        try:
            sys.path.insert(0, os.path.abspath("agents/custom"))
            from custom_calculator import CustomCalculatorAgent
            
            # Create calculator agent
            calculator = CustomCalculatorAgent("custom_calculator", memory)
            
            # Test the calculator
            print("\n=== Testing Calculator Agent ===")
            for operation in ["add", "subtract", "multiply", "divide"]:
                test_data = {
                    "operation": operation,
                    "num1": 10, 
                    "num2": 2
                }
                
                print(f"\nOperation: {operation.upper()}")
                calc_result = calculator.run(test_data)
                print(json.dumps(calc_result, indent=2))
            
        except Exception as e:
            print(f"Error testing calculator agent: {str(e)}")
    else:
        print("\n❌ Failed to create agent file!")
        
    # Check if catalog was updated
    if os.path.exists("catalog/agent_catalog.json"):
        with open("catalog/agent_catalog.json", "r") as f:
            catalog = json.load(f)
            
        if "custom_calculator" in catalog:
            print("\n✅ Agent added to catalog successfully!")
            print(f"Catalog entry: {json.dumps(catalog['custom_calculator'], indent=2)}")
        else:
            print("\n❌ Agent not found in catalog!")

if __name__ == "__main__":
    main()