
import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from agents.base import BaseAgent

class DomainLinkerAgent(BaseAgent):
    def run(self, input_data):
        domain = input_data.get("domain", "example.com")
        files = {
            "scripts/link_domain.sh": f"""
#!/bin/bash
# Link custom domain using Vercel CLI
domain={domain}
vercel domains add $domain
vercel alias set $domain
"""
        }
        return {
            "message": f"Domain linking script generated for {domain}.",
            "files": files
        }