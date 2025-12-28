
import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from agents.base import BaseAgent

class UiGeneratorAgent(BaseAgent):
    def run(self, input_data):
        files = {
            "frontend/components/UserForm.tsx": """
export default function UserForm() {
  return (
    <form className=\"space-y-4\">
      <input type=\"text\" placeholder=\"Username\" className=\"border p-2 rounded w-full\" />
      <input type=\"email\" placeholder=\"Email\" className=\"border p-2 rounded w-full\" />
      <button type=\"submit\" className=\"bg-blue-500 text-white px-4 py-2 rounded\">Submit</button>
    </form>
  );
}
"""
        }
        return {
            "message": "UI form component generated.",
            "files": files
        }