

import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from agents.base import BaseAgent
from typing import Dict, Any

class CustomCalculatorAgent(BaseAgent):
    """
    A simple calculator agent that performs arithmetic operations
    
    Category: utility
    """
    
    def __init__(self, name="custom_calculator", memory=None):
        super().__init__(name, memory)
        self.category = "utility"
        self.description = "A simple calculator agent that performs arithmetic operations"
    
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the agent with the given input data

        Args:
            input_data: Dictionary containing input parameters
                - operation: add, subtract, multiply, divide
                - num1 or a: first number
                - num2 or b: second number

        Returns:
            Dictionary containing agent output
        """
        # Agent implementation
        result = {}

        # Get operation type (support multiple formats)
        operation = input_data.get("operation", input_data.get("op", "add"))

        # Support both num1/num2 and a/b formats
        num1 = input_data.get("num1", input_data.get("a", input_data.get("x", 0)))
        num2 = input_data.get("num2", input_data.get("b", input_data.get("y", 0)))

        # Convert to numbers if strings
        try:
            num1 = float(num1)
            num2 = float(num2)
        except (ValueError, TypeError):
            return {"error": "Invalid number format", "status": "error"}
        
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
            return {"error": f"Unknown operation: {operation}", "status": "error"}
        
        return {
            "message": "custom_calculator executed successfully",
            "status": "success",
            "data": result
        }
