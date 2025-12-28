import os
import pytest
import json
import uuid

from memory.enhanced_memory_manager import (
    EnhancedMemoryManager,
    MemoryStorageError,
    MemoryTransactionError
)

def test_init():
    """Test memory manager initialization"""
    memory = EnhancedMemoryManager()
    assert memory.session_data == {}
    assert memory.current_session is not None

def test_save_and_load():
    """Test saving and loading data"""
    memory = EnhancedMemoryManager()

    # Save some data
    memory.save("test_key", {"value": "test_value"})

    # Load the data
    result = memory.load("test_key")
    assert result == {"value": "test_value"}

    # Check that it was saved to disk
    session_path = memory._get_session_path()
    assert os.path.exists(session_path)

    with open(session_path, "r") as f:
        data = json.load(f)
        assert "test_key" in data
        assert data["test_key"] == {"value": "test_value"}

def test_get_all():
    """Test getting all data"""
    memory = EnhancedMemoryManager()

    # Save multiple items
    memory.save("key1", "value1")
    memory.save("key2", "value2")

    # Get all data
    all_data = memory.get_all()
    assert "key1" in all_data
    assert "key2" in all_data
    assert all_data["key1"] == "value1"
    assert all_data["key2"] == "value2"

def test_delete():
    """Test deleting data"""
    memory = EnhancedMemoryManager()

    # Save and then delete
    memory.save("delete_me", "value")
    assert memory.load("delete_me") == "value"

    success = memory.delete("delete_me")
    assert success is True
    assert memory.load("delete_me") is None

def test_transaction():
    """Test transaction context manager"""
    memory = EnhancedMemoryManager()

    # Use transaction to save multiple items
    with memory.transaction() as tx:
        tx.save("tx_key1", "tx_value1")
        tx.save("tx_key2", "tx_value2")

    # Verify items were saved
    assert memory.load("tx_key1") == "tx_value1"
    assert memory.load("tx_key2") == "tx_value2"

def test_transaction_rollback():
    """Test transaction rollback on exception"""
    memory = EnhancedMemoryManager()

    # Add some initial data
    memory.save("existing", "value")

    # Transaction that raises an exception
    try:
        with memory.transaction() as tx:
            tx.save("should_not_exist", "value")
            raise ValueError("Test exception")
    except ValueError:
        pass

    # Verify the transaction was rolled back
    assert memory.load("should_not_exist") is None
    assert memory.load("existing") == "value"  # Original data still exists

def test_multiple_sessions():
    """Test using multiple sessions"""
    memory = EnhancedMemoryManager()

    # Create unique session IDs
    session1 = str(uuid.uuid4())
    session2 = str(uuid.uuid4())

    # Save data to different sessions
    memory.save("key", "value1", session_id=session1)
    memory.save("key", "value2", session_id=session2)

    # Load data from specific sessions
    assert memory.load("key", session_id=session1) == "value1"
    assert memory.load("key", session_id=session2) == "value2"

    # Switch sessions
    memory.switch_session(session1)
    assert memory.load("key") == "value1"

    memory.switch_session(session2)
    assert memory.load("key") == "value2"

def test_list_sessions():
    """Test listing available sessions"""
    memory = EnhancedMemoryManager()

    # Create a few sessions
    session1 = str(uuid.uuid4())
    session2 = str(uuid.uuid4())

    memory.save("key", "value1", session_id=session1)
    memory.save("key", "value2", session_id=session2)

    # List sessions
    sessions = memory.list_sessions()
    assert session1 in sessions
    assert session2 in sessions

def test_backup_restore():
    """Test backup and restore functionality"""
    memory = EnhancedMemoryManager()

    # Save initial data
    memory.save("original", "value")

    # Create backup
    backup_file = memory._create_backup()
    assert os.path.exists(backup_file)

    # Modify data
    memory.save("original", "new_value")
    assert memory.load("original") == "new_value"

    # Restore from backup
    success = memory._restore_from_backup(backup_file)
    assert success is True
    assert memory.load("original") == "value"  # Original value restored

    # Clean up
    if os.path.exists(backup_file):
        os.remove(backup_file)