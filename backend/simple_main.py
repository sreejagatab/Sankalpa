#!/usr/bin/env python3
"""
Simplified backend API server for Sankalpa
Avoids using WebSockets module for easier deployment
"""

import time
import traceback
import sys
import os
from fastapi import FastAPI, Depends, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

# Direct imports instead of package imports
from core.config import config
from core.logging import get_logger

# Initialize logger
logger = get_logger("api_simple")

# Create the FastAPI application
app = FastAPI(
    title="Sankalpa API Server",
    description="AI-powered development automation platform",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development - update for production
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

# Add request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests and responses"""
    start_time = time.time()
    
    # Generate a request ID
    request_id = request.headers.get("X-Request-ID", f"req_{int(start_time)}")
    
    # Log the request
    logger.info(
        f"Request started",
        extra={
            "request_id": request_id,
            "method": request.method,
            "url": str(request.url),
            "client": request.client.host
        }
    )
    
    try:
        # Process the request
        response = await call_next(request)
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Add processing time header
        response.headers["X-Process-Time"] = str(process_time)
        response.headers["X-Request-ID"] = request_id
        
        # Log the response
        logger.info(
            f"Request completed",
            extra={
                "request_id": request_id,
                "status_code": response.status_code,
                "process_time": process_time
            }
        )
        
        return response
    except Exception as e:
        # Log the error
        logger.error(
            f"Request failed: {str(e)}",
            extra={
                "request_id": request_id,
                "exception": str(e),
                "traceback": traceback.format_exc()
            }
        )
        
        # Return a 500 response
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )

# API endpoints
@app.get("/api/status")
async def status():
    """Status endpoint"""
    return {
        "status": "Sankalpa API Server is running!",
        "version": "1.0.0"
    }

@app.get("/api/agents")
async def list_agents():
    """List all available agents"""
    try:
        # Import agent loader and catalog
        import json
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from agents.loader import get_available_agents
        
        # Get available agents from catalog if it exists
        agents = []
        catalog_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "catalog", "agent_catalog.json")
        
        if os.path.exists(catalog_path):
            try:
                with open(catalog_path, "r") as f:
                    catalog = json.load(f)
                    
                for agent_id, agent_info in catalog.items():
                    agents.append({
                        "name": agent_id,
                        "description": agent_info.get("description", ""),
                        "category": agent_info.get("category", "custom"),
                        "model": agent_info.get("model", "GPT-4"),
                        "inputs": agent_info.get("inputs", [{"name": "input", "type": "string"}]),
                        "outputs": agent_info.get("outputs", [{"name": "output", "type": "object"}])
                    })
            except Exception as e:
                logger.error(f"Error loading catalog: {str(e)}")
        
        # Add core agents if not in catalog
        core_agents = [
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
            },
            {
                "name": "project_architect",
                "description": "Creates project structures based on requirements",
                "category": "builder",
                "model": "GPT-4",
                "inputs": [{"name": "requirements", "type": "string"}],
                "outputs": [{"name": "project_structure", "type": "object"}]
            }
        ]
        
        # Add core agents if not already in the list
        for core_agent in core_agents:
            if not any(a["name"] == core_agent["name"] for a in agents):
                agents.append(core_agent)
        
        # Get custom agents
        custom_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "agents", "custom")
        if os.path.exists(custom_dir):
            for filename in os.listdir(custom_dir):
                if filename.endswith(".py") and filename != "__init__.py":
                    agent_name = filename[:-3]
                    if not any(a["name"] == agent_name for a in agents):
                        agents.append({
                            "name": agent_name,
                            "description": f"Custom agent: {agent_name}",
                            "category": "custom",
                            "model": "GPT-4",
                            "inputs": [{"name": "input", "type": "string"}],
                            "outputs": [{"name": "output", "type": "object"}]
                        })
        
        return {"agents": agents}
    except Exception as e:
        logger.error(f"Error listing agents: {str(e)}")
        traceback.print_exc()
        return {"agents": [], "error": str(e)}

@app.get("/api/agents/enhanced")
async def list_enhanced_agents():
    """List all enhanced agents with simpler format for the composer UI"""
    try:
        # Get all agents first
        agents_response = await list_agents()
        agents_list = agents_response.get("agents", [])
        
        # Convert to enhanced format
        enhanced_agents = []
        for agent in agents_list:
            enhanced_agents.append({
                "id": agent.get("name", ""),
                "name": agent.get("name", "").replace("_", " ").title(),
                "description": agent.get("description", ""),
                "category": agent.get("category", "custom"),
                "model": agent.get("model", "GPT-4")
            })
        
        return enhanced_agents
    except Exception as e:
        logger.error(f"Error listing enhanced agents: {str(e)}")
        traceback.print_exc()
        return []

