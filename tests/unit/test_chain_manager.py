import pytest
import time

from agents.enhanced_chain_manager import (
    EnhancedChainManager,
    ParallelChainManager,
    ConditionalChainManager,
    ChainExecutionError
)

def test_sequential_chain(test_memory, mock_agents):
    """Test sequential chain execution"""
    # Create a chain with two agents
    chain = EnhancedChainManager(
        [mock_agents["mock1"], mock_agents["mock2"]],
        test_memory
    )

    # Run the chain
    result = chain.run({"input": "test_input"})

    # Check the result
    assert result == {"result": "Output from mock2"}

    # Check that both agents were executed (results saved to memory)
    assert test_memory.load("mock1") == {"result": "Output from mock1"}
    assert test_memory.load("mock2") == {"result": "Output from mock2"}

    # Check that metrics were recorded
    metrics = test_memory.load("chain_metrics")
    assert metrics is not None
    assert metrics["success"] is True
    assert "total_execution_time" in metrics
    assert "agent_metrics" in metrics
    assert "mock1" in metrics["agent_metrics"]
    assert "mock2" in metrics["agent_metrics"]

def test_chain_with_error_agent_continue(test_memory, mock_agents):
    """Test chain with an error agent and continue strategy"""
    # Create a chain with error agent in the middle
    chain = EnhancedChainManager(
        [mock_agents["mock1"], mock_agents["error_agent"], mock_agents["mock2"]],
        test_memory,
        recovery_strategy="continue"  # Continue on error
    )

    # Run the chain
    result = chain.run({"input": "test_input"})

    # Check that the chain continued despite the error
    assert test_memory.load("mock1") == {"result": "Output from mock1"}
    assert test_memory.load("mock2") == {"result": "Output from mock2"}

    # Check metrics
    metrics = test_memory.load("chain_metrics")
    assert metrics is not None
    assert metrics["success"] is True  # Chain still succeeded (with recovery)
    assert "error_agent" in metrics["agent_metrics"]
    assert metrics["agent_metrics"]["error_agent"]["success"] is False  # This agent failed

def test_chain_with_error_agent_fail(test_memory, mock_agents):
    """Test chain with an error agent and fail strategy"""
    # Create a chain with error agent in the middle
    chain = EnhancedChainManager(
        [mock_agents["mock1"], mock_agents["error_agent"], mock_agents["mock2"]],
        test_memory,
        recovery_strategy="fail"  # Fail on error
    )

    # Run the chain - should raise an exception
    with pytest.raises(ChainExecutionError):
        chain.run({"input": "test_input"})

    # Check that only the first agent executed
    assert test_memory.load("mock1") == {"result": "Output from mock1"}
    assert test_memory.load("mock2") is None  # Not executed

    # Check metrics
    metrics = test_memory.load("chain_metrics")
    assert metrics is not None
    assert metrics["success"] is False  # Chain failed

def test_conditional_chain(test_memory, mock_agents):
    """Test conditional chain execution"""
    # Define condition branches
    branches = {
        "a": [mock_agents["mock1"]],
        "b": [mock_agents["mock2"]]
    }

    # Define condition function
    def condition_func(input_data):
        return input_data.get("branch", "a")

    # Create conditional chain
    chain = ConditionalChainManager(branches, condition_func, test_memory)

    # Test branch A
    result_a = chain.run({"branch": "a", "input": "test_input"})
    assert result_a == {"result": "Output from mock1"}

    # Reset memory and test branch B
    test_memory.session_data = {}
    result_b = chain.run({"branch": "b", "input": "test_input"})
    assert result_b == {"result": "Output from mock2"}

def test_chain_with_retries(test_memory, mock_agents):
    """Test chain with retries"""
    # Create a chain with error agent and retry strategy
    chain = EnhancedChainManager(
        [mock_agents["mock1"], mock_agents["error_agent"]],
        test_memory,
        recovery_strategy="retry",
        max_retries=2
    )

    # Add a retry counter to track attempts
    attempts = [0]
    original_execute = mock_agents["error_agent"]._execute

    def counting_execute(input_data):
        attempts[0] += 1
        if attempts[0] >= 2:  # Succeed on second attempt
            return {"result": "Success after retry"}
        return original_execute(input_data)

    # Replace the execute method
    mock_agents["error_agent"]._execute = counting_execute

    # Run the chain
    result = chain.run({"input": "test_input"})

    # Check that the agent was retried
    assert attempts[0] == 2
    assert result == {"result": "Success after retry"}

    # Check metrics
    metrics = test_memory.load("chain_metrics")
    assert metrics is not None
    assert metrics["success"] is True
    assert metrics["agent_metrics"]["error_agent"]["retries"] == 1  # One retry