from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query, BackgroundTasks, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import json
import uuid
from datetime import datetime
from typing import Dict, Any, Optional, Set, List
import logging
import importlib
import inspect
import os
import sys

# Add project root to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sankalpa-server")

app = FastAPI(
    title="Sankalpa Development Server",
    description="Development server for the Sankalpa multi-agent platform",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simplified connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        self.connection_info: Dict[str, Dict[str, Any]] = {}
        self.rooms: Dict[str, Dict[str, Any]] = {}
        logger.info("WebSocket connection manager initialized")
    
    async def connect(self, websocket: WebSocket, room_id: str, user_info: Dict[str, Any]) -> str:
        await websocket.accept()
        
        # Create room if it doesn't exist
        if room_id not in self.active_connections:
            self.active_connections[room_id] = set()
            self.rooms[room_id] = {
                "created_at": datetime.utcnow().isoformat(),
                "user_count": 0,
                "metadata": {}
            }
            logger.info(f"Created new room: {room_id}")
        
        # Add connection to room
        self.active_connections[room_id].add(websocket)
        
        # Generate unique connection ID
        connection_id = str(uuid.uuid4())
        
        # Store connection info
        self.connection_info[connection_id] = {
            "user": user_info,
            "room_id": room_id,
            "connected_at": datetime.utcnow().isoformat()
        }
        
        # Update room stats
        self.rooms[room_id]["user_count"] = len(self.active_connections[room_id])
        
        # Notify room about new user
        await self.broadcast_to_room(
            room_id,
            {
                "type": "user_joined",
                "user": user_info,
                "timestamp": datetime.utcnow().isoformat(),
                "room_id": room_id,
                "user_count": self.rooms[room_id]["user_count"]
            },
            exclude=websocket
        )
        
        logger.info(f"Client connected: {connection_id} to room: {room_id}")
        return connection_id
    
    async def disconnect(self, websocket: WebSocket, connection_id: str) -> None:
        # Get connection info
        if connection_id not in self.connection_info:
            logger.warning(f"Unknown connection ID for disconnection: {connection_id}")
            return
            
        info = self.connection_info[connection_id]
        room_id = info["room_id"]
        user_info = info["user"]
        
        # Remove from active connections
        if room_id in self.active_connections:
            self.active_connections[room_id].discard(websocket)
            
            # Update room stats
            self.rooms[room_id]["user_count"] = len(self.active_connections[room_id])
            
            # Clean up empty rooms
            if len(self.active_connections[room_id]) == 0:
                del self.active_connections[room_id]
                del self.rooms[room_id]
                logger.info(f"Removed empty room: {room_id}")
            else:
                # Notify room about user leaving
                await self.broadcast_to_room(
                    room_id,
                    {
                        "type": "user_left",
                        "user": user_info,
                        "timestamp": datetime.utcnow().isoformat(),
                        "room_id": room_id,
                        "user_count": self.rooms[room_id]["user_count"]
                    }
                )
        
        # Remove connection info
        if connection_id in self.connection_info:
            del self.connection_info[connection_id]
            
        logger.info(f"Client disconnected: {connection_id} from room: {room_id}")
    
    async def broadcast_to_room(
        self, room_id: str, message: Dict[str, Any], exclude: Optional[WebSocket] = None
    ) -> int:
        if room_id not in self.active_connections:
            return 0
            
        # Convert message to JSON
        json_message = json.dumps(message)
        
        # Track successful sends
        sent_count = 0
        dead_connections = set()
        
        # Send to all connections in room
        for connection in self.active_connections[room_id]:
            if exclude and connection == exclude:
                continue
                
            try:
                await connection.send_text(json_message)
                sent_count += 1
            except RuntimeError:
                # Connection is dead, mark for removal
                dead_connections.add(connection)
        
        # Clean up dead connections
        for dead in dead_connections:
            self.active_connections[room_id].discard(dead)
            
        # Update room stats after cleanup
        if room_id in self.rooms:
            self.rooms[room_id]["user_count"] = len(self.active_connections[room_id])
            
        return sent_count
    
    async def send_personal_message(self, websocket: WebSocket, message: Dict[str, Any]) -> bool:
        try:
            await websocket.send_text(json.dumps(message))
            return True
        except RuntimeError:
            return False
    
    def get_room_info(self, room_id: str) -> Optional[Dict[str, Any]]:
        if room_id not in self.rooms:
            return None
            
        return {
            **self.rooms[room_id],
            "user_count": len(self.active_connections[room_id]) if room_id in self.active_connections else 0
        }
    
    def get_active_rooms(self) -> List[Dict[str, Any]]:
        return [
            {
                "room_id": room_id,
                **self.get_room_info(room_id)
            }
            for room_id in self.rooms
        ]

# Create connection manager instance
manager = ConnectionManager()

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
            with open(self.filename, "r") as f:
                self.memory = json.load(f)

# Create memory manager
memory = MemoryManager()

def load_agent(agent_name: str, module_prefix: str = "agents"):
    try:
        # First, check if it's a core agent
        module_name = f"{module_prefix}.{agent_name}"
        
        try:
            # Try direct import
            module = importlib.import_module(module_name)
        except ImportError:
            # It might be in a subdirectory - check catalog
            catalog_path = "catalog/agent_catalog.json"
            if os.path.exists(catalog_path):
                with open(catalog_path, "r") as f:
                    catalog = json.load(f)
                
                if agent_name in catalog:
                    module_path = catalog[agent_name].get("module", "")
                    if module_path:
                        module_name = f"{module_prefix}.{module_path}"
                        module = importlib.import_module(module_name)
                    else:
                        raise ImportError(f"No module path in catalog for {agent_name}")
                else:
                    raise ImportError(f"Agent {agent_name} not found in catalog")
            else:
                raise ImportError(f"Agent catalog not found and agent {agent_name} not importable directly")
        
        # Get the agent class
        class_name = agent_name.title().replace('_', '') + 'Agent'
        agent_class = getattr(module, class_name)
        
        # Check if it's a subclass of BaseAgent
        from agents.base import BaseAgent
        if not issubclass(agent_class, BaseAgent):
            logger.warning(f"Class {class_name} is not a subclass of BaseAgent")
            
        # Create and return an instance of the agent
        return agent_class(agent_name, memory=memory)
    except Exception as e:
        logger.error(f"Error loading agent {agent_name}: {str(e)}")
        return None

@app.get("/")
async def root():
    return {"message": "Sankalpa Development Server is running!"}

@app.get("/api/status")
async def status():
    return {"status": "Sankalpa Development Server is running!", "version": "0.1.0"}

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

@app.websocket("/ws/collaboration/{room_id}")
async def websocket_collaboration(
    websocket: WebSocket,
    room_id: str,
    token: Optional[str] = Query(None)
):
    # Simple mock authentication
    user_info = {"id": "anon-" + str(uuid.uuid4())[:8], "username": "Anonymous"}
    
    if token:
        # Just use the token as the user ID for this demo
        user_info = {"id": token, "username": f"User-{token[:5]}"}
    
    # Connect to room
    connection_id = await manager.connect(websocket, room_id, user_info)
    
    # Send room info to the user
    room_info = manager.get_room_info(room_id)
    await manager.send_personal_message(
        websocket,
        {
            "type": "room_info",
            "room_id": room_id,
            "user_count": room_info["user_count"],
            "metadata": room_info.get("metadata", {}),
            "connection_id": connection_id
        }
    )
    
    try:
        # Handle messages
        while True:
            data = await websocket.receive_text()
            
            try:
                message = json.loads(data)
                
                # Validate message
                if not isinstance(message, dict) or "type" not in message:
                    continue
                
                # Add user info to message
                message["user"] = user_info
                
                # Handle message based on type
                if message["type"] == "chat":
                    # Add timestamp if not present
                    if "timestamp" not in message:
                        message["timestamp"] = datetime.utcnow().isoformat()
                    # Chat messages are broadcasted to the room
                    await manager.broadcast_to_room(room_id, message)
                
                elif message["type"] == "ping":
                    # Ping messages are replied to directly
                    await manager.send_personal_message(
                        websocket,
                        {
                            "type": "pong",
                            "timestamp": message.get("timestamp", datetime.utcnow().isoformat())
                        }
                    )
                    
            except Exception as e:
                logger.error(f"Error processing message: {str(e)}")
                # Send error message to client
                await manager.send_personal_message(
                    websocket,
                    {
                        "type": "error",
                        "message": "Failed to process message",
                        "error": str(e)
                    }
                )
                
    except WebSocketDisconnect:
        await manager.disconnect(websocket, connection_id)
    
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        await manager.disconnect(websocket, connection_id)

@app.get("/api/rooms")
async def get_active_rooms():
    rooms = manager.get_active_rooms()
    return {
        "rooms": rooms,
        "count": len(rooms)
    }

@app.get("/api/memory")
async def get_memory():
    """Get all memory data"""
    return memory.get_all()

# Run the server
if __name__ == "__main__":
    uvicorn.run("minimal_server:app", host="0.0.0.0", port=8080, reload=True)