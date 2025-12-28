
import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self, name, memory=None):
        self.name = name
        self.memory = memory or {}

    @abstractmethod
    def run(self, input_data: dict) -> dict:
        pass
