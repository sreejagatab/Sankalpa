
import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from agents.base import BaseAgent

class EmailSystemAgent(BaseAgent):
    def run(self, input_data):
        files = {
            "backend/services/email.py": """
import smtplib
from email.message import EmailMessage

def send_email(to_address, subject, body):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = "noreply@sankalpa.dev"
    msg["To"] = to_address
    msg.set_content(body)

    with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
        server.login("user", "pass")
        server.send_message(msg)
"""
        }
        return {
            "message": "Email system with SMTP integration generated.",
            "files": files
        }