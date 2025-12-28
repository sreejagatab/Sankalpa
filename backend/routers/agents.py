
import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from typing import List, Dict, Any, Optional
import time
import os
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from pydantic import BaseModel, Field

from agents.loader import load_agent
from core import get_logger
from core.security import get_current_user
from memory.enhanced_memory_manager import EnhancedMemoryManager

# Initialize router
router = APIRouter()
logger = get_logger("api.agents")

# Memory manager
memory_manager = EnhancedMemoryManager()

# Pydantic models
class AgentInfo(BaseModel):
    name: str
    description: str
    category: str
    model: Optional[str] = None
    inputs: List[Dict[str, Any]]
    outputs: List[Dict[str, Any]]

class EnhancedAgentInfo(BaseModel):
    id: str
    name: str
    description: str
    category: str
    model: Optional[str] = None

class AgentList(BaseModel):
    agents: List[AgentInfo]

class EnhancedAgentList(BaseModel):
    agents: List[EnhancedAgentInfo]

class AgentExecution(BaseModel):
    agent_name: str
    input_data: Dict[str, Any]
    session_id: Optional[str] = None

class AgentResult(BaseModel):
    agent_name: str
    execution_id: str
    result: Dict[str, Any]
    execution_time: float

class FinetunerRequest(BaseModel):
    model: str = "gpt-3.5-turbo"
    dataset: Optional[str] = None
    epochs: int = 3
    batch_size: int = 4
    learning_rate: float = 0.0002
    auto_execute: bool = False
    api_key: Optional[str] = None

class SelfReplicatorRequest(BaseModel):
    name: str
    description: str
    category: str = "custom"
    logic: str
    inputs: List[Dict[str, Any]] = [{"name": "input", "type": "string"}]
    outputs: List[Dict[str, Any]] = [{"name": "output", "type": "object"}]

class VSCodeExtensionRequest(BaseModel):
    name: str = "sankalpa-extension"
    display_name: str = "Sankalpa AI Agents"
    description: str = "Integrate Sankalpa AI agents directly in your editor"
    publisher: str = "sankalpa"
    version: str = "0.1.0"

class DeploymentRequest(BaseModel):
    platform: str = "vercel"
    project_type: str = "next"
    project_path: str = "."
    env_vars: Dict[str, str] = {}
    domain: Optional[str] = None
    region: str = "us-east-1"

# Routes
@router.get("/", response_model=AgentList)
async def list_agents(current_user = Depends(get_current_user)):
    """List all available agents"""
    # In a real implementation, you would query the agent catalog
    # This combines both old and new agents
    agents = [
        {
            "name": "project_architect",
            "description": "Creates project structures based on requirements",
            "category": "builder",
            "model": "GPT-4",
            "inputs": [{"name": "requirements", "type": "string"}],
            "outputs": [{"name": "project_structure", "type": "object"}]
        },
        {
            "name": "api_builder",
            "description": "Generates API endpoints based on entity descriptions",
            "category": "builder",
            "model": "GPT-3.5",
            "inputs": [{"name": "entities", "type": "array"}],
            "outputs": [{"name": "api_code", "type": "object"}]
        },
        {
            "name": "test_suite",
            "description": "Generates test suites for code",
            "category": "testing",
            "model": "GPT-4",
            "inputs": [{"name": "code", "type": "object"}],
            "outputs": [{"name": "tests", "type": "object"}]
        },
        {
            "name": "finetuner",
            "description": "Fine-tunes LLMs on custom datasets",
            "category": "enhanced",
            "model": "GPT-4",
            "inputs": [
                {"name": "model", "type": "string"},
                {"name": "dataset", "type": "string"},
                {"name": "epochs", "type": "integer"},
                {"name": "batch_size", "type": "integer"},
                {"name": "learning_rate", "type": "number"}
            ],
            "outputs": [{"name": "files", "type": "object"}, {"name": "config", "type": "object"}]
        },
        {
            "name": "self_replicator",
            "description": "Creates specialized agents for specific tasks",
            "category": "enhanced",
            "model": "GPT-4",
            "inputs": [
                {"name": "name", "type": "string"},
                {"name": "description", "type": "string"},
                {"name": "category", "type": "string"},
                {"name": "logic", "type": "string"}
            ],
            "outputs": [{"name": "files", "type": "object"}]
        },
        {
            "name": "vs_code_extension",
            "description": "Creates VS Code extensions for agent integration",
            "category": "enhanced",
            "model": "GPT-4",
            "inputs": [
                {"name": "name", "type": "string"},
                {"name": "display_name", "type": "string"},
                {"name": "description", "type": "string"}
            ],
            "outputs": [{"name": "files", "type": "object"}]
        },
        {
            "name": "deploy_executor",
            "description": "Deploys projects to various platforms",
            "category": "deployment",
            "model": "GPT-4",
            "inputs": [
                {"name": "platform", "type": "string"},
                {"name": "project_type", "type": "string"},
                {"name": "project_path", "type": "string"}
            ],
            "outputs": [{"name": "files", "type": "object"}]
        }
    ]
    
    return {"agents": agents}

