# Sankalpa Chat Module Documentation

## Overview

The chat module provides real-time collaboration capabilities within the Sankalpa platform. It enables users to:
- Create and join collaboration rooms
- Exchange messages in real-time
- See who else is in the same room
- Collaborate on workflows and projects

## Architecture

The chat system follows a client-server architecture with WebSockets:

1. **Backend**:
   - WebSocket server implemented with FastAPI
   - Room-based connection management
   - Message broadcasting and user tracking
   - Authentication via tokens

2. **Frontend**:
   - React Context provider for WebSocket connection management
   - UI components for chatting and room management
   - Real-time message display and notifications

## Implementation Files

### Backend
- `backend/websockets/connection_manager.py`: Core WebSocket connection handling
- `backend/websockets/routes.py`: WebSocket endpoints and HTTP APIs
- `backend/websockets/__init__.py`: Module initialization

### Frontend
- `frontend/components/collaboration/WebSocketProvider.tsx`: React Context provider
- `frontend/components/collaboration/CollaborationPanel.tsx`: Chat UI component
- `frontend/pages/chat.tsx`: Dedicated chat page
- `frontend/components/collaboration/README.md`: Component documentation

## Integration Points

The chat module is integrated into the application in these ways:

1. The `WebSocketProvider` is included in `_app.tsx` to provide app-wide WebSocket context
2. The `CollaborationPanel` component is embedded in the composer page for workflow collaboration
3. A dedicated `/chat` route provides a full-page chat experience
4. The navigation menu includes a link to the chat page

## Message Types

The system supports various message types:
- `chat`: Text messages between users
- `user_joined`/`user_left`: Presence notifications
- `cursor_position`: For collaborative editing
- `chain_update`: For workflow updates
- `room_info`: Room metadata
- `error`: Error messages
- `ping`/`pong`: Connection health checks

## Testing

Tests for the chat functionality are in:
- `tests/integration/test_chat_integration.py`

## Future Enhancements

Possible future improvements:
1. Add message persistence with database storage
2. Implement file sharing functionality
3. Add video/audio chat capabilities
4. Add end-to-end encryption for secure communications
5. Support direct messaging between users

## Usage Instructions

See the chat page (`/chat`) for detailed usage instructions.
