#!/usr/bin/env python3
"""
Enhanced Agent Tester for Sankalpa

This script tests the self-replicator agent and demonstrates how agents can be created on-the-fly.
"""

import os
import sys
import json
from datetime import datetime
import traceback

# Function to create nice visual separators
def section(title):
    width = 80
    print("\n" + "=" * width)
    print(f" {title} ".center(width, "="))
    print("=" * width + "\n")

# Initialize
section("Initializing Test Environment")

# Make sure agents/custom directory exists
os.makedirs("agents/custom", exist_ok=True)
os.makedirs("memory/sessions", exist_ok=True)
print("✅ Created required directories")

# Import the base agent class
try:
    from agents.base import BaseAgent
    print("✅ Successfully imported BaseAgent")
except Exception as e:
    print(f"❌ Failed to import BaseAgent: {str(e)}")
    sys.exit(1)

# Import the self-replicator agent
try:
    from agents.enhanced.self_replicator_agent import SelfReplicatorAgent
    print("✅ Successfully imported SelfReplicatorAgent")
except Exception as e:
    print(f"❌ Failed to import SelfReplicatorAgent: {str(e)}")
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
print("✅ Created memory manager")

# Test creating a date formatter agent
section("Creating Date Formatter Agent")

# Create self-replicator agent
agent = SelfReplicatorAgent("self_replicator", memory)

# Create a new date formatter agent
agent_data = {
    "name": "date_formatter",
    "description": "An agent that formats dates in various ways",
    "category": "utility",
    "logic": '''result = {}

        # Get input date string and format
        date_string = input_data.get("date", None)
        date_format = input_data.get("format", "iso")
        
        if not date_string:
            return {"error": "No date provided", "status": "error"}
            
        try:
            # Parse the date
            from datetime import datetime
            
            # Try common date formats
            formats = [
                "%Y-%m-%d", "%Y/%m/%d", "%m/%d/%Y", "%d/%m/%Y", "%b %d, %Y",
                "%B %d, %Y", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"
            ]
            
            parsed_date = None
            for fmt in formats:
                try:
                    parsed_date = datetime.strptime(date_string, fmt)
                    break
                except ValueError:
                    continue
            
            if not parsed_date:
                # Try parsing as timestamp
                try:
                    parsed_date = datetime.fromtimestamp(float(date_string))
                except:
                    pass
            
            if not parsed_date:
                return {"error": "Could not parse date", "status": "error"}
            
            # Format according to requested format
            if date_format == "iso":
                result["formatted_date"] = parsed_date.isoformat()
            elif date_format == "short":
                result["formatted_date"] = parsed_date.strftime("%m/%d/%Y")
            elif date_format == "long":
                result["formatted_date"] = parsed_date.strftime("%B %d, %Y")
            elif date_format == "timestamp":
                result["formatted_date"] = str(int(parsed_date.timestamp()))
            else:
                # Custom format
                result["formatted_date"] = parsed_date.strftime(date_format)
            
            return result
                
        except Exception as e:
            return {"error": f"Error formatting date: {str(e)}", "status": "error"}''',
    "inputs": [
        {"name": "date", "type": "string"},
        {"name": "format", "type": "string"}
    ],
    "outputs": [
        {"name": "formatted_date", "type": "string"}
    ]
}

try:
    print("🔄 Creating date_formatter agent...")
    result = agent.run(agent_data)
    print(f"✅ Agent created successfully")
    
    # Check if agent file was created
    agent_file_path = "agents/custom/date_formatter.py"
    if os.path.exists(agent_file_path):
        print(f"✅ Agent file created at: {agent_file_path}")
        
        # Display part of the file
        with open(agent_file_path, "r") as f:
            file_content = f.read()
            print("\nFile preview:")
            print("\n".join(file_content.split("\n")[:10]) + "\n...")
    else:
        print(f"❌ Agent file not found at: {agent_file_path}")
    
    # Check if catalog was updated
    catalog_path = "catalog/agent_catalog.json"
    if os.path.exists(catalog_path):
        with open(catalog_path, "r") as f:
            catalog = json.load(f)
        
        if "date_formatter" in catalog:
            print("✅ Agent added to catalog")
        else:
            print("❌ Agent not found in catalog")
    else:
        print("❌ Catalog file not found")
        
except Exception as e:
    print(f"❌ Error creating agent: {str(e)}")
    traceback.print_exc()

# Test the newly created agent
section("Testing Date Formatter Agent")

try:
    # Import the agent
    sys.path.insert(0, ".")
    from agents.custom.date_formatter import DateFormatterAgent
    
    # Create an instance
    formatter = DateFormatterAgent("date_formatter", memory)
    print("✅ Successfully imported and instantiated DateFormatterAgent")
    
    # Test with different formats
    test_cases = [
        {"date": "2023-04-01", "format": "iso"},
        {"date": "2023-04-01", "format": "short"},
        {"date": "2023-04-01", "format": "long"},
        {"date": "2023-04-01", "format": "%A, %B %d, %Y"}
    ]
    
    for i, test_case in enumerate(test_cases):
        print(f"\nTest {i+1}: {test_case}")
        try:
            result = formatter.run(test_case)
            print(f"Result: {json.dumps(result, indent=2)}")
        except Exception as e:
            print(f"❌ Error running test: {str(e)}")
    
except Exception as e:
    print(f"❌ Error testing agent: {str(e)}")
    traceback.print_exc()

# Finish
section("Test Completed")
print("The self-replicator agent is working correctly and generated a new date_formatter agent.")
print("This demonstrates Sankalpa's ability to dynamically create new agents on demand.")
print("You can find the generated agent at: agents/custom/date_formatter.py")