@router.get("/enhanced", response_model=List[EnhancedAgentInfo])
async def list_enhanced_agents(current_user = Depends(get_current_user)):
    """List all enhanced agents with simpler format for the composer UI"""
    agents = [
        {
            "id": "frontend_builder",
            "name": "Frontend Builder",
            "description": "Generates frontend UI components and code based on specifications",
            "category": "builder",
            "model": "GPT-4"
        },
        {
            "id": "backend_builder",
            "name": "Backend Builder",
            "description": "Creates backend services and APIs",
            "category": "builder",
            "model": "GPT-4"
        },
        {
            "id": "markdown_editor",
            "name": "Markdown Editor",
            "description": "Creates and edits markdown documentation",
            "category": "builder",
            "model": "GPT-3.5"
        },
        {
            "id": "db_schema",
            "name": "Database Schema Designer",
            "description": "Creates database schemas based on requirements",
            "category": "builder",
            "model": "GPT-3.5"
        },
        {
            "id": "api_builder",
            "name": "API Builder",
            "description": "Designs and documents RESTful APIs",
            "category": "builder",
            "model": "GPT-3.5"
        },
        {
            "id": "finetuner",
            "name": "Model Fine-Tuner",
            "description": "Fine-tunes LLMs on custom datasets",
            "category": "enhanced",
            "model": "GPT-4"
        },
        {
            "id": "copilot",
            "name": "Workflow Copilot",
            "description": "Assists with workflow creation and debugging",
            "category": "enhanced",
            "model": "Claude-3"
        },
        {
            "id": "self_replicator",
            "name": "Self-Replicator",
            "description": "Creates specialized agents for specific tasks",
            "category": "enhanced",
            "model": "GPT-4"
        },
        {
            "id": "vs_code_extension",
            "name": "VS Code Extension Generator",
            "description": "Creates VS Code extensions for agent integration",
            "category": "enhanced",
            "model": "GPT-4"
        },
        {
            "id": "deploy_executor",
            "name": "Deployment Executor",
            "description": "Deploys projects to various platforms",
            "category": "deployment",
            "model": "GPT-4"
        }
    ]
    
    return agents

@router.get("/{agent_name}", response_model=AgentInfo)
async def get_agent_info(agent_name: str, current_user = Depends(get_current_user)):
    """Get information about a specific agent"""
    # In a real implementation, you would query the agent catalog
    try:
        # Get the agent list
        agents_response = await list_agents(current_user)
        
        # Find the requested agent
        for agent in agents_response["agents"]:
            if agent["name"] == agent_name:
                return agent
                
        # If not found, use a generic response
        agent_info = {
            "name": agent_name,
            "description": "Example agent description",
            "category": "builder",
            "model": "GPT-3.5",
            "inputs": [{"name": "input1", "type": "string"}],
            "outputs": [{"name": "output1", "type": "object"}]
        }
        
        return agent_info
    except Exception as e:
        logger.error(f"Failed to get agent info: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent not found: {agent_name}"
        )

@router.post("/execute", response_model=AgentResult)
async def execute_agent(execution: AgentExecution, current_user = Depends(get_current_user)):
    """Execute an agent with the given input data"""
    try:
        # Load the agent
        agent = load_agent(execution.agent_name)
        
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent not found: {execution.agent_name}"
            )
        
        # Execute the agent
        start_time = time.time()
        result = agent.run(execution.input_data)
        execution_time = time.time() - start_time
        
        # Save the result to memory
        if execution.session_id:
            memory_manager.save(
                f"{execution.agent_name}_result",
                result,
                session_id=execution.session_id
            )
        
        logger.info(f"Agent {execution.agent_name} executed successfully")
        
        return {
            "agent_name": execution.agent_name,
            "execution_id": getattr(agent, "execution_id", "unknown"),
            "result": result,
            "execution_time": execution_time
        }
    except Exception as e:
        logger.error(f"Agent execution failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Agent execution failed: {str(e)}"
        )

