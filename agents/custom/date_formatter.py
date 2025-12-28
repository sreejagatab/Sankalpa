

import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from agents.base import BaseAgent
from typing import Dict, Any

class DateFormatterAgent(BaseAgent):
    """
    An agent that formats dates in various ways
    
    Category: utility
    """
    
    def __init__(self, name="date_formatter", memory=None):
        super().__init__(name, memory)
        self.category = "utility"
        self.description = "An agent that formats dates in various ways"
    
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the agent with the given input data
        
        Args:
            input_data: Dictionary containing input parameters
            
        Returns:
            Dictionary containing agent output
        """
        # Validate inputs
        for input_field in [{'name': 'date', 'type': 'string'}, {'name': 'format', 'type': 'string'}]:
            field_name = input_field["name"]
            if field_name not in input_data:
                return {
                    "error": f"Missing required input: {field_name}",
                    "status": "error"
                }
        
        # Agent implementation
        result = {}

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
            return {"error": f"Error formatting date: {str(e)}", "status": "error"}
        
        return {
            "message": "date_formatter executed successfully",
            "status": "success",
            "data": result
        }
