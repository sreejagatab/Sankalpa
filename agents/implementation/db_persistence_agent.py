
import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from typing import Dict, Any, Optional
import json

from agents.enhanced_base import EnhancedBaseAgent, ValidationError
from backend.db.database import db
from core import get_logger

logger = get_logger("agent.db_persistence")

class DbPersistenceAgent(EnhancedBaseAgent):
    """Agent for database persistence operations
    
    This agent provides functionality to store and retrieve data from
    the database, implementing database-backed memory for other agents.
    """
    
    def __init__(self, name: str = "db_persistence", **kwargs):
        super().__init__(name, **kwargs)
    
    def _execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute database persistence operations
        
        Args:
            input_data: Dictionary containing:
                - operation: Operation to perform (save, load, delete, query)
                - key: Key to save/load/delete (for save, load, delete operations)
                - value: Value to save (for save operation)
                - query: SQL query to execute (for query operation)
                - params: Parameters for SQL query (for query operation)
                - session_id: Optional session ID
                
        Returns:
            Result of the operation
            
        Raises:
            ValidationError: If input is invalid
            Exception: If operation fails
        """
        if "operation" not in input_data:
            raise ValidationError("Missing required field: operation")
            
        operation = input_data["operation"]
        
        if operation == "save":
            return self._save_operation(input_data)
        elif operation == "load":
            return self._load_operation(input_data)
        elif operation == "delete":
            return self._delete_operation(input_data)
        elif operation == "query":
            return self._query_operation(input_data)
        else:
            raise ValidationError(f"Invalid operation: {operation}")
    
    def _save_operation(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save a value to the database
        
        Args:
            input_data: Dictionary containing:
                - key: Key to save under
                - value: Value to save
                - session_id: Optional session ID
                
        Returns:
            Result of the save operation
        """
        if "key" not in input_data:
            raise ValidationError("Missing required field: key")
        if "value" not in input_data:
            raise ValidationError("Missing required field: value")
            
        key = input_data["key"]
        value = input_data["value"]
        session_id = input_data.get("session_id")
        
        if not db.available:
            logger.warning("Database not available. Falling back to memory storage.")
            # Store in memory
            self.memory[key] = value
            return {"success": True, "stored_in": "memory"}
        
        try:
            # Use raw SQL for flexibility
            query = """
            INSERT INTO memory_items (session_id, key, value)
            VALUES (%s, %s, %s)
            ON CONFLICT (session_id, key) DO UPDATE SET
                value = %s,
                updated_at = NOW()
            RETURNING id
            """
            
            # Convert value to JSON
            value_json = json.dumps(value)
            
            with db.session_scope() as session:
                result = session.execute(
                    query, 
                    (session_id, key, value_json, value_json)
                )
                item_id = result.fetchone()[0]
                
            return {
                "success": True,
                "stored_in": "database",
                "item_id": str(item_id)
            }
            
        except Exception as e:
            logger.error(f"Database save failed: {str(e)}")
            # Fall back to memory storage
            self.memory[key] = value
            return {
                "success": True,
                "stored_in": "memory",
                "error": str(e)
            }
    
    def _load_operation(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Load a value from the database
        
        Args:
            input_data: Dictionary containing:
                - key: Key to load
                - session_id: Optional session ID
                
        Returns:
            Result of the load operation
        """
        if "key" not in input_data:
            raise ValidationError("Missing required field: key")
            
        key = input_data["key"]
        session_id = input_data.get("session_id")
        
        # First check memory
        if key in self.memory:
            return {
                "success": True,
                "value": self.memory[key],
                "source": "memory"
            }
        
        if not db.available:
            logger.warning("Database not available. No value found in memory.")
            return {
                "success": False,
                "error": "Value not found and database not available"
            }
        
        try:
            query = """
            SELECT value FROM memory_items
            WHERE session_id = %s AND key = %s
            """
            
            with db.session_scope() as session:
                result = session.execute(query, (session_id, key))
                row = result.fetchone()
                
                if row is None:
                    return {
                        "success": False,
                        "error": "Value not found"
                    }
                    
                # Parse JSON value
                value = json.loads(row[0])
                
                # Cache in memory
                self.memory[key] = value
                
                return {
                    "success": True,
                    "value": value,
                    "source": "database"
                }
                
        except Exception as e:
            logger.error(f"Database load failed: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _delete_operation(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Delete a value from the database
        
        Args:
            input_data: Dictionary containing:
                - key: Key to delete
                - session_id: Optional session ID
                
        Returns:
            Result of the delete operation
        """
        if "key" not in input_data:
            raise ValidationError("Missing required field: key")
            
        key = input_data["key"]
        session_id = input_data.get("session_id")
        
        # Delete from memory
        memory_deleted = False
        if key in self.memory:
            del self.memory[key]
            memory_deleted = True
        
        if not db.available:
            logger.warning("Database not available. Only deleted from memory.")
            return {
                "success": memory_deleted,
                "deleted_from": "memory" if memory_deleted else None
            }
        
        try:
            query = """
            DELETE FROM memory_items
            WHERE session_id = %s AND key = %s
            RETURNING id
            """
            
            with db.session_scope() as session:
                result = session.execute(query, (session_id, key))
                row = result.fetchone()
                
                if row is None:
                    return {
                        "success": memory_deleted,
                        "deleted_from": "memory" if memory_deleted else None
                    }
                    
                return {
                    "success": True,
                    "deleted_from": "both" if memory_deleted else "database"
                }
                
        except Exception as e:
            logger.error(f"Database delete failed: {str(e)}")
            return {
                "success": memory_deleted,
                "deleted_from": "memory" if memory_deleted else None,
                "error": str(e)
            }
    
    def _query_operation(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a custom query against the database
        
        Args:
            input_data: Dictionary containing:
                - query: SQL query to execute
                - params: Optional parameters for SQL query
                
        Returns:
            Result of the query operation
        """
        if "query" not in input_data:
            raise ValidationError("Missing required field: query")
            
        query = input_data["query"]
        params = input_data.get("params", {})
        
        if not db.available:
            logger.error("Database not available. Cannot execute query.")
            return {
                "success": False,
                "error": "Database not available"
            }
        
        try:
            result = db.execute(query, params)
            
            # Convert results to list of dictionaries
            result_list = []
            for row in result:
                row_dict = {}
                for i, column in enumerate(result.keys()):
                    row_dict[column] = row[i]
                result_list.append(row_dict)
                
            return {
                "success": True,
                "results": result_list,
                "count": len(result_list)
            }
            
        except Exception as e:
            logger.error(f"Database query failed: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }