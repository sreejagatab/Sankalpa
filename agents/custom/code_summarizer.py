

import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from agents.base import BaseAgent
from typing import Dict, Any

class CodeSummarizerAgent(BaseAgent):
    """
    An agent that summarizes code snippets
    
    Category: utility
    """
    
    def __init__(self, name="code_summarizer", memory=None):
        super().__init__(name, memory)
        self.category = "utility"
        self.description = "An agent that summarizes code snippets"
    
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the agent with the given input data
        
        Args:
            input_data: Dictionary containing input parameters
            
        Returns:
            Dictionary containing agent output
        """
        # Validate inputs
        for input_field in [{'name': 'code', 'type': 'string'}, {'name': 'language', 'type': 'string'}]:
            field_name = input_field["name"]
            if field_name not in input_data:
                return {
                    "error": f"Missing required input: {field_name}",
                    "status": "error"
                }
        
        # Agent implementation
        
            # Get the code snippet and language
            code = input_data.get("code", "")
            language = input_data.get("language", "unknown")
            
            if not code:
                return {"error": "No code provided", "status": "error"}
            
            # Count lines and characters
            lines = code.count('\n') + 1
            chars = len(code)
            
            # Detect language features based on keywords
            language_features = {}
            
            if language.lower() in ["python", "py", "unknown"]:
                # Check for Python features
                language_features["classes"] = code.count("class ")
                language_features["functions"] = code.count("def ")
                language_features["imports"] = code.count("import ")
                language_features["comments"] = code.count("#")
            
            elif language.lower() in ["javascript", "js", "ts", "typescript"]:
                # Check for JavaScript/TypeScript features
                language_features["functions"] = code.count("function ") + code.count("=>")
                language_features["classes"] = code.count("class ")
                language_features["imports"] = code.count("import ") + code.count("require(")
                language_features["comments"] = code.count("//") + code.count("/*")
                
            # Create summary
            result = {
                "summary": {
                    "language": language,
                    "lines": lines,
                    "characters": chars,
                    "features": language_features
                }
            }
            
            return result
        
        
        return {
            "message": "code_summarizer executed successfully",
            "status": "success",
            "data": result
        }
