
import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from agents.base import BaseAgent

class ProductHuntCopywriterAgent(BaseAgent):
    def run(self, input_data):
        app_name = input_data.get("name", "Sankalpa")
        tagline = input_data.get("tagline", "The AI OS for building apps")
        features = input_data.get("features", [])

        body = f"""Launching {app_name} 🚀\n\n{tagline}\n\n{app_name} helps you build production-ready apps using AI agents that plan, build, test, and deploy code.\n\n### Key Features\n"""
        for f in features:
            body += f"- {f}\n"
        body += "\nLet us know what you think! 💬\n#ProductHunt #AIbuilder #Sankalpa"

        return {
            "message": "Product Hunt launch copy generated.",
            "files": {
                "launch/post.md": body
            }
        }
