import pytest
from fastapi.testclient import TestClient
from fastapi import WebSocket, WebSocketDisconnect
import json
import asyncio
from unittest.mock import Mock, patch

from backend.main import app
from backend.websockets.connection_manager import ConnectionManager

# Mock WebSocket client for testing
class MockWebSocket:
    def __init__(self):
        self.sent_messages = []
        self.closed = False
        self.close_code = None

    async def accept(self):
        pass

    async def send_text(self, data):
        self.sent_messages.append(data)

    async def close(self, code=1000):
        self.closed = True
        self.close_code = code

def test_connection_manager():
    """Test the WebSocket ConnectionManager"""
    # Create connection manager
    manager = ConnectionManager()

    # Create mock websockets and user info
    ws1 = MockWebSocket()
    ws2 = MockWebSocket()
    user1 = {"id": "user1", "username": "User 1"}
    user2 = {"id": "user2", "username": "User 2"}

    # Test connecting to room
    async def test_connect():
        # Connect first user
        room_id = "test-room"
        conn_id1 = await manager.connect(ws1, room_id, user1)
        assert conn_id1 is not None
        assert room_id in manager.active_connections
        assert ws1 in manager.active_connections[room_id]
        assert conn_id1 in manager.connection_info

        # Connect second user
        conn_id2 = await manager.connect(ws2, room_id, user2)
        assert conn_id2 is not None
        assert len(manager.active_connections[room_id]) == 2

        # Test broadcasting message
        message = {"type": "chat", "message": "Hello!", "user": user1}
        sent = await manager.broadcast_to_room(room_id, message)
        assert sent == 2  # Both clients should receive the message

        # Test personal message
        personal_msg = {"type": "ping", "timestamp": "2023-01-01T00:00:00Z"}
        result = await manager.send_personal_message(ws1, personal_msg)
        assert result is True
        assert len(ws1.sent_messages) == 2  # Connect notification + personal message

        # Test disconnecting
        await manager.disconnect(ws1, conn_id1)
        assert len(manager.active_connections[room_id]) == 1
        assert conn_id1 not in manager.connection_info

        # Disconnect last user should remove room
        await manager.disconnect(ws2, conn_id2)
        assert room_id not in manager.active_connections
        assert room_id not in manager.rooms

    # Run the async test
    asyncio.run(test_connect())

@pytest.mark.asyncio
async def test_websocket_endpoint(monkeypatch):
    """Test the WebSocket collaboration endpoint"""

    # Create mock for token authentication
    async def mock_get_user_from_token(token):
        if token == "valid_token":
            return {"id": "test_user", "username": "Test User"}
        raise ValueError("Invalid token")

    # Mock the authentication function
    monkeypatch.setattr(
        "backend.websockets.routes.get_user_from_token",
        mock_get_user_from_token
    )

    # Mock WebSocket connection
    client = TestClient(app)

    # This test verifies the route exists but doesn't test full WebSocket functionality
    # since TestClient doesn't fully support WebSockets
    with client.websocket_connect("/ws/collaboration/test-room?token=valid_token") as websocket:
        # Test basic connection
        # In a real test, we would send and receive messages
        pass

def test_active_rooms_api():
    """Test the active rooms API endpoint"""
    client = TestClient(app)

    # Mock authentication
    with patch("backend.websockets.routes.get_current_user", return_value={"id": "user1"}):
        response = client.get("/collaboration/rooms")
        assert response.status_code == 200
        data = response.json()
        assert "rooms" in data
        assert "count" in data

def test_frontend_websocket_provider():
    """Test the React WebSocketProvider component (mock test)"""
    # This would be a frontend test using a tool like React Testing Library
    # For demonstration purposes, we're just outlining what would be tested

    # Test WebSocketProvider renders without errors
    # Test useWebSocket hook provides expected context
    # Test connection state management
    # Test sendMessage functionality
    # Test joinRoom and leaveRoom functions

    pass  # Actual implementation would require frontend testing setup

def test_frontend_collaboration_panel():
    """Test the React CollaborationPanel component (mock test)"""
    # This would be a frontend test using a tool like React Testing Library
    # For demonstration purposes, we're just outlining what would be tested

    # Test CollaborationPanel renders correctly
    # Test chat message display
    # Test sending messages
    # Test joining/leaving rooms
    # Test connection status display

    pass  # Actual implementation would require frontend testing setup

def test_integration_with_main_app():
    """Test the integration of WebSocket functionality with the main app"""
    # Test that WebSocketProvider is properly used in _app.tsx
    # Test that CollaborationPanel can be imported and used
    # Test that routes are properly configured

    pass  # Requires more in-depth testing infrastructure