@app.post("/api/agents/execute")
async def execute_agent(request: Request):
    """Execute an agent with the given input data"""
    try:
        # Parse request body
        input_data = await request.json()
        agent_name = input_data.get("agent_name")
        agent_input = input_data.get("input_data", {})
        
        if not agent_name:
            raise HTTPException(status_code=400, detail="Missing agent_name in request")
        
        # Import the agent loader
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from agents.loader import load_agent
        
        # Load the agent
        agent = load_agent(agent_name)
        if not agent:
            raise HTTPException(status_code=404, detail=f"Agent {agent_name} not found")
        
        # Execute the agent
        start_time = time.time()
        result = agent.run(agent_input)
        execution_time = time.time() - start_time
        
        # Return the result
        return {
            "agent_name": agent_name,
            "execution_id": getattr(agent, "execution_id", f"exec_{int(time.time())}"),
            "result": result,
            "execution_time": execution_time
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error executing agent: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error executing agent: {str(e)}")

# Memory endpoints
@app.post("/api/memory/save")
async def save_memory(request: Request):
    """Save a key-value pair to memory"""
    try:
        data = await request.json()
        key = data.get("key")
        value = data.get("value")
        session_id = data.get("session_id")

        if not key:
            raise HTTPException(status_code=400, detail="Missing 'key' in request")

        # Import memory manager
        from memory.enhanced_memory_manager import EnhancedMemoryManager

        memory = EnhancedMemoryManager(default_session=session_id)
        memory.save(key, value)

        return {
            "status": "success",
            "message": f"Saved key '{key}' to memory",
            "session_id": memory.current_session
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error saving to memory: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error saving to memory: {str(e)}")

@app.post("/api/memory/load")
async def load_memory(request: Request):
    """Load a value from memory by key"""
    try:
        data = await request.json()
        key = data.get("key")
        session_id = data.get("session_id")

        if not key:
            raise HTTPException(status_code=400, detail="Missing 'key' in request")

        # Import memory manager
        from memory.enhanced_memory_manager import EnhancedMemoryManager

        memory = EnhancedMemoryManager(default_session=session_id)
        value = memory.load(key)

        return {
            "status": "success",
            "key": key,
            "value": value,
            "session_id": memory.current_session
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error loading from memory: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error loading from memory: {str(e)}")

@app.get("/api/memory/all")
async def get_all_memory(session_id: str = None):
    """Get all memory items for a session"""
    try:
        from memory.enhanced_memory_manager import EnhancedMemoryManager

        memory = EnhancedMemoryManager(default_session=session_id)
        all_data = memory.get_all()

        return {
            "status": "success",
            "session_id": memory.current_session,
            "data": all_data
        }
    except Exception as e:
        logger.error(f"Error getting all memory: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting all memory: {str(e)}")

@app.get("/api/memory/sessions")
async def list_sessions():
    """List all available memory sessions"""
    try:
        from memory.enhanced_memory_manager import EnhancedMemoryManager

        memory = EnhancedMemoryManager()
        sessions = memory.list_sessions()

        return {
            "status": "success",
            "sessions": sessions
        }
    except Exception as e:
        logger.error(f"Error listing sessions: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error listing sessions: {str(e)}")

# Chain endpoints
@app.post("/api/chains/execute")
async def execute_chain(request: Request):
    """Execute a chain of agents"""
    try:
        data = await request.json()
        chain_name = data.get("chain_name", "unnamed_chain")
        agents = data.get("agents", [])
        input_data = data.get("input_data", {})
        session_id = data.get("session_id")

        if not agents:
            raise HTTPException(status_code=400, detail="Missing 'agents' list in request")

        # Import required modules
        from agents.loader import load_agent
        from memory.enhanced_memory_manager import EnhancedMemoryManager

        # Initialize memory for the chain
        memory = EnhancedMemoryManager(default_session=session_id)

        # Execute each agent in sequence
        results = []
        current_input = input_data

        for agent_name in agents:
            # Load the agent
            agent = load_agent(agent_name)
            if not agent:
                results.append({
                    "agent": agent_name,
                    "status": "error",
                    "error": f"Agent '{agent_name}' not found"
                })
                continue

            # Execute the agent
            start_time = time.time()
            try:
                result = agent.run(current_input)
                execution_time = time.time() - start_time

                # Store result in memory
                memory.save(f"chain_{chain_name}_{agent_name}", result)

                results.append({
                    "agent": agent_name,
                    "status": "success",
                    "result": result,
                    "execution_time": execution_time
                })

                # Pass output to next agent
                current_input = result
            except Exception as e:
                results.append({
                    "agent": agent_name,
                    "status": "error",
                    "error": str(e)
                })

        return {
            "chain_name": chain_name,
            "status": "completed",
            "session_id": memory.current_session,
            "results": results,
            "final_output": current_input
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error executing chain: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error executing chain: {str(e)}")

@app.get("/api/chains")
async def list_chains():
    """List available chain templates"""
    try:
        import json

        chains = []

        # Check for chain templates in composer_flows directory
        flows_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "composer_flows")

        if os.path.exists(flows_dir):
            for filename in os.listdir(flows_dir):
                if filename.endswith(".json"):
                    try:
                        with open(os.path.join(flows_dir, filename), "r") as f:
                            chain_data = json.load(f)
                            chains.append({
                                "name": chain_data.get("name", filename[:-5]),
                                "description": chain_data.get("description", ""),
                                "agents": chain_data.get("agents", []),
                                "file": filename
                            })
                    except Exception:
                        pass

        # Add default chains
        default_chains = [
            {
                "name": "full_stack_builder",
                "description": "Build a complete full-stack application",
                "agents": ["project_architect", "frontend_builder", "backend_builder", "db_schema"]
            },
            {
                "name": "api_generator",
                "description": "Generate a REST API with database schema",
                "agents": ["db_schema", "backend_builder", "api_builder"]
            }
        ]

        for chain in default_chains:
            if not any(c["name"] == chain["name"] for c in chains):
                chains.append(chain)

        return {"chains": chains}
    except Exception as e:
        logger.error(f"Error listing chains: {str(e)}")
        return {"chains": [], "error": str(e)}

# Main entrypoint
if __name__ == "__main__":
    # Get configuration
    host = "0.0.0.0"
    port = int(os.environ.get("API_PORT", 8080))
    
    logger.info(f"Starting Simple API server on {host}:{port}")
    
    # Start the server without websockets
    uvicorn.run(app, host=host, port=port, ws="none")