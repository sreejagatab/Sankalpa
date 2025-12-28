
import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from agents.base import BaseAgent
import json
import datetime

class VersionTrackerAgent(BaseAgent):
    def run(self, input_data):
        log_entry = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "description": input_data.get("description", "No description provided")
        }
        path = "logs/version_log.json"
        try:
            with open(path, "r") as f:
                log = json.load(f)
        except:
            log = []
        log.append(log_entry)
        with open(path, "w") as f:
            json.dump(log, f, indent=2)
        return {"message": "Version log updated."}