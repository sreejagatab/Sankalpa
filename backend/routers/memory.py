
import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel

from core import get_logger
from core.security import get_current_user
from memory.enhanced_memory_manager import EnhancedMemoryManager

# Initialize router
router = APIRouter()
logger = get_logger("api.memory")

# Memory manager
memory_manager = EnhancedMemoryManager()

# Pydantic models
class MemoryItem(BaseModel):
    key: str
    value: Any

class MemoryItemsList(BaseModel):
    items: Dict[str, Any]
    session_id: str

class MemorySessionsList(BaseModel):
    sessions: List[str]

class MemorySaveRequest(BaseModel):
    key: str
    value: Any
    session_id: Optional[str] = None

class MemoryLoadRequest(BaseModel):
    key: str
    session_id: Optional[str] = None

class MemoryDeleteRequest(BaseModel):
    key: str
    session_id: Optional[str] = None

# Routes
@router.get("/sessions", response_model=MemorySessionsList)
async def list_sessions(current_user = Depends(get_current_user)):
    """List all memory sessions"""
    sessions = memory_manager.list_sessions()
    return {"sessions": sessions}

@router.get("/items", response_model=MemoryItemsList)
async def list_memory_items(
    session_id: Optional[str] = Query(None, description="Memory session ID"),
    current_user = Depends(get_current_user)
):
    """List all memory items in a session"""
    items = memory_manager.get_all(session_id)
    return {
        "items": items,
        "session_id": session_id or memory_manager.current_session
    }

@router.post("/save", response_model=MemoryItem)
async def save_memory_item(request: MemorySaveRequest, current_user = Depends(get_current_user)):
    """Save a value to memory"""
    try:
        memory_manager.save(request.key, request.value, request.session_id)
        return {"key": request.key, "value": request.value}
    except Exception as e:
        logger.error(f"Failed to save memory item: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save memory item: {str(e)}"
        )

@router.post("/load", response_model=MemoryItem)
async def load_memory_item(request: MemoryLoadRequest, current_user = Depends(get_current_user)):
    """Load a value from memory"""
    value = memory_manager.load(request.key, None, request.session_id)
    if value is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Memory item not found: {request.key}"
        )
    return {"key": request.key, "value": value}

@router.post("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_memory_item(request: MemoryDeleteRequest, current_user = Depends(get_current_user)):
    """Delete a value from memory"""
    success = memory_manager.delete(request.key, request.session_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Memory item not found: {request.key}"
        )
    return None