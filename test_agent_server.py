import os
import sys
import importlib
import json
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sankalpa-test")

# Add project root to path for imports 
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Create FastAPI app
app = FastAPI(
    title="Sankalpa Test Server",
    description="Test server for Sankalpa agent execution",
    version="0.1.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple memory manager
class MemoryManager:
    def __init__(self, filename="memory/sessions/session_log.json"):
        self.filename = filename
        self.memory = {}
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        self._load_from_file()

    def save(self, key, value):
        self.memory[key] = value
        with open(self.filename, "w") as f:
            json.dump(self.memory, f, indent=2)

    def load(self, key):
        return self.memory.get(key, None)

    def get_all(self):
        return self.memory

    def _load_from_file(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    self.memory = json.load(f)
            except json.JSONDecodeError:
                self.memory = {}

# Create memory manager
memory = MemoryManager()

# Agent loader function
def load_agent(agent_name: str, module_prefix: str = "agents"):
    try:
        # Determine module path and name
        if agent_name.count(".") > 0:
            # Handle direct module paths like "enhanced.self_replicator"
            module_name = f"{module_prefix}.{agent_name}"
            class_name = agent_name.split(".")[-1].title().replace('_', '') + 'Agent'
        else:
            # Handle simple names like "self_replicator" - check catalog
            catalog_path = "catalog/agent_catalog.json"
            
            if os.path.exists(catalog_path):
                with open(catalog_path, "r") as f:
                    catalog = json.load(f)
                
                if agent_name in catalog:
                    module_path = catalog[agent_name].get("module", "")
                    if module_path:
                        module_name = f"{module_prefix}.{module_path}"
                        class_name = agent_name.title().replace('_', '') + 'Agent'
                    else:
                        raise ImportError(f"No module path in catalog for {agent_name}")
                else:
                    # Try direct import from common folders
                    for folder in ["enhanced", "builder", "testing", "custom"]:
                        try:
                            module_name = f"{module_prefix}.{folder}.{agent_name}"
                            importlib.import_module(module_name)
                            class_name = agent_name.title().replace('_', '') + 'Agent'
                            break
                        except ImportError:
                            continue
                    else:
                        module_name = f"{module_prefix}.{agent_name}"
                        class_name = agent_name.title().replace('_', '') + 'Agent'
            else:
                # No catalog, try direct import
                module_name = f"{module_prefix}.{agent_name}"
                class_name = agent_name.title().replace('_', '') + 'Agent'
        
        # Import the module
        logger.info(f"Loading module: {module_name}")
        module = importlib.import_module(module_name)
        
        # Get the agent class
        logger.info(f"Looking for class: {class_name}")
        agent_class = getattr(module, class_name)
        
        # Create and return an instance of the agent
        return agent_class(agent_name, memory=memory)
    except Exception as e:
        logger.error(f"Error loading agent {agent_name}: {str(e)}")
        return None

@app.get("/")
async def root():
    return {"message": "Sankalpa Test Server is running!"}

@app.get("/api/status")
async def status():
    return {"status": "Sankalpa Test Server is running!", "version": "0.1.0"}

@app.get("/api/agents")
async def list_agents():
    """List all available agents from the catalog"""
    catalog_path = "catalog/agent_catalog.json"
    if os.path.exists(catalog_path):
        with open(catalog_path, "r") as f:
            catalog = json.load(f)
        
        agents = []
        for name, info in catalog.items():
            agents.append({
                "name": name,
                "description": info.get("description", ""),
                "module": info.get("module", ""),
                "category": info.get("category", ""),
                "inputs": info.get("inputs", []),
                "outputs": info.get("outputs", [])
            })
        
        return {"agents": agents, "count": len(agents)}
    else:
        return {"agents": [], "count": 0, "error": "Agent catalog not found"}

@app.post("/api/agents/execute/{agent_name}")
async def execute_agent(agent_name: str, input_data: Dict[str, Any]):
    """Execute an agent with the given input data"""
    try:
        # Load the agent
        agent = load_agent(agent_name)
        
        if not agent:
            raise HTTPException(
                status_code=404,
                detail=f"Agent {agent_name} not found"
            )
        
        # Execute the agent
        start_time = datetime.utcnow()
        result = agent.run(input_data)
        end_time = datetime.utcnow()
        execution_time = (end_time - start_time).total_seconds()
        
        # Save to memory
        memory.save(f"execution_{agent_name}_{start_time.isoformat()}", {
            "agent": agent_name,
            "input": input_data,
            "result": result,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "execution_time": execution_time
        })
        
        # Return result
        return {
            "agent": agent_name,
            "result": result,
            "execution_time": execution_time,
            "timestamp": end_time.isoformat()
        }
    except Exception as e:
        logger.error(f"Error executing agent {agent_name}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error executing agent: {str(e)}"
        )

@app.get("/api/memory")
async def get_memory():
    """Get all memory data"""
    return memory.get_all()

# Direct agent endpoints for specific useful agents
@app.post("/api/create-agent")
async def create_agent(agent_data: Dict[str, Any]):
    """Create a new agent using the self-replicator"""
    try:
        # Load the self-replicator agent
        agent = load_agent("enhanced.self_replicator")
        
        if not agent:
            raise HTTPException(
                status_code=500,
                detail="Self-replicator agent not found"
            )
        
        # Execute the agent
        result = agent.run(agent_data)
        
        # Return result
        return {
            "message": "Agent created successfully",
            "result": result
        }
    except Exception as e:
        logger.error(f"Error creating agent: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error creating agent: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run("test_agent_server:app", host="0.0.0.0", port=8080, reload=True)