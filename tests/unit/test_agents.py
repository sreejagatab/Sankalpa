"""
Unit tests for agent functionality
"""

import pytest
import os
import sys
import json
from unittest.mock import Mock, patch

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from agents.enhanced_base import EnhancedBaseAgent
from agents.enhanced.self_replicator_agent import SelfReplicatorAgent
from tests.unit.test_agent_impl import TestAgent

def test_base_agent_initialization():
    """Test basic agent initialization"""
    agent = TestAgent("test_agent")
    assert agent.name == "test_agent"

def test_agent_execution():
    """Test agent execution flow"""
    # Create a test agent with a mock execution method
    agent = TestAgent("test_agent")

    # Mock the _execute method
    original_execute = agent._execute
    agent._execute = Mock(return_value={"result": "test_result"})

    # Test execution
    result = agent.run({"input": "test_input"})

    # Verify the result
    assert result == {"result": "test_result"}
    agent._execute.assert_called_once_with({"input": "test_input"})

    # Restore original method
    agent._execute = original_execute

def test_agent_with_memory(test_memory):
    """Test agent with memory integration"""
    # Create an agent with memory
    agent = TestAgent("memory_agent", memory=test_memory)

    # Mock execution that uses memory
    def mock_execute(input_data):
        # Store something in memory
        agent.memory.save("test_key", "test_value")
        return {"result": "memory_test"}

    # Replace execution method
    original_execute = agent._execute
    agent._execute = mock_execute

    # Execute the agent
    result = agent.run({"input": "test"})

    # Verify memory was used
    assert agent.memory.load("test_key") == "test_value"
    assert result == {"result": "memory_test"}

    # Restore original method
    agent._execute = original_execute

def test_self_replicator_agent():
    """Test the self-replicator agent"""
    # Create a mock for the BaseAgent.run method
    with patch('agents.base.BaseAgent.run') as mock_run:
        # Set up the mock to return a valid response
        mock_run.return_value = {
            "files": {
                "agents/custom/test_new_agent.py": "class NewAgent(BaseAgent):\n    def run(self, input_data):\n        return {'result': 'new agent'}\n"
            },
            "agent_name": "test_new_agent",
            "status": "success"
        }

        # Create the agent
        memory = Mock()
        agent = SelfReplicatorAgent("self_replicator", memory)

        # Test the agent
        result = agent.run({
            "name": "test_new_agent",
            "description": "Test agent",
            "logic": "result = {'output': 'test'}"
        })

        # Verify the result
        assert "files" in result
        assert "agent_name" in result
        assert result["agent_name"] == "test_new_agent"

def test_agent_error_handling():
    """Test agent error handling"""
    # Create an agent that raises an exception
    agent = TestAgent("error_agent")

    # Mock execution that raises an exception
    def mock_execute_with_error(input_data):
        raise ValueError("Test error")

    # Replace execution method
    original_execute = agent._execute
    agent._execute = mock_execute_with_error

    # Execute the agent and expect an exception
    with pytest.raises(Exception):
        agent.run({"input": "test"})

    # Restore original method
    agent._execute = original_execute

def test_agent_with_capabilities():
    """Test agent capabilities"""
    # Create an agent with specific capabilities
    agent = TestAgent("capability_agent")

    # Add custom capabilities
    agent.capabilities = ["test", "analyze", "generate"]

    # Verify capabilities
    assert "test" in agent.capabilities
    assert "analyze" in agent.capabilities
    assert "generate" in agent.capabilities
    assert len(agent.capabilities) == 3
