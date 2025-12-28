from agents.base import BaseAgent

class RoleAuthAgent(BaseAgent):
    def run(self, input_data):
        files = {
            "backend/services/roles.py": """
def has_permission(user_role, required_role):
    roles = ["guest", "user", "admin"]
    return roles.index(user_role) >= roles.index(required_role)
"""
        }
        return {
            "message": "Role-based auth service created.",
            "files": files
        }