import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import dynamic from 'next/dynamic';
import { useRouter } from 'next/router';
import { useAlerts } from '../components/alerts/GlobalAlertProvider';
import { useWebSocket } from '../components/collaboration/WebSocketProvider';
import CollaborationPanel from '../components/collaboration/CollaborationPanel';

// Dynamically import components to avoid SSR issues
const ChartComponent = dynamic(() => import('../components/dashboard/ApiMetricsChart'), { ssr: false });

interface ChatMetrics {
  totalMessages: number;
  activeRooms: number;
  activeUsers: number;
  messagesPerMinute: number;
}

const ChatDashboard: React.FC = () => {
  const router = useRouter();
  const { connected, roomId, userCount, messages } = useWebSocket();
  const [metrics, setMetrics] = useState<ChatMetrics>({
    totalMessages: 0,
    activeRooms: 1,
    activeUsers: 0,
    messagesPerMinute: 0
  });
  const { addAlert } = useAlerts();
  const [showChat, setShowChat] = useState<boolean>(false);
  const [loadingRooms, setLoadingRooms] = useState<boolean>(true);
  const [availableRooms, setAvailableRooms] = useState<any[]>([]);

  // Update metrics based on WebSocket data
  useEffect(() => {
    if (connected) {
      // Update user count from WebSocket context
      setMetrics(prev => ({
        ...prev,
        activeUsers: userCount,
        totalMessages: messages.filter(m => m.type === 'chat').length
      }));
    }
  }, [connected, userCount, messages]);

  // Fetch rooms when component mounts
  useEffect(() => {
    fetchRooms();
    
    // Refresh rooms every 30 seconds
    const interval = setInterval(fetchRooms, 30000);
    return () => clearInterval(interval);
  }, []);

  // Simulate fetching rooms from API
  const fetchRooms = () => {
    setLoadingRooms(true);
    // Simulate API call with a timeout
    setTimeout(() => {
      const mockRooms = [
        { id: 'general', name: 'General', userCount: 5 },
        { id: 'support', name: 'Support', userCount: 3 },
        { id: 'development', name: 'Development', userCount: 7 },
        { id: 'random', name: 'Random', userCount: 2 }
      ];
      setAvailableRooms(mockRooms);
      setLoadingRooms(false);
      
      // Update metrics
      setMetrics(prev => ({
        ...prev,
        activeRooms: mockRooms.length,
        messagesPerMinute: Math.floor(Math.random() * 10) + 1 // Random value between 1-10
      }));
    }, 500);
  };

  // Join a chat room
  const joinRoom = (roomId: string) => {
    setShowChat(true);
  };

  return (
    <>
      <Head>
        <title>Chat Dashboard | Sankalpa</title>
      </Head>
      
      <div className="py-6">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center mb-6">
            <h1 className="text-2xl font-semibold text-gray-900">Chat Dashboard</h1>
            
            <div className="flex items-center space-x-4">
              <button
                onClick={fetchRooms}
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                <svg
                  className={`mr-2 h-4 w-4 ${loadingRooms ? 'animate-spin' : ''}`}
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                  ></circle>
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  ></path>
                </svg>
                Refresh
              </button>
            </div>
          </div>
          
          {/* Metrics Cards */}
          <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-6">
            {/* Total Messages Card */}
            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="px-4 py-5 sm:p-6">
                <div className="flex items-center">
                  <div className="flex-shrink-0 bg-blue-500 rounded-md p-3">
                    <svg
                      className="h-6 w-6 text-white"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth="2"
                        d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
                      />
                    </svg>
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">Total Messages</dt>
                      <dd>
                        <div className="text-lg font-medium text-gray-900">
                          {metrics.totalMessages}
                        </div>
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>
            
            {/* Active Rooms Card */}
            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="px-4 py-5 sm:p-6">
                <div className="flex items-center">
                  <div className="flex-shrink-0 bg-green-500 rounded-md p-3">
                    <svg
                      className="h-6 w-6 text-white"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth="2"
                        d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"
                      />
                    </svg>
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">Active Rooms</dt>
                      <dd>
                        <div className="text-lg font-medium text-gray-900">
                          {metrics.activeRooms}
                        </div>
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>
            
            {/* Active Users Card */}
            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="px-4 py-5 sm:p-6">
                <div className="flex items-center">
                  <div className="flex-shrink-0 bg-purple-500 rounded-md p-3">
                    <svg
                      className="h-6 w-6 text-white"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth="2"
                        d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"
                      />
                    </svg>
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">Active Users</dt>
                      <dd>
                        <div className="text-lg font-medium text-gray-900">
                          {metrics.activeUsers}
                        </div>
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>
            
            {/* Messages Per Minute Card */}
            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="px-4 py-5 sm:p-6">
                <div className="flex items-center">
                  <div className="flex-shrink-0 bg-indigo-500 rounded-md p-3">
                    <svg
                      className="h-6 w-6 text-white"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth="2"
                        d="M13 10V3L4 14h7v7l9-11h-7z"
                      />
                    </svg>
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">Messages Per Minute</dt>
                      <dd>
                        <div className="text-lg font-medium text-gray-900">
                          {metrics.messagesPerMinute}
                        </div>
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          {/* Main Content */}
          <div className="grid grid-cols-1 gap-5 lg:grid-cols-3">
            {/* Rooms List */}
            <div className="bg-white overflow-hidden shadow rounded-lg lg:col-span-1">
              <div className="px-4 py-5 sm:p-6">
                <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">Available Rooms</h3>
                
                {loadingRooms ? (
                  <div className="flex justify-center py-4">
                    <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-700"></div>
                  </div>
                ) : (
                  <div className="space-y-2">
                    {availableRooms.map(room => (
                      <div 
                        key={room.id}
                        className="border rounded-lg p-3 hover:bg-gray-50 cursor-pointer flex justify-between items-center"
                        onClick={() => joinRoom(room.id)}
                      >
                        <div>
                          <h4 className="font-medium">{room.name}</h4>
                          <p className="text-sm text-gray-500">{room.userCount} users active</p>
                        </div>
                        <button className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
                          Join
                        </button>
                      </div>
                    ))}
                    
                    <button 
                      onClick={() => {
                        const roomId = 'room-' + Date.now().toString(36);
                        joinRoom(roomId);
                      }}
                      className="w-full py-2 mt-4 border border-dashed border-gray-300 rounded-lg text-gray-600 hover:bg-gray-50 flex items-center justify-center"
                    >
                      <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clipRule="evenodd" />
                      </svg>
                      Create New Room
                    </button>
                  </div>
                )}
              </div>
            </div>
            
            {/* Chat Panel or Usage Chart */}
            <div className="bg-white overflow-hidden shadow rounded-lg lg:col-span-2">
              {showChat ? (
                <div className="p-4 h-full">
                  <div className="flex justify-between items-center mb-4">
                    <h3 className="text-lg leading-6 font-medium text-gray-900">Chat</h3>
                    <button 
                      onClick={() => setShowChat(false)}
                      className="text-gray-500 hover:text-gray-700"
                    >
                      <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                      </svg>
                    </button>
                  </div>
                  <div className="h-[500px]">
                    <CollaborationPanel />
                  </div>
                </div>
              ) : (
                <div className="px-4 py-5 sm:p-6">
                  <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">Chat Usage</h3>
                  <div className="h-[500px] flex items-center justify-center">
                    <div className="text-center">
                      <svg 
                        className="mx-auto h-12 w-12 text-gray-400"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path 
                          strokeLinecap="round" 
                          strokeLinejoin="round" 
                          strokeWidth="2" 
                          d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
                        />
                      </svg>
                      <h3 className="mt-2 text-sm font-medium text-gray-900">No active chat</h3>
                      <p className="mt-1 text-sm text-gray-500">
                        Select a room from the list to join the conversation.
                      </p>
                      <div className="mt-6">
                        <button
                          onClick={() => {
                            const roomId = 'room-' + Date.now().toString(36);
                            joinRoom(roomId);
                          }}
                          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                        >
                          <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clipRule="evenodd" />
                          </svg>
                          Create a new room
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default ChatDashboard;