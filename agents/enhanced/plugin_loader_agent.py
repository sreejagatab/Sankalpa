
import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from agents.base import BaseAgent
import json

class PluginLoaderAgent(BaseAgent):
    def run(self, input_data):
        plugin_name = input_data.get("plugin", "example_plugin")
        module_path = f"plugins/{plugin_name}.py"
        code = f"def run_plugin(input):\n    return \"{plugin_name} executed\""

        catalog_path = "catalog/plugin_registry.json"
        try:
            with open(catalog_path, "r") as f:
                registry = json.load(f)
        except:
            registry = {}

        registry[plugin_name] = {"path": module_path, "description": "Custom plugin"}

        with open(catalog_path, "w") as f:
            json.dump(registry, f, indent=2)

        return {
            "message": f"Plugin {plugin_name} created and registered.",
            "files": {module_path: code, catalog_path: json.dumps(registry, indent=2)}
        }