import os
import sys
import importlib
import json
import uuid
from datetime import datetime
import traceback

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# Create FastAPI app
app = FastAPI(
    title="Sankalpa Simple Server",
    description="Simple server for the Sankalpa multi-agent platform",
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

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = datetime.utcnow()
    
    try:
        response = await call_next(request)
        
        # Calculate processing time
        process_time = (datetime.utcnow() - start_time).total_seconds()
        
        # Log request details
        print(f"[{datetime.utcnow()}] {request.method} {request.url.path} - {response.status_code} ({process_time:.4f}s)")
        
        return response
    except Exception as e:
        # Log error
        print(f"[{datetime.utcnow()}] ERROR {request.method} {request.url.path} - {str(e)}")
        print(traceback.format_exc())
        
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
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
            except Exception:
                self.memory = {}

# Create memory manager
memory = MemoryManager()

class AgentLoader:
    @staticmethod
    def load_agent(agent_name, memory_manager=None):
        """Load an agent by name"""
        try:
            # Determine the module path
            if '.' in agent_name:
                # Handle direct module paths like "enhanced.self_replicator"
                module_name = f"agents.{agent_name}"
                class_name = agent_name.split('.')[-1].title().replace('_', '') + 'Agent'
            else:
                # Check catalog first
                catalog_path = "catalog/agent_catalog.json"
                if os.path.exists(catalog_path):
                    with open(catalog_path, "r") as f:
                        catalog = json.load(f)
                    
                    if agent_name in catalog:
                        module_path = catalog[agent_name].get("module", "")
                        if module_path:
                            module_name = f"agents.{module_path}"
                            class_name = agent_name.title().replace('_', '') + 'Agent'
                        else:
                            # Try to guess based on the agent name
                            module_name = f"agents.{agent_name}"
                            class_name = agent_name.title().replace('_', '') + 'Agent'
                    else:
                        # Try to guess based on common locations
                        for folder in ["builder", "testing", "enhanced", "deployment", "marketing", "custom"]:
                            try:
                                module_name = f"agents.{folder}.{agent_name}"
                                module = importlib.import_module(module_name)
                                class_name = agent_name.title().replace('_', '') + 'Agent'
                                break
                            except ImportError:
                                continue
                        else:
                            # Fall back to direct module path
                            module_name = f"agents.{agent_name}"
                            class_name = agent_name.title().replace('_', '') + 'Agent'
                else:
                    # No catalog, just guess
                    module_name = f"agents.{agent_name}"
                    class_name = agent_name.title().replace('_', '') + 'Agent'
            
            # Import the module
            print(f"Loading module: {module_name}")
            module = importlib.import_module(module_name)
            
            # Get the agent class and create an instance
            print(f"Creating agent: {class_name}")
            agent_class = getattr(module, class_name)
            return agent_class(agent_name, memory=memory_manager or memory)
            
        except Exception as e:
            print(f"Error loading agent {agent_name}: {str(e)}")
            print(traceback.format_exc())
            return None

# API endpoints
@app.get("/")
async def root():
    return {"message": "Sankalpa Simple Server is running!"}

@app.get("/api/status")
async def status():
    return {"status": "Sankalpa Simple Server is running!", "version": "0.1.0"}

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

@app.get("/api/memory")
async def get_memory():
    """Get all memory data"""
    return memory.get_all()

@app.post("/api/agents/execute/{agent_name}")
async def execute_agent(agent_name: str, request: Request):
    """Execute an agent with the given input data"""
    try:
        # Parse request body
        input_data = await request.json()
        
        # Load the agent
        agent = AgentLoader.load_agent(agent_name)
        
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
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error executing agent {agent_name}: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Error executing agent: {str(e)}"
        )

@app.post("/api/create-agent")
async def create_agent(request: Request):
    """Create a new agent using the self-replicator"""
    try:
        # Parse request body
        agent_data = await request.json()
        
        # Load the self-replicator agent
        agent = AgentLoader.load_agent("enhanced.self_replicator")
        
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
        print(f"Error creating agent: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Error creating agent: {str(e)}"
        )

# Run the server
if __name__ == "__main__":
    print("Starting Sankalpa Simple Server...")
    uvicorn.run(
        "simple_server:app", 
        host="0.0.0.0", 
        port=8080, 
        reload=True,
        ws="none"  # Don't use websockets
    )