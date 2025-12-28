import React, { useState, useEffect } from 'react';
import { useWebSocket } from '../../frontend/components/collaboration/WebSocketProvider';

interface ChatRoom {
  id: string;
  name: string;
  userCount: number;
}

interface ChatSidebarProps {
  onRoomSelect?: (roomId: string) => void;
}

const ChatSidebar: React.FC<ChatSidebarProps> = ({ onRoomSelect }) => {
  const { connected, roomId: activeRoomId, joinRoom, userCount } = useWebSocket();
  const [loading, setLoading] = useState(false);
  const [rooms, setRooms] = useState<ChatRoom[]>([]);
  const [newRoomName, setNewRoomName] = useState('');
  const [showCreateForm, setShowCreateForm] = useState(false);

  // Fetch rooms from server or use mock data
  useEffect(() => {
    fetchRooms();
    // Set up refresh interval
    const interval = setInterval(fetchRooms, 30000);
    return () => clearInterval(interval);
  }, []);

  // Mock fetching rooms from server
  const fetchRooms = () => {
    setLoading(true);
    // Simulate API call
    setTimeout(() => {
      const mockRooms = [
        { id: 'general', name: 'General', userCount: 5 },
        { id: 'support', name: 'Support', userCount: 3 },
        { id: 'development', name: 'Development', userCount: 7 },
        { id: 'random', name: 'Random', userCount: 2 }
      ];
      
      setRooms(mockRooms);
      setLoading(false);
    }, 1000);
  };

  // Handle room join
  const handleJoinRoom = (roomId: string) => {
    joinRoom(roomId);
    if (onRoomSelect) {
      onRoomSelect(roomId);
    }
  };

  // Handle room creation
  const handleCreateRoom = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newRoomName.trim()) return;
    
    const roomId = `room-${Date.now().toString(36)}`;
    // Add the new room to the list
    setRooms(prev => [...prev, { id: roomId, name: newRoomName, userCount: 0 }]);
    // Join the new room
    handleJoinRoom(roomId);
    // Reset form
    setNewRoomName('');
    setShowCreateForm(false);
  };

  return (
    <div className="bg-white rounded-lg shadow p-4 h-full">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-lg font-medium text-gray-900">Chat Rooms</h2>
        <button
          onClick={fetchRooms}
          className="text-gray-500 hover:text-gray-700"
          title="Refresh"
        >
          <svg className={`w-5 h-5 ${loading ? 'animate-spin' : ''}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
        </button>
      </div>
      
      {/* Connection status */}
      <div className="flex items-center mb-4 p-2 bg-gray-50 rounded-md">
        <div className={`w-2 h-2 rounded-full mr-2 ${connected ? 'bg-green-500' : 'bg-red-500'}`}></div>
        <span className="text-sm text-gray-600">
          {connected ? `Connected (${userCount} users)` : 'Disconnected'}
        </span>
      </div>
      
      {/* Room list */}
      <div className="space-y-2 mb-4">
        <h3 className="text-sm font-medium text-gray-700">Available Rooms</h3>
        
        {loading ? (
          <div className="flex justify-center py-4">
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-indigo-500"></div>
          </div>
        ) : rooms.length === 0 ? (
          <p className="text-sm text-gray-500 py-2">No active rooms</p>
        ) : (
          <div className="space-y-1 max-h-60 overflow-y-auto">
            {rooms.map(room => (
              <div
                key={room.id}
                className={`p-2 rounded cursor-pointer flex justify-between items-center ${
                  activeRoomId === room.id
                    ? 'bg-indigo-100 border border-indigo-300'
                    : 'hover:bg-gray-50 border border-gray-100'
                }`}
                onClick={() => handleJoinRoom(room.id)}
              >
                <div>
                  <p className="font-medium text-sm">{room.name}</p>
                  <p className="text-xs text-gray-500">{room.userCount} users</p>
                </div>
                {activeRoomId !== room.id && (
                  <button className="text-xs px-2 py-1 bg-indigo-50 text-indigo-700 rounded hover:bg-indigo-100">
                    Join
                  </button>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
      
      {/* Create room button/form */}
      {showCreateForm ? (
        <form onSubmit={handleCreateRoom} className="mt-2">
          <div className="flex items-center mb-2">
            <input
              type="text"
              value={newRoomName}
              onChange={(e) => setNewRoomName(e.target.value)}
              placeholder="Room name"
              className="flex-grow px-3 py-2 border rounded-l focus:outline-none focus:ring-2 focus:ring-indigo-500 text-sm"
              autoFocus
            />
            <button
              type="submit"
              className="px-3 py-2 bg-indigo-600 text-white rounded-r hover:bg-indigo-700 text-sm"
            >
              Create
            </button>
          </div>
          <button
            type="button"
            onClick={() => setShowCreateForm(false)}
            className="text-xs text-gray-500 hover:text-gray-700"
          >
            Cancel
          </button>
        </form>
      ) : (
        <button
          onClick={() => setShowCreateForm(true)}
          className="w-full py-2 text-sm border border-dashed border-gray-300 rounded text-gray-600 hover:bg-gray-50 flex items-center justify-center"
        >
          <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clipRule="evenodd" />
          </svg>
          Create New Room
        </button>
      )}
    </div>
  );
};

export default ChatSidebar;