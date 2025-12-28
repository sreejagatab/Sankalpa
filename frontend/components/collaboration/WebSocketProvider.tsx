import React, { createContext, useContext, useState, useEffect, useCallback, ReactNode } from 'react';
import { useRouter } from 'next/router';

import { useAlerts } from '../alerts/GlobalAlertProvider';

// WebSocket message types
export type MessageType = 
  | 'chat' 
  | 'cursor_position' 
  | 'chain_update' 
  | 'user_joined' 
  | 'user_left'
  | 'room_info'
  | 'error'
  | 'ping'
  | 'pong';

// WebSocket message format
export interface WebSocketMessage {
  type: MessageType;
  [key: string]: any;
}

// WebSocket context interface
interface WebSocketContextType {
  connected: boolean;
  connectionId: string | null;
  roomId: string | null;
  userCount: number;
  messages: WebSocketMessage[];
  sendMessage: (message: WebSocketMessage) => void;
  joinRoom: (roomId: string) => void;
  leaveRoom: () => void;
}

// Create context
const WebSocketContext = createContext<WebSocketContextType | undefined>(undefined);

// Hook to use the WebSocket context
export function useWebSocket() {
  const context = useContext(WebSocketContext);
  if (context === undefined) {
    throw new Error('useWebSocket must be used within a WebSocketProvider');
  }
  return context;
}

interface WebSocketProviderProps {
  children: ReactNode;
}

export function WebSocketProvider({ children }: WebSocketProviderProps) {
  const [socket, setSocket] = useState<WebSocket | null>(null);
  const [connected, setConnected] = useState(false);
  const [connectionId, setConnectionId] = useState<string | null>(null);
  const [roomId, setRoomId] = useState<string | null>(null);
  const [userCount, setUserCount] = useState(0);
  const [messages, setMessages] = useState<WebSocketMessage[]>([]);
  
  const { addAlert } = useAlerts();
  const router = useRouter();
  
  // Close socket on unmount
  useEffect(() => {
    return () => {
      if (socket) {
        socket.close();
      }
    };
  }, [socket]);
  
  // Handle socket open
  const handleOpen = useCallback(() => {
    console.log('WebSocket connected');
    setConnected(true);
    addAlert({
      type: 'success',
      message: 'Connected to collaboration server',
      duration: 3000,
    });
  }, [addAlert]);
  
  // Handle socket close
  const handleClose = useCallback(() => {
    console.log('WebSocket disconnected');
    setConnected(false);
    setConnectionId(null);
    
    addAlert({
      type: 'warning',
      message: 'Disconnected from collaboration server',
      duration: 3000,
    });
  }, [addAlert]);
  
  // Handle socket error
  const handleError = useCallback(() => {
    console.error('WebSocket error');
    setConnected(false);
    
    addAlert({
      type: 'error',
      message: 'Error connecting to collaboration server',
      duration: 5000,
    });
  }, [addAlert]);
  
  // Handle socket message
  const handleMessage = useCallback((event: MessageEvent) => {
    try {
      const data = JSON.parse(event.data) as WebSocketMessage;
      
      // Process message based on type
      switch (data.type) {
        case 'room_info':
          setConnectionId(data.connection_id);
          setUserCount(data.user_count);
          break;
          
        case 'user_joined':
        case 'user_left':
          setUserCount(data.user_count);
          addAlert({
            type: 'info',
            message: data.type === 'user_joined'
              ? `${data.user?.username || 'A user'} joined the room`
              : `${data.user?.username || 'A user'} left the room`,
            duration: 3000,
          });
          break;
          
        case 'error':
          addAlert({
            type: 'error',
            message: data.message,
            duration: 5000,
          });
          break;
      }
      
      // Add message to history
      setMessages((prev) => [...prev, data]);
      
    } catch (error) {
      console.error('Error parsing WebSocket message', error);
    }
  }, [addAlert]);
  
  // Join a room
  const joinRoom = useCallback((newRoomId: string) => {
    // We're using a simulation for now, but in production we would connect to a real WebSocket
    console.log(`Joining room: ${newRoomId}`);
    
    // Update state to simulate connection
    setConnected(true);
    setConnectionId(`sim-conn-${Date.now()}`);
    setRoomId(newRoomId);
    setUserCount(1);
    setMessages([
      {
        type: 'room_info',
        connection_id: `sim-conn-${Date.now()}`,
        user_count: 1,
        timestamp: new Date().toISOString()
      }
    ]);
    
    // Show success alert
    addAlert({
      type: 'success',
      message: `Connected to room: ${newRoomId}`,
      duration: 3000,
    });
    
    // Update URL - remember current page path to add room parameter
    if (router) {
      const currentPath = router.pathname === '/chat' ? '/chat' : '/composer';
      router.push(`${currentPath}?room=${newRoomId}`, undefined, { shallow: true });
    }
  }, [addAlert, router]);
  
  // Leave the current room
  const leaveRoom = useCallback(() => {
    console.log('Leaving room');
    
    // Update state to simulate disconnection
    setRoomId(null);
    setConnectionId(null);
    setConnected(false);
    setUserCount(0);
    setMessages([]);
    
    // Show alert
    addAlert({
      type: 'info',
      message: 'Disconnected from room',
      duration: 3000,
    });
    
    // Update URL - keep on same page but remove room parameter
    if (router) {
      const currentPath = router.pathname;
      router.push(currentPath, undefined, { shallow: true });
    }
  }, [addAlert, router]);
  
  // Send a message
  const sendMessage = useCallback((message: WebSocketMessage) => {
    if (connected) {
      console.log('Sending message:', message);
      
      // For demo purposes, we'll simulate receiving the message back
      const simulatedResponse: WebSocketMessage = {
        ...message,
        user: {
          id: 'current-user',
          username: 'You',
        },
        timestamp: new Date().toISOString()
      };
      
      // Add to messages
      setMessages((prev) => [...prev, simulatedResponse]);
    } else {
      console.warn('Cannot send message: Not connected');
    }
  }, [connected]);
  
  // Auto-connect to room from URL if available
  useEffect(() => {
    if (router && router.query.room && typeof router.query.room === 'string' && !roomId) {
      joinRoom(router.query.room);
    }
  }, [router, router?.query.room, roomId, joinRoom]);
  
  // Context value
  const value = {
    connected,
    connectionId,
    roomId,
    userCount,
    messages,
    sendMessage,
    joinRoom,
    leaveRoom,
  };
  
  return <WebSocketContext.Provider value={value}>{children}</WebSocketContext.Provider>;
}