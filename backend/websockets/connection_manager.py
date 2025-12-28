
import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from typing import Dict, List, Any, Optional, Set
from fastapi import WebSocket, WebSocketDisconnect
import json
import asyncio
from datetime import datetime
import uuid
import logging

# For simplified testing, use built-in logging
logger = logging.getLogger("websockets")

class ConnectionManager:
    """Manager for WebSocket connections
    
    Handles WebSocket connections and message broadcasting for real-time
    collaboration features.
    """
    
    def __init__(self):
        # Map of room_id to set of WebSocket connections
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        
        # Map of connection_id to user info
        self.connection_info: Dict[str, Dict[str, Any]] = {}
        
        # Map of room_id to room metadata
        self.rooms: Dict[str, Dict[str, Any]] = {}
        
        logger.info("WebSocket connection manager initialized")
    
    async def connect(self, websocket: WebSocket, room_id: str, user_info: Dict[str, Any]) -> str:
        """Connect a WebSocket to a room
        
        Args:
            websocket: The WebSocket connection
            room_id: The room identifier
            user_info: Information about the connected user
            
        Returns:
            A unique connection ID
        """
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
        """Disconnect a WebSocket
        
        Args:
            websocket: The WebSocket connection
            connection_id: The connection identifier
        """
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
        """Broadcast a message to all connections in a room
        
        Args:
            room_id: The room identifier
            message: The message to broadcast
            exclude: Optional WebSocket to exclude from the broadcast
            
        Returns:
            Number of connections the message was sent to
        """
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
        """Send a message to a specific connection
        
        Args:
            websocket: The WebSocket connection
            message: The message to send
            
        Returns:
            True if the message was sent successfully
        """
        try:
            await websocket.send_text(json.dumps(message))
            return True
        except RuntimeError:
            return False
    
    def get_room_info(self, room_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a room
        
        Args:
            room_id: The room identifier
            
        Returns:
            Room information or None if room doesn't exist
        """
        if room_id not in self.rooms:
            return None
            
        return {
            **self.rooms[room_id],
            "user_count": len(self.active_connections[room_id]) if room_id in self.active_connections else 0
        }
    
    def get_connection_info(self, connection_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a connection
        
        Args:
            connection_id: The connection identifier
            
        Returns:
            Connection information or None if connection doesn't exist
        """
        return self.connection_info.get(connection_id)
    
    def get_active_rooms(self) -> List[Dict[str, Any]]:
        """Get a list of active rooms
        
        Returns:
            List of room information
        """
        return [
            {
                "room_id": room_id,
                **self.get_room_info(room_id)
            }
            for room_id in self.rooms
        ]
    
    def set_room_metadata(self, room_id: str, metadata: Dict[str, Any]) -> bool:
        """Set metadata for a room
        
        Args:
            room_id: The room identifier
            metadata: The metadata to set
            
        Returns:
            True if the metadata was set, False if room doesn't exist
        """
        if room_id not in self.rooms:
            return False
            
        self.rooms[room_id]["metadata"] = {
            **self.rooms[room_id].get("metadata", {}),
            **metadata
        }
        
        return True

# Global connection manager instance
connection_manager = ConnectionManager()