# Collaboration Components

This directory contains components for real-time collaboration features within Sankalpa.

## Components

### WebSocketProvider

The `WebSocketProvider` component provides WebSocket connectivity to the application through React Context. It handles:

- WebSocket connection management
- User authentication via tokens
- Joining/leaving collaboration rooms
- Message sending and receiving
- Connection status tracking

Usage:
```tsx
// Wrap your app with the provider
<WebSocketProvider>
  <YourApp />
</WebSocketProvider>

// Use the context in components
import { useWebSocket } from './WebSocketProvider';

function YourComponent() {
  const { 
    connected, 
    roomId, 
    sendMessage, 
    joinRoom, 
    leaveRoom 
  } = useWebSocket();
  
  // Use these functions/values
}
```

### CollaborationPanel

The `CollaborationPanel` component provides a UI for chat and collaboration features:

- Room creation and joining
- Real-time messaging 
- User presence indicators
- Connection status display

Usage:
```tsx
import CollaborationPanel from '../components/collaboration/CollaborationPanel';

function YourPage() {
  return (
    <div>
      <h1>Your Page</h1>
      <CollaborationPanel />
    </div>
  );
}
```

## Message Types

The WebSocket system supports these message types:

- `chat`: Text messages between users
- `user_joined`: Notification when a user joins the room
- `user_left`: Notification when a user leaves the room
- `cursor_position`: User cursor position updates
- `chain_update`: Workflow chain update notifications
- `room_info`: Information about the current room
- `error`: Error messages
- `ping`/`pong`: Connection health checks

## Backend Integration

The frontend WebSocket components connect to backend WebSocket endpoints at:
- `/ws/collaboration/{room_id}?token={auth_token}`

The backend implements the socket handling in:
- `backend/websockets/connection_manager.py`
- `backend/websockets/routes.py`

## Integration Points

The WebSocket functionality integrates with:
- Authentication system for secure connections
- Alert system for notifications
- URL-based room joining
- Routing to preserve room connections