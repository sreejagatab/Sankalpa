
import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from agents.base import BaseAgent
import json

class SessionReplayerAgent(BaseAgent):
    def run(self, input_data):
        session_file = input_data.get("session_file", "memory/sessions/session_log.json")
        try:
            with open(session_file, "r") as f:
                log = json.load(f)
        except Exception as e:
            return {"error": str(e)}

        replay = []
        for agent, output in log.items():
            replay.append(f"{agent}: {output.get('message', 'No message')}")

        return {
            "message": "Session replay complete.",
            "replay_log": replay
        }
