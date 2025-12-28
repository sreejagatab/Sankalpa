"""
End-to-end tests for API workflow
"""

import pytest
import os
import sys
import time
import json
import requests

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Skip these tests if the API server is not running
pytestmark = pytest.mark.skipif(
    not os.environ.get("RUN_E2E_TESTS"),
    reason="E2E tests are only run when RUN_E2E_TESTS environment variable is set"
)

@pytest.fixture(scope="module")
def api_url():
    """Get the API URL"""
    return "http://localhost:8000"

@pytest.fixture(scope="module")
def app_server():
    """Start the application server for testing"""
    import subprocess
    import time
    
    # Start the backend server
    backend_process = subprocess.Popen(
        ["python", "run_sankalpa.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for the server to start
    time.sleep(5)
    
    yield
    
    # Clean up
    backend_process.terminate()
    backend_process.wait()

def test_api_status(api_url, app_server):
    """Test the API status endpoint"""
    response = requests.get(f"{api_url}/api/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "Ultimate Sankalpa API is running!"

def test_api_health(api_url, app_server):
    """Test the API health endpoint"""
    response = requests.get(f"{api_url}/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data
    assert "timestamp" in data

def test_agents_list(api_url, app_server):
    """Test the agents list endpoint"""
    response = requests.get(f"{api_url}/api/agents")
    assert response.status_code == 200
    data = response.json()
    assert "agents" in data
    assert isinstance(data["agents"], list)
    assert len(data["agents"]) > 0

def test_agent_execution(api_url, app_server):
    """Test executing an agent"""
    # First, get the list of agents
    response = requests.get(f"{api_url}/api/agents")
    assert response.status_code == 200
    data = response.json()
    
    # Get the first agent
    if data["agents"]:
        agent_id = data["agents"][0]["id"]
        
        # Execute the agent
        response = requests.post(
            f"{api_url}/api/agents/execute/{agent_id}",
            json={"input": "Test input for API workflow"}
        )
        assert response.status_code == 200
        result = response.json()
        assert "result" in result

def test_memory_operations(api_url, app_server):
    """Test memory operations"""
    # Save data to memory
    test_data = {"value": "test_value", "timestamp": time.time()}
    response = requests.post(
        f"{api_url}/api/memory/test_key",
        json=test_data
    )
    assert response.status_code == 200
    
    # Get the data back
    response = requests.get(f"{api_url}/api/memory/test_key")
    assert response.status_code == 200
    data = response.json()
    assert data["value"] == "test_value"
    
    # List all keys
    response = requests.get(f"{api_url}/api/memory")
    assert response.status_code == 200
    data = response.json()
    assert "keys" in data
    assert "test_key" in data["keys"]
    
    # Delete the key
    response = requests.delete(f"{api_url}/api/memory/test_key")
    assert response.status_code == 200
    
    # Verify it's gone
    response = requests.get(f"{api_url}/api/memory/test_key")
    assert response.status_code == 404

def test_chain_operations(api_url, app_server):
    """Test chain operations"""
    # First, get the list of agents
    response = requests.get(f"{api_url}/api/agents")
    assert response.status_code == 200
    agents_data = response.json()
    
    if len(agents_data["agents"]) >= 2:
        # Get the first two agents
        agent1_id = agents_data["agents"][0]["id"]
        agent2_id = agents_data["agents"][1]["id"]
        
        # Create a chain
        chain_config = {
            "name": "test_chain",
            "agents": [agent1_id, agent2_id],
            "type": "sequential"
        }
        
        response = requests.post(
            f"{api_url}/api/chains/create",
            json=chain_config
        )
        assert response.status_code == 200
        chain_data = response.json()
        assert chain_data["name"] == "test_chain"
        
        # Execute the chain
        response = requests.post(
            f"{api_url}/api/chains/execute/test_chain",
            json={"input": "Test input for chain"}
        )
        assert response.status_code == 200
        result = response.json()
        assert "result" in result
        
        # List all chains
        response = requests.get(f"{api_url}/api/chains")
        assert response.status_code == 200
        chains_data = response.json()
        assert "chains" in chains_data
        assert any(chain["name"] == "test_chain" for chain in chains_data["chains"])
        
        # Delete the chain
        response = requests.delete(f"{api_url}/api/chains/test_chain")
        assert response.status_code == 200
        
        # Verify it's gone
        response = requests.get(f"{api_url}/api/chains/test_chain")
        assert response.status_code == 404
