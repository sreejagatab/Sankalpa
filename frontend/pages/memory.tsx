import { useEffect, useState } from 'react';
import Head from 'next/head';
import dynamic from 'next/dynamic';

// Dynamically import MemoryManager to fix any SSR issues with localStorage
const MemoryManager = dynamic(() => import('../components/memory/MemoryManager'), { ssr: false });

export default function MemoryDashboard() {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Just a small delay to simulate API loading
    const timer = setTimeout(() => {
      setLoading(false);
    }, 1000);
    
    return () => clearTimeout(timer);
  }, []);

  return (
    <>
      <Head>
        <title>Memory - Sankalpa</title>
      </Head>
      
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold mb-2">Memory Dashboard</h1>
          <p className="text-gray-600">
            Long-term contextual memory for agent sessions and vector knowledge storage
          </p>
        </div>
        
        <div className="bg-white p-4 rounded-lg shadow mb-6">
          <div className="flex items-start space-x-4">
            <div className="bg-blue-100 text-blue-800 p-3 rounded-full">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <h3 className="font-medium text-gray-900">About Memory System</h3>
              <p className="text-sm text-gray-600 mt-1">
                The memory system allows Sankalpa agents to maintain context across sessions. Memory items can be stored as JSON, text, or vector embeddings for semantic search.
              </p>
            </div>
          </div>
        </div>
        
        {loading ? (
          <div className="text-center p-8">
            <div className="animate-spin h-8 w-8 mx-auto border-4 border-indigo-600 border-t-transparent rounded-full"></div>
            <p className="mt-2">Loading memory system...</p>
          </div>
        ) : (
          <MemoryManager />
        )}
      </div>
    </>
  );
}