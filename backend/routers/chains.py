
import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
import time
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from agents.loader import load_agent
from agents.enhanced_chain_manager import EnhancedChainManager, ParallelChainManager, ConditionalChainManager
from core import get_logger
from core.security import get_current_user
from memory.enhanced_memory_manager import EnhancedMemoryManager

# Initialize router
router = APIRouter()
logger = get_logger("api.chains")

# Memory manager
memory_manager = EnhancedMemoryManager()

# Pydantic models
class ChainDefinition(BaseModel):
    name: str
    description: str
    agents: List[str]
    type: str = Field("sequential", description="Chain type: sequential, parallel, conditional")
    condition_key: Optional[str] = Field(None, description="For conditional chains, the key to evaluate")
    condition_branches: Optional[Dict[str, List[str]]] = Field(None, description="For conditional chains, mapping conditions to agent lists")

class ChainList(BaseModel):
    chains: List[ChainDefinition]

class ChainExecution(BaseModel):
    chain_name: str
    input_data: Dict[str, Any]
    session_id: Optional[str] = None

class ChainResult(BaseModel):
    chain_name: str
    result: Dict[str, Any]
    execution_time: float
    metrics: Dict[str, Any]

# Routes
@router.get("/", response_model=ChainList)
async def list_chains(current_user = Depends(get_current_user)):
    """List all available chains"""
    # In a real implementation, you would query a database of saved chains
    # For now, just return a few example chains
    chains = [
        {
            "name": "blog_generation",
            "description": "Generate a blog post from a topic",
            "agents": ["project_architect", "markdown_editor", "seo_optimizer"],
            "type": "sequential"
        },
        {
            "name": "fullstack_app",
            "description": "Generate a full-stack application",
            "agents": ["project_architect", "frontend_builder", "backend_builder", "api_builder"],
            "type": "sequential"
        }
    ]
    
    return {"chains": chains}

@router.get("/{chain_name}", response_model=ChainDefinition)
async def get_chain_info(chain_name: str, current_user = Depends(get_current_user)):
    """Get information about a specific chain"""
    # In a real implementation, you would query a database
    # For now, just return an example chain
    try:
        # Mock chain info
        if chain_name == "blog_generation":
            chain_info = {
                "name": "blog_generation",
                "description": "Generate a blog post from a topic",
                "agents": ["project_architect", "markdown_editor", "seo_optimizer"],
                "type": "sequential"
            }
        elif chain_name == "conditional_example":
            chain_info = {
                "name": "conditional_example",
                "description": "Example of a conditional chain",
                "agents": [],  # No agents at top level for conditional chains
                "type": "conditional",
                "condition_key": "project_type",
                "condition_branches": {
                    "blog": ["project_architect", "markdown_editor"],
                    "webapp": ["project_architect", "frontend_builder", "backend_builder"],
                    "api": ["project_architect", "api_builder"]
                }
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Chain not found: {chain_name}"
            )
            
        return chain_info
    except Exception as e:
        logger.error(f"Failed to get chain info: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chain not found: {chain_name}"
        )

@router.post("/execute", response_model=ChainResult)
async def execute_chain(execution: ChainExecution, current_user = Depends(get_current_user)):
    """Execute a chain with the given input data"""
    try:
        # In a real implementation, you would load the chain definition from a database
        # For demonstration, we'll create a mock chain based on the name
        chain_info = None
        
        # Get chain info
        try:
            chain_info = await get_chain_info(execution.chain_name, current_user)
        except HTTPException:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Chain not found: {execution.chain_name}"
            )
        
        # Load the agents
        agent_chain = []
        
        # Create memory manager for this execution
        session_id = execution.session_id or f"chain_{execution.chain_name}_{int(time.time())}"
        memory = EnhancedMemoryManager(default_session=session_id)
        
        # Handle different chain types
        if chain_info.type == "sequential":
            for agent_name in chain_info.agents:
                agent = load_agent(agent_name)
                if not agent:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Agent not found: {agent_name}"
                    )
                agent_chain.append(agent)
                
            # Create the chain manager
            chain_manager = EnhancedChainManager(agent_chain, memory)
            
        elif chain_info.type == "parallel":
            for agent_name in chain_info.agents:
                agent = load_agent(agent_name)
                if not agent:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Agent not found: {agent_name}"
                    )
                agent_chain.append(agent)
                
            # Create the parallel chain manager
            chain_manager = ParallelChainManager(agent_chain, memory)
            
        elif chain_info.type == "conditional":
            if not chain_info.condition_key or not chain_info.condition_branches:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Conditional chain requires condition_key and condition_branches"
                )
                
            # Create agent chains for each branch
            agent_chains = {}
            for condition, agent_names in chain_info.condition_branches.items():
                branch_agents = []
                for agent_name in agent_names:
                    agent = load_agent(agent_name)
                    if not agent:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Agent not found: {agent_name}"
                        )
                    branch_agents.append(agent)
                agent_chains[condition] = branch_agents
                
            # Create condition function
            def condition_function(input_data):
                condition_value = input_data.get(chain_info.condition_key)
                if not condition_value or condition_value not in agent_chains:
                    # Default to first branch if condition not met
                    return list(agent_chains.keys())[0]
                return condition_value
                
            # Create the conditional chain manager
            chain_manager = ConditionalChainManager(agent_chains, condition_function, memory)
            
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported chain type: {chain_info.type}"
            )
        
        # Execute the chain
        start_time = time.time()
        result = chain_manager.run(execution.input_data)
        execution_time = time.time() - start_time
        
        # Get the metrics
        metrics = memory.load("chain_metrics") or {}
        
        logger.info(f"Chain {execution.chain_name} executed successfully")
        
        return {
            "chain_name": execution.chain_name,
            "result": result,
            "execution_time": execution_time,
            "metrics": metrics
        }
    except Exception as e:
        logger.error(f"Chain execution failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chain execution failed: {str(e)}"
        )