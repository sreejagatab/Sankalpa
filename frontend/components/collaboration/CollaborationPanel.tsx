import React, { useState, useRef, useEffect } from 'react';
import { useWebSocket, WebSocketMessage } from './WebSocketProvider';

interface CollaborationPanelProps {
  onClose?: () => void;
}

const CollaborationPanel: React.FC<CollaborationPanelProps> = ({ onClose }) => {
  const { connected, roomId, userCount, messages, sendMessage, joinRoom, leaveRoom } = useWebSocket();
  
  const [chatMessage, setChatMessage] = useState('');
  const [newRoomId, setNewRoomId] = useState('');
  const [chatMessages, setChatMessages] = useState<WebSocketMessage[]>([]);
  const chatEndRef = useRef<HTMLDivElement>(null);
  
  // Filter chat messages from all messages
  useEffect(() => {
    setChatMessages(messages.filter(msg => msg.type === 'chat'));
  }, [messages]);
  
  // Scroll to bottom when new messages arrive
  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [chatMessages]);
  
  const handleSendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!chatMessage.trim() || !connected) return;
    
    sendMessage({
      type: 'chat',
      message: chatMessage,
      timestamp: new Date().toISOString()
    });
    
    setChatMessage('');
  };
  
  const handleJoinRoom = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!newRoomId.trim()) return;
    
    joinRoom(newRoomId);
    setNewRoomId('');
  };
  
  return (
    <div className="bg-white rounded-lg shadow-lg p-4 w-full max-w-md">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-bold">Collaboration</h2>
        {onClose && (
          <button 
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700"
          >
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path
                fillRule="evenodd"
                d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                clipRule="evenodd"
              />
            </svg>
          </button>
        )}
      </div>
      
      <div className="mb-4">
        <div className="flex items-center mb-2">
          <div className={`w-3 h-3 rounded-full mr-2 ${connected ? 'bg-green-500' : 'bg-red-500'}`} />
          <p className="text-sm font-medium">
            {connected ? 'Connected' : 'Disconnected'}
            {roomId && connected && ` to room: ${roomId}`}
          </p>
        </div>
        
        {connected && roomId && (
          <div className="flex justify-between">
            <p className="text-sm text-gray-600">{userCount} user(s) in this room</p>
            <button
              onClick={leaveRoom}
              className="text-sm text-red-600 hover:text-red-800"
            >
              Leave Room
            </button>
          </div>
        )}
      </div>
      
      {!connected || !roomId ? (
        <div className="mb-4">
          <form onSubmit={handleJoinRoom} className="flex">
            <input
              type="text"
              placeholder="Enter room ID"
              value={newRoomId}
              onChange={(e) => setNewRoomId(e.target.value)}
              className="flex-grow px-3 py-2 border rounded-l-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              type="submit"
              className="px-4 py-2 bg-blue-600 text-white rounded-r-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              Join
            </button>
          </form>
          
          <div className="mt-2">
            <button
              onClick={() => joinRoom(`room-${Date.now().toString(36)}`)}
              className="w-full px-4 py-2 text-blue-600 border border-blue-600 rounded-lg hover:bg-blue-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              Create New Room
            </button>
          </div>
        </div>
      ) : (
        <>
          <div className="h-64 overflow-y-auto mb-4 border rounded-lg p-2 bg-gray-50">
            {chatMessages.length === 0 ? (
              <p className="text-gray-500 text-center py-4">No messages yet. Start the conversation!</p>
            ) : (
              <div className="space-y-2">
                {chatMessages.map((msg, index) => (
                  <div
                    key={index}
                    className={`p-2 rounded-lg max-w-[80%] ${
                      msg.user?.id === 'current-user'
                        ? 'ml-auto bg-blue-100 text-blue-900'
                        : 'bg-gray-200 text-gray-900'
                    }`}
                  >
                    <div className="text-xs font-medium mb-1">
                      {msg.user?.username || 'Anonymous'}
                    </div>
                    <div>{msg.message}</div>
                    <div className="text-xs text-right opacity-50">
                      {new Date(msg.timestamp).toLocaleTimeString()}
                    </div>
                  </div>
                ))}
                <div ref={chatEndRef} />
              </div>
            )}
          </div>
          
          <form onSubmit={handleSendMessage} className="flex">
            <input
              type="text"
              placeholder="Type your message..."
              value={chatMessage}
              onChange={(e) => setChatMessage(e.target.value)}
              className="flex-grow px-3 py-2 border rounded-l-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              type="submit"
              className="px-4 py-2 bg-blue-600 text-white rounded-r-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              Send
            </button>
          </form>
        </>
      )}
    </div>
  );
};

export default CollaborationPanel;