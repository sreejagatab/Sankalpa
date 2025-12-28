import os
import re
from typing import Dict, Any, List, Optional, Tuple
import json
import asyncio
import httpx

from sankalpa.core import get_logger
from sankalpa.core.caching import cache, cached

logger = get_logger("nlp.processor")

class NLPProcessor:
    """Natural language command processor for Sankalpa
    
    This module processes natural language commands and converts them
    into structured agent chains that can be executed.
    """
    
    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        """Initialize the NLP processor
        
        Args:
            model_name: The LLM model to use for processing
        """
        self.model_name = model_name
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.system_prompt = """
        You are an AI assistant that converts natural language commands into structured 
        Sankalpa agent chains. Your task is to:
        
        1. Analyze the user's intent
        2. Identify the specific agents needed
        3. Configure them with appropriate parameters
        4. Determine the optimal execution flow (sequential, parallel, or conditional)
        
        Your output should be a JSON object with the following structure:
        
        {
            "name": "Chain name based on user request",
            "description": "Brief description of what this chain does",
            "type": "sequential|parallel|conditional",
            "agents": [
                {
                    "name": "agent_name",
                    "type": "agent_type",
                    "parameters": {
                        "param1": "value1",
                        "param2": "value2"
                    }
                }
            ],
            "condition_key": "Only for conditional chains - the key to check",
            "condition_branches": {
                "value1": ["agent1", "agent2"],
                "value2": ["agent3", "agent4"]
            }
        }
        
        Available agent types:
        - project_architect: Creates project structures based on requirements
        - frontend_builder: Generates frontend code for web applications
        - backend_builder: Generates backend API code
        - api_builder: Generates REST API endpoints
        - db_schema: Creates database schema definitions
        - ui_generator: Creates UI components
        - test_suite: Generates test cases
        - deploy_executor: Handles deployment configuration
        - readme_writer: Creates documentation
        - security_scanner: Checks for security issues
        
        IMPORTANT: You must provide parameter values appropriate for each agent type.
        """
        
        if not self.api_key:
            logger.warning("OpenAI API key not found. NLP processing will not work properly.")
    
    async def process_command(self, command: str) -> Dict[str, Any]:
        """Process a natural language command
        
        Args:
            command: The natural language command
            
        Returns:
            Chain specification in JSON format
        """
        # Check if we have a cached result
        cache_key = f"nlp:command:{command}"
        cached_result = cache.get(cache_key)
        if cached_result:
            logger.info(f"Using cached result for command: {command[:30]}...")
            return cached_result
        
        # Process with LLM if API key is available
        if self.api_key:
            try:
                result = await self._process_with_openai(command)
                
                # Validate and clean the result
                result = self._validate_and_clean_result(result)
                
                # Cache the result
                cache.set(cache_key, result, ttl=3600)  # Cache for 1 hour
                
                return result
            except Exception as e:
                logger.error(f"Error processing command with OpenAI: {str(e)}")
                return self._fallback_processing(command)
        else:
            # Use fallback processing
            return self._fallback_processing(command)
    
    async def _process_with_openai(self, command: str) -> Dict[str, Any]:
        """Process command using OpenAI API
        
        Args:
            command: The natural language command
            
        Returns:
            Processed result as a dictionary
        """
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.model_name,
                        "messages": [
                            {"role": "system", "content": self.system_prompt},
                            {"role": "user", "content": command}
                        ],
                        "temperature": 0.2,
                        "max_tokens": 2000
                    }
                )
                
                if response.status_code != 200:
                    logger.error(f"OpenAI API error: {response.text}")
                    raise Exception(f"OpenAI API error: {response.status_code}")
                
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                
                # Extract JSON from response
                json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
                if json_match:
                    json_str = json_match.group(1)
                else:
                    json_str = content
                
                # Clean the string and parse JSON
                json_str = re.sub(r'^```json', '', json_str)
                json_str = re.sub(r'```$', '', json_str)
                json_str = json_str.strip()
                
                return json.loads(json_str)
                
        except Exception as e:
            logger.error(f"Error in OpenAI processing: {str(e)}")
            raise
    
    def _validate_and_clean_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and clean the result from the LLM
        
        Args:
            result: The result to validate
            
        Returns:
            Validated and cleaned result
        """
        # Check for required fields
        required_fields = ["name", "description", "type", "agents"]
        for field in required_fields:
            if field not in result:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate chain type
        valid_types = ["sequential", "parallel", "conditional"]
        if result["type"] not in valid_types:
            logger.warning(f"Invalid chain type: {result['type']}. Defaulting to sequential.")
            result["type"] = "sequential"
        
        # If conditional, validate condition fields
        if result["type"] == "conditional":
            if "condition_key" not in result or "condition_branches" not in result:
                logger.warning("Conditional chain missing condition_key or condition_branches. Defaulting to sequential.")
                result["type"] = "sequential"
                if "condition_key" in result:
                    del result["condition_key"]
                if "condition_branches" in result:
                    del result["condition_branches"]
        
        # Validate agents
        valid_agents = [
            "project_architect", "frontend_builder", "backend_builder", 
            "api_builder", "db_schema", "ui_generator", "test_suite", 
            "deploy_executor", "readme_writer", "security_scanner"
        ]
        
        cleaned_agents = []
        for agent in result["agents"]:
            if "name" not in agent or "type" not in agent:
                logger.warning(f"Agent missing name or type: {agent}. Skipping.")
                continue
                
            if agent["type"] not in valid_agents:
                logger.warning(f"Invalid agent type: {agent['type']}. Skipping.")
                continue
                
            # Ensure parameters is a dictionary
            if "parameters" not in agent or not isinstance(agent["parameters"], dict):
                agent["parameters"] = {}
                
            cleaned_agents.append(agent)
        
        result["agents"] = cleaned_agents
        
        return result
    
    def _fallback_processing(self, command: str) -> Dict[str, Any]:
        """Fallback processing when OpenAI API is not available
        
        Args:
            command: The natural language command
            
        Returns:
            Simple chain based on keyword detection
        """
        # Extract potential project type from command
        project_type = "generic"
        if re.search(r'\b(blog|website)\b', command, re.IGNORECASE):
            project_type = "blog"
        elif re.search(r'\b(app|application|dashboard)\b', command, re.IGNORECASE):
            project_type = "web-app"
        elif re.search(r'\b(api|rest|backend)\b', command, re.IGNORECASE):
            project_type = "api"
        
        # Create a basic chain based on the project type
        if project_type == "blog":
            return {
                "name": "Blog Generator",
                "description": f"Generate a blog website based on: {command}",
                "type": "sequential",
                "agents": [
                    {
                        "name": "architect",
                        "type": "project_architect",
                        "parameters": {
                            "project_type": "blog",
                            "requirements": command
                        }
                    },
                    {
                        "name": "frontend",
                        "type": "frontend_builder",
                        "parameters": {
                            "framework": "next",
                            "requirements": command
                        }
                    },
                    {
                        "name": "documentation",
                        "type": "readme_writer",
                        "parameters": {
                            "project_type": "blog",
                            "requirements": command
                        }
                    }
                ]
            }
        elif project_type == "web-app":
            return {
                "name": "Web App Generator",
                "description": f"Generate a web application based on: {command}",
                "type": "sequential",
                "agents": [
                    {
                        "name": "architect",
                        "type": "project_architect",
                        "parameters": {
                            "project_type": "web-app",
                            "requirements": command
                        }
                    },
                    {
                        "name": "frontend",
                        "type": "frontend_builder",
                        "parameters": {
                            "framework": "react",
                            "requirements": command
                        }
                    },
                    {
                        "name": "backend",
                        "type": "backend_builder",
                        "parameters": {
                            "framework": "fastapi",
                            "requirements": command
                        }
                    },
                    {
                        "name": "database",
                        "type": "db_schema",
                        "parameters": {
                            "database": "postgres",
                            "requirements": command
                        }
                    },
                    {
                        "name": "documentation",
                        "type": "readme_writer",
                        "parameters": {
                            "project_type": "web-app",
                            "requirements": command
                        }
                    }
                ]
            }
        elif project_type == "api":
            return {
                "name": "API Generator",
                "description": f"Generate a REST API based on: {command}",
                "type": "sequential",
                "agents": [
                    {
                        "name": "architect",
                        "type": "project_architect",
                        "parameters": {
                            "project_type": "api",
                            "requirements": command
                        }
                    },
                    {
                        "name": "api",
                        "type": "api_builder",
                        "parameters": {
                            "framework": "fastapi",
                            "requirements": command
                        }
                    },
                    {
                        "name": "database",
                        "type": "db_schema",
                        "parameters": {
                            "database": "postgres",
                            "requirements": command
                        }
                    },
                    {
                        "name": "tests",
                        "type": "test_suite",
                        "parameters": {
                            "test_type": "api",
                            "requirements": command
                        }
                    },
                    {
                        "name": "documentation",
                        "type": "readme_writer",
                        "parameters": {
                            "project_type": "api",
                            "requirements": command
                        }
                    }
                ]
            }
        else:
            # Generic project
            return {
                "name": "Generic Project Generator",
                "description": f"Generate a project based on: {command}",
                "type": "sequential",
                "agents": [
                    {
                        "name": "architect",
                        "type": "project_architect",
                        "parameters": {
                            "project_type": "generic",
                            "requirements": command
                        }
                    },
                    {
                        "name": "documentation",
                        "type": "readme_writer",
                        "parameters": {
                            "project_type": "generic",
                            "requirements": command
                        }
                    }
                ]
            }

# Singleton instance
nlp_processor = NLPProcessor()