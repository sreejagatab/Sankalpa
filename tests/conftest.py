import os
import sys
import pytest
from fastapi.testclient import TestClient

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the enhanced application
from backend.enhanced_main import app
from core import config
from memory.enhanced_memory_manager import EnhancedMemoryManager

@pytest.fixture
def test_client():
    """Create a test client for the FastAPI application"""
    with TestClient(app) as client:
        yield client

@pytest.fixture
def test_memory():
    """Create a memory manager for tests that writes to a temporary location"""
    # Use a test-specific memory location
    test_memory_path = "memory/test_sessions"
    os.makedirs(test_memory_path, exist_ok=True)

    # Create a new memory manager with a unique session
    memory = EnhancedMemoryManager(base_path=test_memory_path)

    yield memory

    # Cleanup - delete test session file
    session_path = memory._get_session_path()
    if os.path.exists(session_path):
        os.remove(session_path)

@pytest.fixture
def mock_agents():
    """Create mock agents for testing"""
    from agents.enhanced_base import EnhancedBaseAgent

    class MockAgent(EnhancedBaseAgent):
        def __init__(self, name, response=None):
            super().__init__(name)
            self.response = response or {"result": f"Output from {name}"}

        def _execute(self, input_data):
            # Simply return the predefined response
            return self.response

    # Create a few mock agents
    agents = {
        "mock1": MockAgent("mock1"),
        "mock2": MockAgent("mock2"),
        "error_agent": MockAgent("error_agent"),
    }

    # Special behavior for error agent
    def _error_execute(input_data):
        raise ValueError("Simulated error")

    agents["error_agent"]._execute = _error_execute

    return agents

@pytest.fixture
def mock_token_header():
    """Create a mock authorization header for tests"""
    # In a real test, you would generate a proper JWT token
    # For simplicity, we'll just mock the auth middleware
    return {"Authorization": "Bearer test_token"}