
import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from abc import ABC, abstractmethod
import time
import traceback
import uuid
from typing import Dict, Any, Optional, Callable, List

from core import get_logger

logger = get_logger("agent")

class ValidationError(Exception):
    """Exception raised when input or output validation fails"""
    pass

class AgentTimeoutError(Exception):
    """Exception raised when an agent execution times out"""
    pass

class AgentExecutionError(Exception):
    """Exception raised when an agent execution fails"""
    pass

class AgentValidator:
    """Base validator for agent inputs and outputs"""
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate agent input data
        
        Args:
            input_data: Input data to validate
            
        Returns:
            True if validation passes
            
        Raises:
            ValidationError: If validation fails
        """
        return True
        
    def validate_output(self, output_data: Dict[str, Any]) -> bool:
        """Validate agent output data
        
        Args:
            output_data: Output data to validate
            
        Returns:
            True if validation passes
            
        Raises:
            ValidationError: If validation fails
        """
        return True

class EnhancedBaseAgent(ABC):
    """Enhanced base agent with validation, timing, and error handling"""
    
    def __init__(
        self, 
        name: str, 
        memory: Optional[Dict] = None,
        validator: Optional[AgentValidator] = None,
        timeout_seconds: int = 60
    ):
        """Initialize the agent
        
        Args:
            name: Name of the agent
            memory: Optional memory dict
            validator: Optional validator for input/output
            timeout_seconds: Maximum execution time in seconds
        """
        self.name = name
        self.memory = memory or {}
        self.validator = validator
        self.timeout_seconds = timeout_seconds
        self.logger = get_logger(f"agent.{name}")
        self.execution_id = None
        
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run the agent with timing, validation, and error handling
        
        Args:
            input_data: Input data for the agent
            
        Returns:
            Agent output data
            
        Raises:
            ValidationError: If input or output validation fails
            AgentTimeoutError: If execution times out
            AgentExecutionError: If execution fails
        """
        start_time = time.time()
        self.execution_id = str(uuid.uuid4())
        
        self.logger.info(
            f"Agent execution started",
            extra={
                "execution_id": self.execution_id,
                "agent": self.name
            }
        )
        
        try:
            # Validate input
            if self.validator and not self.validator.validate_input(input_data):
                raise ValidationError(f"Invalid input for agent: {self.name}")
                
            # Execute the agent implementation
            # TODO: Implement proper timeout handling
            result = self._execute(input_data)
            
            # Validate output
            if self.validator and not self.validator.validate_output(result):
                raise ValidationError(f"Invalid output from agent: {self.name}")
                
            execution_time = time.time() - start_time
            
            self.logger.info(
                f"Agent execution completed",
                extra={
                    "execution_id": self.execution_id,
                    "agent": self.name,
                    "execution_time": execution_time
                }
            )
            
            return result
            
        except ValidationError as e:
            self.logger.error(
                f"Validation failed: {str(e)}",
                extra={
                    "execution_id": self.execution_id,
                    "agent": self.name,
                    "error_type": "validation"
                }
            )
            raise
            
        except Exception as e:
            execution_time = time.time() - start_time
            
            self.logger.error(
                f"Agent execution failed: {str(e)}",
                extra={
                    "execution_id": self.execution_id,
                    "agent": self.name,
                    "error": str(e),
                    "traceback": traceback.format_exc(),
                    "execution_time": execution_time
                }
            )
            
            raise AgentExecutionError(f"Agent {self.name} execution failed: {str(e)}")
    
    @abstractmethod
    def _execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Actual agent implementation to be overridden by subclasses
        
        Args:
            input_data: Input data for the agent
            
        Returns:
            Agent output data
        """
        pass


class SchemaValidator(AgentValidator):
    """Schema-based validator for agent inputs and outputs"""
    
    def __init__(self, input_schema: Dict = None, output_schema: Dict = None):
        """Initialize the schema validator
        
        Args:
            input_schema: JSON Schema for input validation
            output_schema: JSON Schema for output validation
        """
        self.input_schema = input_schema
        self.output_schema = output_schema
        
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input against the input schema
        
        Args:
            input_data: Input data to validate
            
        Returns:
            True if validation passes
            
        Raises:
            ValidationError: If validation fails
        """
        if not self.input_schema:
            return True
            
        # TODO: Implement JSON Schema validation
        # For now, just do basic required field checking
        if "required" in self.input_schema:
            for field in self.input_schema["required"]:
                if field not in input_data:
                    raise ValidationError(f"Required field missing: {field}")
                    
        return True
        
    def validate_output(self, output_data: Dict[str, Any]) -> bool:
        """Validate output against the output schema
        
        Args:
            output_data: Output data to validate
            
        Returns:
            True if validation passes
            
        Raises:
            ValidationError: If validation fails
        """
        if not self.output_schema:
            return True
            
        # TODO: Implement JSON Schema validation
        # For now, just do basic required field checking
        if "required" in self.output_schema:
            for field in self.output_schema["required"]:
                if field not in output_data:
                    raise ValidationError(f"Required output field missing: {field}")
                    
        return True