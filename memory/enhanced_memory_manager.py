
import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
import json
import os
import shutil
import time
import uuid
from pathlib import Path
from typing import Dict, Any, Optional, Union

from core import get_logger

logger = get_logger("memory")

class MemoryException(Exception):
    """Base exception for memory operations"""
    pass

class MemoryStorageError(MemoryException):
    """Raised when memory storage operations fail"""
    pass

class MemoryTransactionError(MemoryException):
    """Raised when a memory transaction fails"""
    pass

class EnhancedMemoryManager:
    """Enhanced memory manager with transaction support and error handling"""
    
    def __init__(self, base_path: str = "memory/sessions", default_session: Optional[str] = None):
        """Initialize the memory manager
        
        Args:
            base_path: Base directory for memory storage
            default_session: Default session ID (will create if not exists)
        """
        self.base_path = base_path
        self.current_session = default_session or str(uuid.uuid4())
        self.session_data: Dict[str, Any] = {}
        self.backup_path = f"{base_path}/.backup"
        
        # Ensure directories exist
        Path(self.base_path).mkdir(parents=True, exist_ok=True)
        Path(self.backup_path).mkdir(parents=True, exist_ok=True)
        
        # Load session if it exists
        self._load_session()
        
        logger.info(f"Memory manager initialized with session: {self.current_session}")
    
    def _get_session_path(self, session_id: Optional[str] = None) -> str:
        """Get the path for a session file"""
        sid = session_id or self.current_session
        return os.path.join(self.base_path, f"{sid}.json")
    
    def _load_session(self) -> None:
        """Load the current session from disk"""
        session_path = self._get_session_path()
        
        try:
            if os.path.exists(session_path):
                with open(session_path, "r") as f:
                    self.session_data = json.load(f)
                logger.debug(f"Loaded session {self.current_session}")
            else:
                self.session_data = {}
                logger.debug(f"Created new session {self.current_session}")
        except Exception as e:
            logger.error(f"Failed to load session {self.current_session}: {str(e)}")
            self.session_data = {}
    
    def _create_backup(self) -> str:
        """Create a backup of the current session
        
        Returns:
            Path to the backup file
        """
        session_path = self._get_session_path()
        if not os.path.exists(session_path):
            return ""
            
        backup_id = str(uuid.uuid4())
        backup_file = os.path.join(self.backup_path, f"{self.current_session}_{backup_id}.json")
        
        try:
            shutil.copy2(session_path, backup_file)
            logger.debug(f"Created backup: {backup_file}")
            return backup_file
        except Exception as e:
            logger.warning(f"Failed to create backup: {str(e)}")
            return ""
    
    def _restore_from_backup(self, backup_file: str) -> bool:
        """Restore session from a backup file
        
        Args:
            backup_file: Path to the backup file
            
        Returns:
            True if restore was successful
        """
        if not backup_file or not os.path.exists(backup_file):
            logger.error("No valid backup file provided for restore")
            return False
            
        session_path = self._get_session_path()
        
        try:
            shutil.copy2(backup_file, session_path)
            self._load_session()
            logger.info(f"Restored from backup: {backup_file}")
            return True
        except Exception as e:
            logger.error(f"Failed to restore from backup: {str(e)}")
            return False
    
    def _atomic_write(self) -> bool:
        """Write session data to disk atomically
        
        Returns:
            True if write was successful
        """
        session_path = self._get_session_path()
        temp_path = f"{session_path}.tmp"
        
        try:
            with open(temp_path, "w") as f:
                json.dump(self.session_data, f, indent=2)
                
            # Atomic rename
            os.replace(temp_path, session_path)
            logger.debug(f"Session {self.current_session} saved")
            return True
        except Exception as e:
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except:
                    pass
            logger.error(f"Failed to save session {self.current_session}: {str(e)}")
            return False
    
    def save(self, key: str, value: Any, session_id: Optional[str] = None) -> bool:
        """Save a value to memory
        
        Args:
            key: Key to store the value under
            value: Value to store
            session_id: Optional session ID (uses current if not provided)
            
        Returns:
            True if save was successful
            
        Raises:
            MemoryStorageError: If the save operation fails
        """
        if session_id and session_id != self.current_session:
            # Saving to a different session
            other_manager = EnhancedMemoryManager(self.base_path, session_id)
            return other_manager.save(key, value)
        
        # Create backup before modification
        backup_file = self._create_backup()
        
        try:
            self.session_data[key] = value
            if not self._atomic_write():
                if backup_file:
                    self._restore_from_backup(backup_file)
                raise MemoryStorageError(f"Failed to save value for key: {key}")
            return True
        except Exception as e:
            logger.error(f"Save operation failed: {str(e)}")
            if backup_file:
                self._restore_from_backup(backup_file)
            raise MemoryStorageError(f"Error saving value: {str(e)}")
    
    def load(self, key: str, default: Any = None, session_id: Optional[str] = None) -> Any:
        """Load a value from memory
        
        Args:
            key: Key to retrieve
            default: Default value if key not found
            session_id: Optional session ID (uses current if not provided)
            
        Returns:
            The stored value or default if not found
        """
        if session_id and session_id != self.current_session:
            # Loading from a different session
            other_manager = EnhancedMemoryManager(self.base_path, session_id)
            return other_manager.load(key, default)
        
        try:
            return self.session_data.get(key, default)
        except Exception as e:
            logger.error(f"Load operation failed for key {key}: {str(e)}")
            return default
    
    def delete(self, key: str, session_id: Optional[str] = None) -> bool:
        """Delete a value from memory
        
        Args:
            key: Key to delete
            session_id: Optional session ID (uses current if not provided)
            
        Returns:
            True if delete was successful
        """
        if session_id and session_id != self.current_session:
            # Deleting from a different session
            other_manager = EnhancedMemoryManager(self.base_path, session_id)
            return other_manager.delete(key)
        
        # Create backup before modification
        backup_file = self._create_backup()
        
        try:
            if key in self.session_data:
                del self.session_data[key]
                if not self._atomic_write():
                    if backup_file:
                        self._restore_from_backup(backup_file)
                    return False
                return True
            return False
        except Exception as e:
            logger.error(f"Delete operation failed for key {key}: {str(e)}")
            if backup_file:
                self._restore_from_backup(backup_file)
            return False
    
    def get_all(self, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Get all values in the session
        
        Args:
            session_id: Optional session ID (uses current if not provided)
            
        Returns:
            Dictionary of all values
        """
        if session_id and session_id != self.current_session:
            # Getting from a different session
            other_manager = EnhancedMemoryManager(self.base_path, session_id)
            return other_manager.get_all()
        
        return self.session_data.copy()
    
    def list_sessions(self) -> list:
        """List all available sessions
        
        Returns:
            List of session IDs
        """
        sessions = []
        for file in os.listdir(self.base_path):
            if file.endswith(".json") and not file.startswith("."):
                sessions.append(file.replace(".json", ""))
        return sessions
    
    def switch_session(self, session_id: str) -> bool:
        """Switch to a different session
        
        Args:
            session_id: Session ID to switch to
            
        Returns:
            True if switch was successful
        """
        self.current_session = session_id
        self._load_session()
        return True
    
    def transaction(self):
        """Create a memory transaction context manager
        
        Returns:
            Transaction context manager
        """
        return MemoryTransaction(self)


class MemoryTransaction:
    """Transaction context manager for memory operations"""
    
    def __init__(self, memory_manager: EnhancedMemoryManager):
        self.memory_manager = memory_manager
        self.backup_file = None
        self.changes = {}
        
    def __enter__(self):
        """Start the transaction"""
        self.backup_file = self.memory_manager._create_backup()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """End the transaction"""
        if exc_type is not None:
            # Exception occurred, restore from backup
            if self.backup_file:
                self.memory_manager._restore_from_backup(self.backup_file)
            return False
        
        # Commit all changes
        try:
            for key, value in self.changes.items():
                self.memory_manager.session_data[key] = value
                
            if not self.memory_manager._atomic_write():
                if self.backup_file:
                    self.memory_manager._restore_from_backup(self.backup_file)
                raise MemoryTransactionError("Failed to commit transaction")
                
            return True
        except Exception as e:
            logger.error(f"Transaction failed: {str(e)}")
            if self.backup_file:
                self.memory_manager._restore_from_backup(self.backup_file)
            return False
    
    def save(self, key: str, value: Any) -> None:
        """Stage a save operation in the transaction"""
        self.changes[key] = value
    
    def delete(self, key: str) -> None:
        """Stage a delete operation in the transaction"""
        self.changes[key] = None  # Mark for deletion
        
    def commit(self) -> bool:
        """Manually commit the transaction
        
        Returns:
            True if commit was successful
        """
        try:
            for key, value in self.changes.items():
                if value is None:
                    # Delete operation
                    if key in self.memory_manager.session_data:
                        del self.memory_manager.session_data[key]
                else:
                    # Save operation
                    self.memory_manager.session_data[key] = value
                    
            if not self.memory_manager._atomic_write():
                if self.backup_file:
                    self.memory_manager._restore_from_backup(self.backup_file)
                return False
                
            return True
        except Exception as e:
            logger.error(f"Manual transaction commit failed: {str(e)}")
            if self.backup_file:
                self.memory_manager._restore_from_backup(self.backup_file)
            return False