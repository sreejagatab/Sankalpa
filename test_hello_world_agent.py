#!/usr/bin/env python3
"""
Test the hello_world agent that was created by the self-replicator
"""

import os
import sys
import json

# Add the project root to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Simple memory manager
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

# Import the hello_world agent
try:
    from agents.custom.hello_world import HelloWorldAgent
    print("Successfully imported HelloWorldAgent")
except Exception as e:
    print(f"Error importing HelloWorldAgent: {str(e)}")
    sys.exit(1)

# Create the agent
agent = HelloWorldAgent("hello_world", memory)
print(f"Created agent: {agent.name}")

# Test with different inputs
test_inputs = [
    {"name": "World"},
    {"name": "Sankalpa User"},
    {}  # Test with missing "name" to test validation
]

# Run tests
print("\nRunning tests...")
for i, test_input in enumerate(test_inputs):
    print(f"\nTest {i+1}: {test_input}")
    result = agent.run(test_input)
    print(f"Result: {json.dumps(result, indent=2)}")

print("\nAll tests completed!")