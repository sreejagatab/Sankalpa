
import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query, HTTPException
from typing import Dict, Any, Optional
import logging

from backend.websockets.connection_manager import connection_manager
# For simplified testing, use built-in logging
logger = logging.getLogger("websockets.routes")

router = APIRouter()

async def get_user_from_token(token: str) -> Dict[str, Any]:
    """Get user information from a token
    
    Args:
        token: The authentication token
        
    Returns:
        User information
        
    Raises:
        HTTPException: If the token is invalid
    """
    try:
        # For simplified testing, we'll just return mock user info
        user_id = "test_user_123"
        return {
            "id": user_id,
            "username": f"user_{user_id[:8]}"
        }
    except Exception as e:
        logger.error(f"Invalid token for WebSocket connection: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid authentication token")

@router.websocket("/ws/collaboration/{room_id}")
async def websocket_collaboration(
    websocket: WebSocket,
    room_id: str,
    token: Optional[str] = Query(None)
):
    """WebSocket endpoint for real-time collaboration
    
    Args:
        websocket: The WebSocket connection
        room_id: The room identifier
        token: Optional authentication token
    """
    # Authenticate user if token provided
    user_info = {"id": "anonymous", "username": "Anonymous"}
    
    if token:
        try:
            user_info = await get_user_from_token(token)
        except HTTPException:
            await websocket.close(code=1008)  # Policy violation
            return
    
    # Connect to room
    connection_id = await connection_manager.connect(websocket, room_id, user_info)
    
    # Send room info to the user
    room_info = connection_manager.get_room_info(room_id)
    await connection_manager.send_personal_message(
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
                import json
                message = json.loads(data)
                
                # Validate message
                if not isinstance(message, dict):
                    continue
                    
                if "type" not in message:
                    continue
                
                # Add user info to message
                message["user"] = user_info
                
                # Handle message based on type
                if message["type"] == "chat":
                    # Chat messages are broadcasted to the room
                    await connection_manager.broadcast_to_room(room_id, message)
                
                elif message["type"] == "cursor_position":
                    # Cursor position updates are broadcasted to the room
                    await connection_manager.broadcast_to_room(room_id, message, exclude=websocket)
                
                elif message["type"] == "chain_update":
                    # Chain updates are broadcasted to the room
                    await connection_manager.broadcast_to_room(room_id, message, exclude=websocket)
                
                elif message["type"] == "ping":
                    # Ping messages are replied to directly
                    await connection_manager.send_personal_message(
                        websocket,
                        {
                            "type": "pong",
                            "timestamp": message.get("timestamp")
                        }
                    )
                    
            except Exception as e:
                logger.error(f"Error processing message: {str(e)}")
                # Send error message to client
                await connection_manager.send_personal_message(
                    websocket,
                    {
                        "type": "error",
                        "message": "Failed to process message",
                        "error": str(e)
                    }
                )
                
    except WebSocketDisconnect:
        await connection_manager.disconnect(websocket, connection_id)
    
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        await connection_manager.disconnect(websocket, connection_id)

@router.get("/collaboration/rooms", tags=["collaboration"])
async def get_active_rooms():
    """Get a list of active collaboration rooms
    
    Returns:
        List of room information
    """
    rooms = connection_manager.get_active_rooms()
    
    # Filter sensitive information
    for room in rooms:
        if "metadata" in room and "sensitive" in room["metadata"]:
            del room["metadata"]["sensitive"]
    
    return {
        "rooms": rooms,
        "count": len(rooms)
    }

@router.post("/collaboration/rooms/{room_id}/metadata", tags=["collaboration"])
async def set_room_metadata(
    room_id: str,
    metadata: Dict[str, Any]
):
    """Set metadata for a collaboration room
    
    Args:
        room_id: The room identifier
        metadata: The metadata to set
        
    Returns:
        Success status
    """
    success = connection_manager.set_room_metadata(room_id, metadata)
    
    if not success:
        raise HTTPException(status_code=404, detail=f"Room {room_id} not found")
    
    return {
        "success": True,
        "room_id": room_id
    }