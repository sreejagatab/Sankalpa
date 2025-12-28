"""
Integration tests for agent chains
"""

import pytest
import os
import sys
import json
from unittest.mock import Mock, patch

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from agents.enhanced_base import EnhancedBaseAgent
from agents.enhanced_chain_manager import EnhancedChainManager
from memory.enhanced_memory_manager import EnhancedMemoryManager

class TestAgent(EnhancedBaseAgent):
    """Test agent for integration testing"""

    def __init__(self, name, response=None):
        super().__init__(name)
        self.response = response or {"result": f"Output from {name}"}

    def _execute(self, input_data):
        # Process the input data
        if isinstance(input_data, dict) and "message" in input_data:
            # Echo back the message with agent name
            return {"result": f"{self.name} processed: {input_data['message']}"}

        # Return the default response
        return self.response

def test_agent_chain_execution():
    """Test execution of a chain of agents"""
    # Create memory manager
    memory = EnhancedMemoryManager()

    # Create test agents
    agent1 = TestAgent("agent1")
    agent2 = TestAgent("agent2")
    agent3 = TestAgent("agent3")

    # Create a chain
    chain = EnhancedChainManager([agent1, agent2, agent3], memory)

    # Execute the chain
    result = chain.run({"message": "Test message"})

    # Verify the result (should be from the last agent)
    assert result["result"] == "agent3 processed: Test message"

    # Verify all agents executed and stored results in memory
    assert memory.load("agent1")["result"] == "agent1 processed: Test message"
    assert memory.load("agent2")["result"] == "agent2 processed: Test message"
    assert memory.load("agent3")["result"] == "agent3 processed: Test message"

def test_agent_chain_with_data_passing():
    """Test data passing between agents in a chain"""
    # Create memory manager
    memory = EnhancedMemoryManager()

    # Create custom agents that modify the data
    class ProcessingAgent(EnhancedBaseAgent):
        def _execute(self, input_data):
            # Add a field with the agent's name
            result = input_data.copy() if isinstance(input_data, dict) else {}
            result[self.name] = f"Processed by {self.name}"
            return result

    # Create agents
    agent1 = ProcessingAgent("step1")
    agent2 = ProcessingAgent("step2")
    agent3 = ProcessingAgent("step3")

    # Create a chain
    chain = EnhancedChainManager([agent1, agent2, agent3], memory)

    # Execute the chain
    result = chain.run({"initial": "data"})

    # Verify the result contains data from all agents
    assert result["initial"] == "data"
    assert result["step1"] == "Processed by step1"
    assert result["step2"] == "Processed by step2"
    assert result["step3"] == "Processed by step3"

def test_conditional_chain_integration():
    """Test conditional chain execution"""
    # Create memory manager
    memory = EnhancedMemoryManager()

    # Create test agents
    path_a_agent = TestAgent("path_a_agent")
    path_b_agent = TestAgent("path_b_agent")

    # Create branches
    branches = {
        "a": [path_a_agent],
        "b": [path_b_agent]
    }

    # Create condition function
    def condition_func(input_data):
        return input_data.get("path", "a")

    # Create conditional chain
    from agents.enhanced_chain_manager import ConditionalChainManager
    chain = ConditionalChainManager(branches, condition_func, memory)

    # Test path A
    result_a = chain.run({"path": "a", "message": "Take path A"})
    assert result_a["result"] == "path_a_agent processed: Take path A"

    # Test path B
    memory.session_data = {}  # Reset memory
    result_b = chain.run({"path": "b", "message": "Take path B"})
    assert result_b["result"] == "path_b_agent processed: Take path B"

def test_parallel_chain_integration():
    """Test parallel chain execution"""
    # Create memory manager
    memory = EnhancedMemoryManager()

    # Create test agents
    agent1 = TestAgent("parallel1")
    agent2 = TestAgent("parallel2")
    agent3 = TestAgent("parallel3")

    # Create parallel chain
    from agents.enhanced_chain_manager import ParallelChainManager
    chain = ParallelChainManager([agent1, agent2, agent3], memory)

    # Execute the chain
    results = chain.run({"message": "Parallel test"})

    # Verify all agents executed
    assert "parallel1" in results
    assert "parallel2" in results
    assert "parallel3" in results

    # Verify results
    assert results["parallel1"]["result"] == "parallel1 processed: Parallel test"
    assert results["parallel2"]["result"] == "parallel2 processed: Parallel test"
    assert results["parallel3"]["result"] == "parallel3 processed: Parallel test"
