#!/usr/bin/env python3
"""
Minimal API server for Sankalpa that supports basic agent operations
"""

import os
import sys
import json
import traceback
from datetime import datetime

# Add the project root to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Create FastAPI app
app = FastAPI(
    title="Sankalpa Minimal API Server",
    description="Minimal API server for Sankalpa",
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

# Memory manager
class MemoryManager:
    def __init__(self, filename="memory/sessions/minimal_api.json"):
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
            except Exception:
                self.memory = {}

# Create memory manager
memory = MemoryManager()

# Create direct imports of agents we want to use
from agents.base import BaseAgent
from agents.enhanced.self_replicator_agent import SelfReplicatorAgent
from agents.builder.project_architect_agent import ProjectArchitectAgent

# Create endpoints
@app.get("/")
async def root():
    return {"message": "Sankalpa Minimal API Server is running!"}

@app.get("/api/status")
async def status():
    return {"status": "Sankalpa Minimal API is running!", "version": "0.1.0"}

@app.get("/api/agents")
async def list_agents():
    """List available agents"""
    agents = [
        {
            "name": "self_replicator",
            "description": "Creates new agents from specifications",
            "category": "enhanced"
        },
        {
            "name": "project_architect",
            "description": "Creates project structure",
            "category": "builder"
        }
    ]
    
    # Add custom agents if they exist
    custom_dir = "agents/custom"
    if os.path.exists(custom_dir):
        for filename in os.listdir(custom_dir):
            if filename.endswith(".py") and filename != "__init__.py":
                agent_name = filename[:-3]
                agents.append({
                    "name": agent_name,
                    "description": f"Custom agent: {agent_name}",
                    "category": "custom"
                })
    
    return {"agents": agents, "count": len(agents)}

@app.get("/api/memory")
async def get_memory():
    """Get memory contents"""
    return memory.get_all()

@app.post("/api/create-agent")
async def create_agent(request: Request):
    """Create a new agent using the self-replicator"""
    try:
        agent_data = await request.json()
        
        # Create self-replicator agent
        agent = SelfReplicatorAgent("self_replicator", memory)
        
        # Run the agent to create a new agent
        result = agent.run(agent_data)
        
        return {
            "message": "Agent created successfully",
            "result": result
        }
    except Exception as e:
        print(f"Error creating agent: {str(e)}")
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Error creating agent: {str(e)}"
        )

@app.post("/api/agents/execute/{agent_name}")
async def execute_agent(agent_name: str, request: Request):
    """Execute an agent with the given input data"""
    try:
        # Parse request body
        input_data = await request.json()
        
        # Load the agent
        if agent_name == "self_replicator":
            agent = SelfReplicatorAgent("self_replicator", memory)
        elif agent_name == "project_architect":
            agent = ProjectArchitectAgent("project_architect", memory)
        else:
            # Try to dynamically import a custom agent
            try:
                module_name = f"agents.custom.{agent_name}"
                class_name = agent_name.title().replace('_', '') + 'Agent'
                
                module = __import__(module_name, fromlist=[class_name])
                agent_class = getattr(module, class_name)
                agent = agent_class(agent_name, memory)
            except Exception as e:
                print(f"Error loading agent {agent_name}: {str(e)}")
                traceback.print_exc()
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
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error executing agent {agent_name}: {str(e)}")
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Error executing agent: {str(e)}"
        )

# Run the server
if __name__ == "__main__":
    print("Starting Sankalpa Minimal API Server...")
    uvicorn.run(
        "minimal_api_server:app", 
        host="0.0.0.0", 
        port=8080, 
        reload=True,
        ws="none"  # Disable WebSockets support
    )