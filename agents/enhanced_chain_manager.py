
import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
import time
import traceback
from typing import List, Dict, Any, Optional, Callable

from core import get_logger, config
from memory.enhanced_memory_manager import EnhancedMemoryManager

logger = get_logger("chain_manager")

class ChainExecutionError(Exception):
    """Exception raised when a chain execution fails"""
    
    def __init__(self, message: str, agent_name: str, input_data: Any, original_error: Optional[Exception] = None):
        self.agent_name = agent_name
        self.input_data = input_data
        self.original_error = original_error
        super().__init__(f"{message} - Agent: {agent_name}, Error: {str(original_error)}")


class EnhancedChainManager:
    """Enhanced chain manager with error handling, retries, and monitoring"""
    
    def __init__(
        self, 
        agent_chain: List, 
        memory: EnhancedMemoryManager,
        recovery_strategy: str = None,
        max_retries: int = None,
        timeout_seconds: int = None,
        callback: Optional[Callable] = None
    ):
        """Initialize the chain manager
        
        Args:
            agent_chain: List of agent instances to execute
            memory: Enhanced memory manager instance
            recovery_strategy: How to handle failures ('continue', 'retry', 'fail')
            max_retries: Maximum number of retry attempts per agent
            timeout_seconds: Maximum execution time per agent
            callback: Optional callback function for progress updates
        """
        self.agent_chain = agent_chain
        self.memory = memory
        self.recovery_strategy = recovery_strategy or config.get("agents.recovery_strategy", "continue")
        self.max_retries = max_retries or config.get("agents.max_retries", 3)
        self.timeout_seconds = timeout_seconds or config.get("agents.timeout_seconds", 60)
        self.callback = callback
        
        # Execution metrics
        self.metrics = {
            "chain_start_time": 0,
            "chain_end_time": 0,
            "total_execution_time": 0,
            "agent_metrics": {},
            "success": False
        }
        
        logger.info(f"Chain manager initialized with {len(agent_chain)} agents")
    
    def _execute_agent(self, agent, input_data: Dict) -> Dict:
        """Execute a single agent with timing and retries
        
        Args:
            agent: Agent instance to execute
            input_data: Input data for the agent
            
        Returns:
            Agent output data
            
        Raises:
            ChainExecutionError: If the agent execution fails
        """
        agent_name = getattr(agent, 'name', str(agent.__class__.__name__))
        agent_metrics = {
            "start_time": time.time(),
            "end_time": 0,
            "execution_time": 0,
            "retries": 0,
            "success": False,
        }
        
        logger.info(f"Executing agent: {agent_name}")
        
        # Notify callback if available
        if self.callback:
            self.callback({
                "event": "agent_start",
                "agent_name": agent_name,
                "timestamp": agent_metrics["start_time"]
            })
        
        retry_count = 0
        last_error = None
        
        while retry_count <= self.max_retries:
            try:
                # Check if we're in a retry
                if retry_count > 0:
                    logger.info(f"Retry {retry_count}/{self.max_retries} for agent {agent_name}")
                    agent_metrics["retries"] = retry_count
                    
                    # Notify callback if available
                    if self.callback:
                        self.callback({
                            "event": "agent_retry",
                            "agent_name": agent_name,
                            "retry_count": retry_count,
                            "timestamp": time.time()
                        })
                
                # Execute the agent with timeout
                start_time = time.time()
                
                # TODO: Implement proper timeout handling with asyncio or threading
                result = agent.run(input_data)
                
                # Record success metrics
                agent_metrics["end_time"] = time.time()
                agent_metrics["execution_time"] = agent_metrics["end_time"] - start_time
                agent_metrics["success"] = True
                
                # Notify callback if available
                if self.callback:
                    self.callback({
                        "event": "agent_success",
                        "agent_name": agent_name,
                        "execution_time": agent_metrics["execution_time"],
                        "timestamp": agent_metrics["end_time"]
                    })
                
                # Save metrics for this agent
                self.metrics["agent_metrics"][agent_name] = agent_metrics
                
                return result
                
            except Exception as e:
                retry_count += 1
                last_error = e
                
                error_msg = f"Agent {agent_name} failed: {str(e)}"
                logger.error(error_msg)
                logger.debug(traceback.format_exc())
                
                # Notify callback if available
                if self.callback:
                    self.callback({
                        "event": "agent_error",
                        "agent_name": agent_name,
                        "error": str(e),
                        "timestamp": time.time()
                    })
                
                # Check if we should retry
                if retry_count <= self.max_retries and self.recovery_strategy == "retry":
                    # Exponential backoff
                    backoff_factor = config.get("agents.backoff_factor", 2)
                    backoff_time = backoff_factor ** (retry_count - 1)
                    logger.info(f"Backing off for {backoff_time}s before retry")
                    time.sleep(backoff_time)
                else:
                    # Save failed metrics
                    agent_metrics["end_time"] = time.time()
                    agent_metrics["execution_time"] = agent_metrics["end_time"] - agent_metrics["start_time"]
                    agent_metrics["success"] = False
                    self.metrics["agent_metrics"][agent_name] = agent_metrics
                    
                    break
        
        # All retries failed or we don't retry
        if self.recovery_strategy == "continue":
            logger.warning(f"Continuing chain execution despite failure in agent {agent_name}")
            return input_data  # Return the input unchanged
        else:
            # Fail the chain
            raise ChainExecutionError(
                f"Agent execution failed after {retry_count} attempts", 
                agent_name, 
                input_data, 
                last_error
            )
    
    def run(self, input_data: Dict) -> Dict:
        """Execute the chain of agents
        
        Args:
            input_data: Initial input for the chain
            
        Returns:
            Final output from the chain
            
        Raises:
            ChainExecutionError: If the chain execution fails
        """
        self.metrics["chain_start_time"] = time.time()
        result = input_data
        
        logger.info(f"Starting chain execution with {len(self.agent_chain)} agents")
        
        # Notify callback if available
        if self.callback:
            self.callback({
                "event": "chain_start",
                "agent_count": len(self.agent_chain),
                "timestamp": self.metrics["chain_start_time"]
            })
        
        try:
            for agent in self.agent_chain:
                # Execute the agent
                result = self._execute_agent(agent, result)
                
                # Save the result to memory
                agent_name = getattr(agent, 'name', str(agent.__class__.__name__))
                self.memory.save(agent_name, result)
            
            # Record success metrics
            self.metrics["chain_end_time"] = time.time()
            self.metrics["total_execution_time"] = self.metrics["chain_end_time"] - self.metrics["chain_start_time"]
            self.metrics["success"] = True
            
            # Save the chain metrics to memory
            self.memory.save("chain_metrics", self.metrics)
            
            # Notify callback if available
            if self.callback:
                self.callback({
                    "event": "chain_success",
                    "execution_time": self.metrics["total_execution_time"],
                    "timestamp": self.metrics["chain_end_time"]
                })
            
            logger.info(f"Chain execution completed successfully in {self.metrics['total_execution_time']:.2f}s")
            return result
            
        except Exception as e:
            self.metrics["chain_end_time"] = time.time()
            self.metrics["total_execution_time"] = self.metrics["chain_end_time"] - self.metrics["chain_start_time"]
            self.metrics["success"] = False
            
            # Save the chain metrics to memory
            self.memory.save("chain_metrics", self.metrics)
            
            # Notify callback if available
            if self.callback:
                self.callback({
                    "event": "chain_error",
                    "error": str(e),
                    "execution_time": self.metrics["total_execution_time"],
                    "timestamp": self.metrics["chain_end_time"]
                })
            
            logger.error(f"Chain execution failed: {str(e)}")
            raise


