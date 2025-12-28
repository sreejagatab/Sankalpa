#!/usr/bin/env python3
"""
Simple runtime for Sankalpa
"""

import os
import sys
import json
import importlib
from datetime import datetime

# Make sure we can import agents
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Make sure the necessary directories exist
os.makedirs("agents/custom", exist_ok=True)
os.makedirs("memory/sessions", exist_ok=True)

# Set up basic memory management
class MemoryManager:
    def __init__(self, filename="memory/sessions/simple_run.json"):
        self.filename = filename
        self.memory = {}
        self._load_from_file()

    def save(self, key, value):
        self.memory[key] = value
        with open(self.filename, "w") as f:
            json.dump(self.memory, f, indent=2)

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

# Create memory manager
memory = MemoryManager()

# Import agents
from agents.base import BaseAgent
from agents.enhanced.self_replicator_agent import SelfReplicatorAgent
from agents.builder.project_architect_agent import ProjectArchitectAgent
from agents.chain_manager import ChainManager

# Create the self-replicator agent
self_replicator = SelfReplicatorAgent("self_replicator", memory)

print("=" * 80)
print("Welcome to Sankalpa Platform Runner")
print("=" * 80)
print("1. Test Self-Replicator Agent")
print("2. Test Project Architect Agent")
print("3. Test Agent Chain")
print("4. List Memory Contents")
print("5. Exit")
print()

while True:
    choice = input("Enter your choice (1-5): ")
    
    if choice == "1":
        print("\nTesting Self-Replicator Agent")
        agent_name = input("Enter a name for the new agent: ")
        
        # Create a simple agent
        agent_spec = {
            "name": agent_name,
            "description": f"A custom {agent_name} agent",
            "category": "custom",
            "logic": """
                message = input_data.get("message", "Hello!")
                result = {"response": f"You said: {message}"}
                return result
            """,
            "inputs": [
                {"name": "message", "type": "string"}
            ],
            "outputs": [
                {"name": "response", "type": "string"}
            ]
        }
        
        print(f"Creating {agent_name} agent...")
        result = self_replicator.run(agent_spec)
        print(f"Result: {json.dumps(result, indent=2)}")
        
    elif choice == "2":
        print("\nTesting Project Architect Agent")
        project_name = input("Enter a project name: ")
        
        architect = ProjectArchitectAgent("project_architect", memory)
        result = architect.run({"project": project_name})
        print(f"Result: {json.dumps(result, indent=2)}")
        
    elif choice == "3":
        print("\nTesting Agent Chain")
        
        # Create a simple chain
        architect = ProjectArchitectAgent("project_architect", memory)
        
        # Try to load a custom agent if available
        custom_agents = [f[:-3] for f in os.listdir("agents/custom") if f.endswith(".py") and f != "__init__.py"]
        
        if custom_agents:
            print(f"Available custom agents: {', '.join(custom_agents)}")
            agent_name = input("Choose a custom agent to chain with (or press Enter to skip): ")
            
            if agent_name in custom_agents:
                try:
                    module_name = f"agents.custom.{agent_name}"
                    class_name = agent_name.title().replace('_', '') + 'Agent'
                    
                    module = importlib.import_module(module_name)
                    agent_class = getattr(module, class_name)
                    
                    custom_agent = agent_class(agent_name, memory)
                    chain = ChainManager([architect, custom_agent], memory)
                    
                    print(f"Running chain with Project Architect -> {agent_name}")
                    project_name = input("Enter a project name: ")
                    message = input("Enter a message for the custom agent: ")
                    
                    result = chain.run({
                        "project": project_name,
                        "message": message
                    })
                    
                    print(f"Chain result: {json.dumps(result, indent=2)}")
                except Exception as e:
                    print(f"Error running chain: {str(e)}")
            else:
                print("No custom agent selected. Skipping chain test.")
        else:
            print("No custom agents available. Create one with the Self-Replicator first.")
        
    elif choice == "4":
        print("\nMemory Contents:")
        contents = memory.get_all()
        print(json.dumps(contents, indent=2))
        
    elif choice == "5":
        print("\nExiting Sankalpa Platform Runner")
        break
        
    else:
        print("\nInvalid choice. Please try again.")
    
    print("\n" + "=" * 80)