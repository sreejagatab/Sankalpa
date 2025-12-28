
import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
import os
import json
from agents.base import BaseAgent

class SelfReplicatorAgent(BaseAgent):
    """
    Advanced agent that can generate new agent implementations
    based on specified requirements and then register them in the catalog.
    """
    
    def run(self, input_data):
        # Extract parameters
        agent_name = input_data.get("name", "new_agent").lower()
        description = input_data.get("description", f"Custom agent: {agent_name}")
        category = input_data.get("category", "custom")
        logic = input_data.get("logic", "# TODO: Define agent behavior")
        input_schema = input_data.get("inputs", [{"name": "input", "type": "string"}])
        output_schema = input_data.get("outputs", [{"name": "output", "type": "object"}])
        
        # Create directories if they don't exist
        os.makedirs(f"agents/custom", exist_ok=True)
        
        # Generate class name
        class_name = agent_name.title().replace('_', '')
        
        # Generate agent file content
        agent_code = f"""
from agents.base import BaseAgent
from typing import Dict, Any

class {class_name}Agent(BaseAgent):
    \"\"\"
    {description}
    
    Category: {category}
    \"\"\"
    
    def __init__(self, name="{agent_name}", memory=None):
        super().__init__(name, memory)
        self.category = "{category}"
        self.description = "{description}"
    
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        \"\"\"
        Execute the agent with the given input data
        
        Args:
            input_data: Dictionary containing input parameters
            
        Returns:
            Dictionary containing agent output
        \"\"\"
        # Validate inputs
        for input_field in {input_schema}:
            field_name = input_field["name"]
            if field_name not in input_data:
                return {{
                    "error": f"Missing required input: {{field_name}}",
                    "status": "error"
                }}
        
        # Agent implementation
        {logic}
        
        return {{
            "message": "{agent_name} executed successfully",
            "status": "success",
            "data": result
        }}
"""
        
        # Initialize file dictionary
        files = {
            f"agents/custom/{agent_name}.py": agent_code
        }
        
        # Actually write the agent file to disk
        agent_file_path = f"agents/custom/{agent_name}.py"
        try:
            with open(agent_file_path, "w") as f:
                f.write(agent_code)
            print(f"Created agent file: {agent_file_path}")
        except Exception as e:
            print(f"Error writing agent file: {str(e)}")
        
        # Create an __init__.py file if it doesn't exist
        init_path = "agents/custom/__init__.py"
        if not os.path.exists(init_path):
            with open(init_path, "w") as f:
                f.write("# Custom generated agents")
            files[init_path] = "# Custom generated agents"
        
        # Add to catalog
        try:
            catalog_path = "catalog/agent_catalog.json"
            if os.path.exists(catalog_path):
                with open(catalog_path, "r") as f:
                    catalog = json.load(f)
            else:
                catalog = {}
            
            # Add the new agent to the catalog
            catalog[agent_name] = {
                "description": description,
                "module": f"custom.{agent_name}",
                "category": category,
                "inputs": input_schema,
                "outputs": output_schema
            }
            
            # Save updated catalog
            with open(catalog_path, "w") as f:
                json.dump(catalog, f, indent=2)
            
            files[catalog_path] = json.dumps(catalog, indent=2)
            print(f"Updated catalog: {catalog_path}")
        except Exception as e:
            return {
                "message": f"Agent {agent_name} generated, but catalog update failed: {str(e)}",
                "files": files,
                "status": "partial_success"
            }
        
        return {
            "message": f"Agent {agent_name} generated and registered in catalog.",
            "files": files,
            "agent_name": agent_name,
            "class_name": f"{class_name}Agent",
            "category": category,
            "status": "success"
        }