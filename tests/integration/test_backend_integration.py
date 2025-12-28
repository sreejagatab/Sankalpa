"""
Integration tests for backend components
"""

import pytest
import os
import sys
import json
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.enhanced_main import app
from memory.enhanced_memory_manager import EnhancedMemoryManager
from agents.enhanced_base import EnhancedBaseAgent

def test_api_memory_integration(test_client, test_memory):
    """Test integration between API and memory manager"""
    # Mock the memory manager in the app
    app.state.memory = test_memory

    # Save some test data to memory
    test_memory.save("test_key", {"value": "test_value"})

    # Test retrieving the data via API
    response = test_client.get("/api/memory/test_key")
    assert response.status_code == 200
    data = response.json()
    assert data["value"] == "test_value"

    # Test saving data via API
    new_data = {"value": "new_value"}
    response = test_client.post("/api/memory/new_key", json=new_data)
    assert response.status_code == 200

    # Verify data was saved
    assert test_memory.load("new_key") == new_data

def test_api_agent_integration(test_client, mock_agents):
    """Test integration between API and agents"""
    # Mock the agents in the app
    app.state.agents = mock_agents

    # Test executing an agent via API
    response = test_client.post("/api/agents/execute/mock1", json={"input": "test"})
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == "Output from mock1"

    # Test error handling
    response = test_client.post("/api/agents/execute/error_agent", json={"input": "test"})
    assert response.status_code == 500
    data = response.json()
    assert "error" in data

def test_api_chain_integration(test_client, mock_agents, test_memory):
    """Test integration between API and agent chains"""
    # Mock the components in the app
    app.state.agents = mock_agents
    app.state.memory = test_memory

    # Create a chain configuration
    chain_config = {
        "name": "test_chain",
        "agents": ["mock1", "mock2"],
        "type": "sequential"
    }

    # Create the chain via API
    response = test_client.post("/api/chains/create", json=chain_config)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "test_chain"

    # Execute the chain
    response = test_client.post("/api/chains/execute/test_chain", json={"input": "test"})
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == "Output from mock2"

    # Verify chain execution was recorded in memory
    chain_metrics = test_memory.load("chain_metrics")
    assert chain_metrics is not None
    assert chain_metrics["success"] is True

def test_websocket_integration():
    """Test WebSocket integration"""
    from fastapi.testclient import TestClient
    from backend.main import app

    client = TestClient(app)

    # Mock authentication
    with patch("backend.websockets.routes.get_user_from_token",
               return_value={"id": "test_user", "username": "Test User"}):

        # Connect to WebSocket
        with client.websocket_connect("/ws/collaboration/test-room?token=valid_token") as websocket:
            # Send a message
            websocket.send_json({"type": "chat", "message": "Hello"})

            # Receive the message back (echo)
            data = websocket.receive_json()
            assert data["type"] == "chat"
            assert "message" in data

def test_database_integration():
    """Test database integration"""
    # This is a placeholder for database integration tests
    # In a real implementation, you would:
    # 1. Set up a test database
    # 2. Create test models
    # 3. Perform CRUD operations
    # 4. Verify the results

    # For now, we'll just mark this as a placeholder
    pass
