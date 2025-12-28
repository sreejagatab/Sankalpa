

import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from agents.base import BaseAgent
from typing import Dict, Any

class HelloWorldAgent(BaseAgent):
    """
    A simple hello world agent
    
    Category: testing
    """
    
    def __init__(self, name="hello_world", memory=None):
        super().__init__(name, memory)
        self.category = "testing"
        self.description = "A simple hello world agent"
    
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the agent with the given input data
        
        Args:
            input_data: Dictionary containing input parameters
            
        Returns:
            Dictionary containing agent output
        """
        # Validate inputs
        for input_field in [{'name': 'name', 'type': 'string'}]:
            field_name = input_field["name"]
            if field_name not in input_data:
                return {
                    "error": f"Missing required input: {field_name}",
                    "status": "error"
                }
        
        # Agent implementation
        
        name = input_data.get("name", "World")
        result = {"greeting": f"Hello, {name}!"}
        return result
    
        
        return {
            "message": "hello_world executed successfully",
            "status": "success",
            "data": result
        }
