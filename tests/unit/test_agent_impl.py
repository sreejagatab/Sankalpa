"""
Test agent implementation for unit tests
"""

from agents.enhanced_base import EnhancedBaseAgent
from typing import Dict, Any

class TestAgent(EnhancedBaseAgent):
    """Test agent for unit testing"""
    
    def __init__(self, name="test_agent", memory=None, response=None):
        super().__init__(name, memory)
        self.response = response or {"result": f"Output from {name}"}
        
    def _execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Implementation of the abstract method"""
        # Process the input data
        if isinstance(input_data, dict) and "message" in input_data:
            # Echo back the message with agent name
            return {"result": f"{self.name} processed: {input_data['message']}"}
        
        # Return the default response
        return self.response