class ParallelChainManager(EnhancedChainManager):
    """Parallel chain manager for concurrent agent execution"""
    
    def run(self, input_data: Dict) -> Dict:
        """Execute agents in parallel and combine results
        
        Currently a stub - would use asyncio or threading in full implementation
        """
        # TODO: Implement parallel execution
        result = super().run(input_data)
        return result


class ConditionalChainManager(EnhancedChainManager):
    """Conditional chain manager with branching logic"""
    
    def __init__(self, agent_chains: Dict[str, List], condition_function: Callable, *args, **kwargs):
        """Initialize the conditional chain manager
        
        Args:
            agent_chains: Dictionary mapping condition values to agent chains
            condition_function: Function that determines which chain to execute
            *args, **kwargs: Arguments passed to parent class
        """
        # Initialize with an empty chain
        super().__init__([], *args, **kwargs)
        
        self.agent_chains = agent_chains
        self.condition_function = condition_function
    
    def run(self, input_data: Dict) -> Dict:
        """Execute the appropriate chain based on the condition
        
        Args:
            input_data: Initial input for the chain
            
        Returns:
            Final output from the selected chain
            
        Raises:
            ChainExecutionError: If the chain execution fails
        """
        # Determine which chain to execute
        condition_value = self.condition_function(input_data)
        
        logger.info(f"Conditional chain selected branch: {condition_value}")
        
        if condition_value not in self.agent_chains:
            logger.error(f"No chain defined for condition value: {condition_value}")
            raise ChainExecutionError(
                f"No chain defined for condition value: {condition_value}",
                "conditional_manager",
                input_data
            )
        
        # Set the selected agent chain
        self.agent_chain = self.agent_chains[condition_value]
        
        # Execute the selected chain
        return super().run(input_data)