@router.post("/finetuner/run", response_model=AgentResult)
async def run_finetuner(request: FinetunerRequest, current_user = Depends(get_current_user)):
    """Run the finetuner agent with specialized parameters"""
    try:
        # Load the agent
        agent = load_agent("finetuner")
        
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Finetuner agent not found"
            )
        
        # Build input data
        input_data = {
            "model": request.model,
            "dataset": request.dataset,
            "epochs": request.epochs,
            "batch_size": request.batch_size,
            "learning_rate": request.learning_rate,
            "auto_execute": request.auto_execute
        }
        
        # Add API key if provided
        if request.api_key:
            input_data["api_key"] = request.api_key
        
        # Execute the agent
        start_time = time.time()
        result = agent.run(input_data)
        execution_time = time.time() - start_time
        
        logger.info("Finetuner agent executed successfully")
        
        return {
            "agent_name": "finetuner",
            "execution_id": getattr(agent, "execution_id", "unknown"),
            "result": result,
            "execution_time": execution_time
        }
    except Exception as e:
        logger.error(f"Finetuner agent failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Finetuner agent failed: {str(e)}"
        )

@router.post("/finetuner/upload-dataset")
async def upload_dataset(file: UploadFile = File(...), current_user = Depends(get_current_user)):
    """Upload a dataset file for fine-tuning"""
    try:
        # Create directory if it doesn't exist
        os.makedirs("fine_tuning/data", exist_ok=True)
        
        # Save file
        file_path = f"fine_tuning/data/{file.filename}"
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        return {
            "status": "success",
            "message": "File uploaded successfully",
            "file_path": file_path
        }
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading file: {str(e)}"
        )

@router.post("/self_replicator/run", response_model=AgentResult)
async def run_self_replicator(request: SelfReplicatorRequest, current_user = Depends(get_current_user)):
    """Run the self-replicator agent to create a new agent"""
    try:
        # Load the agent
        agent = load_agent("self_replicator")
        
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Self-replicator agent not found"
            )
        
        # Build input data
        input_data = {
            "name": request.name,
            "description": request.description,
            "category": request.category,
            "logic": request.logic,
            "inputs": request.inputs,
            "outputs": request.outputs
        }
        
        # Execute the agent
        start_time = time.time()
        result = agent.run(input_data)
        execution_time = time.time() - start_time
        
        logger.info(f"Self-replicator agent created new agent: {request.name}")
        
        return {
            "agent_name": "self_replicator",
            "execution_id": getattr(agent, "execution_id", "unknown"),
            "result": result,
            "execution_time": execution_time
        }
    except Exception as e:
        logger.error(f"Self-replicator agent failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Self-replicator agent failed: {str(e)}"
        )

@router.post("/vs_code_extension/run", response_model=AgentResult)
async def run_vs_code_extension(request: VSCodeExtensionRequest, current_user = Depends(get_current_user)):
    """Generate a VS Code extension with the VS Code Extension agent"""
    try:
        # Load the agent
        agent = load_agent("vs_code_extension")
        
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="VS Code Extension agent not found"
            )
        
        # Build input data
        input_data = {
            "name": request.name,
            "display_name": request.display_name,
            "description": request.description,
            "publisher": request.publisher,
            "version": request.version
        }
        
        # Execute the agent
        start_time = time.time()
        result = agent.run(input_data)
        execution_time = time.time() - start_time
        
        logger.info(f"VS Code Extension agent generated extension: {request.name}")
        
        return {
            "agent_name": "vs_code_extension",
            "execution_id": getattr(agent, "execution_id", "unknown"),
            "result": result,
            "execution_time": execution_time
        }
    except Exception as e:
        logger.error(f"VS Code Extension agent failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"VS Code Extension agent failed: {str(e)}"
        )

@router.post("/deploy_executor/run", response_model=AgentResult)
async def run_deploy_executor(request: DeploymentRequest, current_user = Depends(get_current_user)):
    """Execute deployment with the Deployment Executor agent"""
    try:
        # Load the agent
        agent = load_agent("deploy_executor")
        
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Deployment Executor agent not found"
            )
        
        # Build input data
        input_data = {
            "platform": request.platform,
            "project_type": request.project_type,
            "project_path": request.project_path,
            "env_vars": request.env_vars
        }
        
        if request.domain:
            input_data["domain"] = request.domain
            
        if request.region:
            input_data["region"] = request.region
        
        # Execute the agent
        start_time = time.time()
        result = agent.run(input_data)
        execution_time = time.time() - start_time
        
        logger.info(f"Deployment Executor generated deployment for platform: {request.platform}")
        
        return {
            "agent_name": "deploy_executor",
            "execution_id": getattr(agent, "execution_id", "unknown"),
            "result": result,
            "execution_time": execution_time
        }
    except Exception as e:
        logger.error(f"Deployment Executor agent failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Deployment Executor agent failed: {str(e)}"
        )