
import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from agents.base import BaseAgent

class SecurityScannerAgent(BaseAgent):
    def run(self, input_data):
        issues = []

        if 'eval(' in str(input_data):
            issues.append("Use of eval() detected — potential security risk.")
        if 'password' in str(input_data) and 'hashlib' not in str(input_data):
            issues.append("Password handling found without proper hashing.")

        return {
            "message": "Security scan complete.",
            "issues_found": issues if issues else ["No critical issues detected."]
        }