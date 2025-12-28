import React, { useState } from 'react';
import Head from 'next/head';
import CollaborationPanel from '../components/collaboration/CollaborationPanel';
import dynamic from 'next/dynamic';

// Dynamically import ChatSidebar to fix importing issues
const ChatSidebar = dynamic(() => import('../components/chat/ChatSidebar'), { ssr: false });

export default function ChatPage() {
  const [activeRoom, setActiveRoom] = useState<string | null>(null);
  const [showFullScreen, setShowFullScreen] = useState(false);
  
  const handleRoomSelect = (roomId: string) => {
    setActiveRoom(roomId);
  };
  
  return (
    <>
      <Head>
        <title>Chat - Sankalpa</title>
      </Head>
      
      <div className="space-y-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <h1 className="text-2xl font-bold mb-4">Real-time Collaboration</h1>
          <p className="text-gray-600 mb-4">
            Connect with other users to collaborate in real-time. Join an existing room or create a new one.
          </p>
          
          <div className="flex justify-end">
            <button
              onClick={() => setShowFullScreen(!showFullScreen)}
              className="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700 transition"
            >
              {showFullScreen ? 'Minimize' : 'Expand'}
            </button>
          </div>
        </div>
        
        <div className={`${showFullScreen ? 'fixed inset-0 z-50 bg-white p-6' : ''}`}>
          {showFullScreen && (
            <button
              onClick={() => setShowFullScreen(false)}
              className="absolute top-4 right-4 p-2 rounded-full hover:bg-gray-100"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          )}
          
          <div className={`mx-auto ${showFullScreen ? 'h-full' : ''} flex flex-col md:flex-row gap-6`}>
            <div className="md:w-1/3">
              <ChatSidebar onRoomSelect={handleRoomSelect} />
            </div>
            
            <div className="md:w-2/3">
              <CollaborationPanel onClose={showFullScreen ? () => setShowFullScreen(false) : undefined} />
            </div>
          </div>
        </div>
        
        <div className="bg-blue-50 border border-blue-200 p-6 rounded-lg">
          <h2 className="text-xl font-bold text-blue-800 mb-2">How to use the chat</h2>
          <ul className="list-disc list-inside space-y-2 text-blue-800">
            <li>Click <strong>Create New Room</strong> to start a new collaboration session</li>
            <li>Share the room ID with others so they can join your session</li>
            <li>Select a room from the sidebar to join an existing session</li>
            <li>Type messages in the chat box and press <strong>Send</strong> to communicate</li>
            <li>Click <strong>Leave Room</strong> when you're done collaborating</li>
          </ul>
        </div>
      </div>
    </>
  );
}