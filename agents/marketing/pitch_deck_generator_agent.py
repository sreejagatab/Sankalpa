
import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from agents.base import BaseAgent

class PitchDeckGeneratorAgent(BaseAgent):
    def run(self, input_data):
        slides = [
            "Problem",
            "Solution",
            "Product Demo",
            "Market Opportunity",
            "Business Model",
            "Go-To-Market",
            "Competition",
            "Team",
            "Financials",
            "Vision & Ask"
        ]
        deck = "# Sankalpa Pitch Deck\n\n"
        for slide in slides:
            deck += f"## {slide}\n\n(Add content here)\n\n"
        return {
            "message": "Pitch deck outline generated.",
            "files": {
                "pitch/pitch_deck.md": deck
            }
        }