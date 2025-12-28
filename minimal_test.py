#!/usr/bin/env python3
"""
Minimal test script for Sankalpa agents
"""

import os
import sys
import json
from datetime import datetime

# Create required directories
os.makedirs("agents/custom", exist_ok=True)
os.makedirs("memory/sessions", exist_ok=True)

# Add the project root to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import the self-replicator agent
try:
    from agents.enhanced.self_replicator_agent import SelfReplicatorAgent
    print("Successfully imported SelfReplicatorAgent")
except Exception as e:
    print(f"Error importing SelfReplicatorAgent: {str(e)}")
    sys.exit(1)

# Create a simple memory manager
class MemoryManager:
    def __init__(self, filename="memory/sessions/test_session.json"):
        self.filename = filename
        self.memory = {}
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

# Create memory manager
memory = MemoryManager()

# Create self-replicator agent
agent = SelfReplicatorAgent("self_replicator", memory)
print(f"Created agent: {agent.name}")

# Simple test input
test_input = {
    "name": "hello_world",
    "description": "A simple hello world agent",
    "category": "testing",
    "logic": '''
        name = input_data.get("name", "World")
        result = {"greeting": f"Hello, {name}!"}
        return result
    ''',
    "inputs": [
        {"name": "name", "type": "string"}
    ],
    "outputs": [
        {"name": "greeting", "type": "string"}
    ]
}

# Run the agent
print("\nRunning self-replicator agent to create a hello_world agent...")
result = agent.run(test_input)

# Print the result
print("\nResult:")
print(json.dumps(result, indent=2))

# Check if the agent file was created
agent_file_path = "agents/custom/hello_world.py"
if os.path.exists(agent_file_path):
    print(f"\nAgent file created successfully: {agent_file_path}")
    with open(agent_file_path, "r") as f:
        print("\nFile content:")
        print(f.read())
else:
    print(f"\nAgent file was not created at: {agent_file_path}")

print("\nTest completed!")