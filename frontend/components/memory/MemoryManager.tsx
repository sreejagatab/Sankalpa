import React, { useState, useEffect } from 'react';
import { apiClient } from '../../lib/api-client';

interface MemoryItem {
  key: string;
  value: any;
  timestamp: string;
  type: string;
  usage_count: number;
  embedding?: number[];
  vector_id?: string;
}

interface MemorySession {
  id: string;
  name: string;
  created_at: string;
  last_accessed: string;
  item_count: number;
  agent_id?: string;
}

interface MemoryManagerProps {
  sessionId?: string;
  onMemoryUpdate?: (items: MemoryItem[]) => void;
}

const MemoryManager: React.FC<MemoryManagerProps> = ({ sessionId, onMemoryUpdate }) => {
  const [sessions, setSessions] = useState<MemorySession[]>([]);
  const [items, setItems] = useState<MemoryItem[]>([]);
  const [activeSession, setActiveSession] = useState<string | undefined>(sessionId);
  const [newItemKey, setNewItemKey] = useState('');
  const [newItemValue, setNewItemValue] = useState('');
  const [newSessionName, setNewSessionName] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showCreateSession, setShowCreateSession] = useState(false);
  const [selectedMemoryType, setSelectedMemoryType] = useState<string>('json');
  const [searchQuery, setSearchQuery] = useState('');
  const [isVectorSearch, setIsVectorSearch] = useState(false);

  useEffect(() => {
    fetchSessions();
    if (activeSession) {
      fetchItems(activeSession);
    }
  }, [activeSession]);

  const fetchSessions = async () => {
    setIsLoading(true);
    setError(null);

    try {
      // For development, using mock data
      setTimeout(() => {
        const mockSessions: MemorySession[] = [
          { id: 'session-1', name: 'Project Alpha', created_at: '2023-01-15T10:30:00Z', last_accessed: '2023-01-17T14:20:00Z', item_count: 8, agent_id: 'frontend-builder' },
          { id: 'session-2', name: 'Project Beta', created_at: '2023-02-02T09:15:00Z', last_accessed: '2023-02-04T16:45:00Z', item_count: 12 },
          { id: 'session-3', name: 'Personal Workspace', created_at: '2023-03-10T11:00:00Z', last_accessed: '2023-03-10T18:30:00Z', item_count: 5, agent_id: 'copilot' },
        ];
        setSessions(mockSessions);
        setIsLoading(false);
        
        // If no active session is set, select the first one
        if (!activeSession && mockSessions.length > 0) {
          setActiveSession(mockSessions[0].id);
        }
      }, 500);
    } catch (err) {
      setError('Failed to load memory sessions');
      setIsLoading(false);
    }
  };

  const fetchItems = async (sessionId: string) => {
    setIsLoading(true);
    setError(null);

    try {
      // For development, using mock data
      setTimeout(() => {
        const mockItems: MemoryItem[] = [
          { 
            key: 'project_requirements', 
            value: { description: 'E-commerce web application with user auth, product catalog, and cart functionality', priority: 'high' },
            timestamp: '2023-01-15T10:35:00Z',
            type: 'json',
            usage_count: 12
          },
          { 
            key: 'architecture_design', 
            value: 'Frontend: React with Redux, Backend: Node.js with Express, Database: MongoDB',
            timestamp: '2023-01-15T11:20:00Z',
            type: 'text',
            usage_count: 8
          },
          { 
            key: 'api_endpoints', 
            value: [
              { path: '/api/auth/login', method: 'POST', description: 'User login' },
              { path: '/api/products', method: 'GET', description: 'Get all products' },
              { path: '/api/products/:id', method: 'GET', description: 'Get product by ID' },
              { path: '/api/cart', method: 'GET', description: 'Get user cart' },
              { path: '/api/cart', method: 'POST', description: 'Add item to cart' }
            ],
            timestamp: '2023-01-16T09:45:00Z',
            type: 'json',
            usage_count: 15,
            embedding: [0.1, 0.2, 0.3, 0.4],
            vector_id: 'vec-123456'
          },
          { 
            key: 'color_palette', 
            value: { primary: '#3B82F6', secondary: '#10B981', accent: '#8B5CF6', text: '#1F2937' },
            timestamp: '2023-01-16T14:10:00Z',
            type: 'json',
            usage_count: 6
          },
          { 
            key: 'team_feedback', 
            value: 'Navigation bar should be simplified. Add a search feature to the product catalog.',
            timestamp: '2023-01-17T11:30:00Z',
            type: 'text',
            usage_count: 4,
            embedding: [0.2, 0.3, 0.4, 0.5],
            vector_id: 'vec-789012'
          }
        ];

        // Filter items if search query exists
        let filteredItems = mockItems;
        if (searchQuery) {
          if (isVectorSearch) {
            // Simulate vector search by returning items with embeddings
            filteredItems = mockItems.filter(item => item.embedding !== undefined);
          } else {
            // Simple text search
            const query = searchQuery.toLowerCase();
            filteredItems = mockItems.filter(item => 
              item.key.toLowerCase().includes(query) || 
              (typeof item.value === 'string' && item.value.toLowerCase().includes(query)) ||
              (typeof item.value === 'object' && JSON.stringify(item.value).toLowerCase().includes(query))
            );
          }
        }
        
        setItems(filteredItems);
        if (onMemoryUpdate) {
          onMemoryUpdate(filteredItems);
        }
        setIsLoading(false);
      }, 500);
    } catch (err) {
      setError('Failed to load memory items');
      setIsLoading(false);
    }
  };

  const handleCreateItem = async () => {
    if (!newItemKey.trim() || !activeSession) return;
    
    setIsLoading(true);
    setError(null);

    try {
      // For development, simulate adding an item
      let parsedValue: any = newItemValue;
      if (selectedMemoryType === 'json') {
        try {
          parsedValue = JSON.parse(newItemValue);
        } catch (e) {
          setError('Invalid JSON format');
          setIsLoading(false);
          return;
        }
      }

      const newItem: MemoryItem = {
        key: newItemKey,
        value: parsedValue,
        timestamp: new Date().toISOString(),
        type: selectedMemoryType,
        usage_count: 0
      };

      // Simulate API response
      setTimeout(() => {
        setItems(prev => [newItem, ...prev]);
        setNewItemKey('');
        setNewItemValue('');
        setIsLoading(false);
        // Update related session item count
        setSessions(prev => 
          prev.map(session => 
            session.id === activeSession 
              ? { ...session, item_count: session.item_count + 1, last_accessed: new Date().toISOString() }
              : session
          )
        );
      }, 500);
    } catch (err) {
      setError('Failed to create memory item');
      setIsLoading(false);
    }
  };

  const handleCreateSession = async () => {
    if (!newSessionName.trim()) return;
    
    setIsLoading(true);
    setError(null);

    try {
      // For development, simulate adding a session
      const newSession: MemorySession = {
        id: `session-${Date.now()}`,
        name: newSessionName,
        created_at: new Date().toISOString(),
        last_accessed: new Date().toISOString(),
        item_count: 0
      };

      // Simulate API response
      setTimeout(() => {
        setSessions(prev => [newSession, ...prev]);
        setNewSessionName('');
        setShowCreateSession(false);
        setActiveSession(newSession.id);
        setIsLoading(false);
      }, 500);
    } catch (err) {
      setError('Failed to create memory session');
      setIsLoading(false);
    }
  };

  const handleDeleteItem = async (key: string) => {
    if (!activeSession) return;
    
    setIsLoading(true);
    setError(null);

    try {
      // For development, simulate deleting an item
      setTimeout(() => {
        setItems(prev => prev.filter(item => item.key !== key));
        setIsLoading(false);
        // Update related session item count
        setSessions(prev => 
          prev.map(session => 
            session.id === activeSession 
              ? { ...session, item_count: Math.max(0, session.item_count - 1), last_accessed: new Date().toISOString() }
              : session
          )
        );
      }, 500);
    } catch (err) {
      setError('Failed to delete memory item');
      setIsLoading(false);
    }
  };

  const formatValue = (value: any, type: string): string => {
    if (type === 'json') {
      return JSON.stringify(value, null, 2);
    }
    return String(value);
  };

  const renderMemoryValue = (item: MemoryItem) => {
    if (item.type === 'json') {
      return (
        <pre className="bg-gray-50 p-3 rounded-md overflow-auto max-h-60 text-sm">
          {formatValue(item.value, item.type)}
        </pre>
      );
    }
    return <p className="text-gray-800">{item.value}</p>;
  };

  return (
    <div className="bg-white rounded-lg shadow overflow-hidden">
      <div className="p-4 border-b border-gray-200">
        <h2 className="text-lg font-medium text-gray-900">Memory Manager</h2>
        <p className="text-sm text-gray-600 mt-1">
          Store and retrieve contextual memory for Sankalpa agents
        </p>
      </div>
      
      <div className="flex">
        {/* Sessions panel */}
        <div className="w-72 border-r border-gray-200 bg-gray-50 p-4 overflow-auto" style={{ maxHeight: '70vh' }}>
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-sm font-medium text-gray-700">Memory Sessions</h3>
            {!showCreateSession ? (
              <button
                onClick={() => setShowCreateSession(true)}
                className="text-xs px-2 py-1 bg-blue-100 text-blue-700 rounded hover:bg-blue-200 transition-colors"
              >
                New Session
              </button>
            ) : (
              <button
                onClick={() => setShowCreateSession(false)}
                className="text-xs text-gray-500 hover:text-gray-700"
              >
                Cancel
              </button>
            )}
          </div>
          
          {showCreateSession && (
            <div className="mb-4 p-3 bg-white rounded border border-gray-200">
              <input
                type="text"
                placeholder="Session name"
                className="w-full p-2 text-sm border rounded mb-2"
                value={newSessionName}
                onChange={(e) => setNewSessionName(e.target.value)}
              />
              <button
                onClick={handleCreateSession}
                disabled={!newSessionName.trim() || isLoading}
                className="w-full bg-blue-600 text-white text-xs py-2 rounded disabled:opacity-50"
              >
                {isLoading ? 'Creating...' : 'Create Session'}
              </button>
            </div>
          )}
          
          {sessions.length === 0 ? (
            <div className="text-center py-8 text-gray-500 text-sm">
              No memory sessions available
            </div>
          ) : (
            <div className="space-y-2">
              {sessions.map((session) => (
                <button
                  key={session.id}
                  onClick={() => setActiveSession(session.id)}
                  className={`w-full text-left p-3 rounded-md transition-colors ${activeSession === session.id ? 'bg-blue-100 border border-blue-300' : 'bg-white border border-gray-200 hover:bg-gray-50'}`}
                >
                  <div className="font-medium text-sm">{session.name}</div>
                  <div className="text-xs text-gray-500 mt-1 flex justify-between">
                    <span>{session.item_count} items</span>
                    <span>{new Date(session.last_accessed).toLocaleDateString()}</span>
                  </div>
                  {session.agent_id && (
                    <div className="text-xs bg-indigo-50 text-indigo-700 rounded-full px-2 py-0.5 mt-1 inline-block">
                      Agent: {session.agent_id}
                    </div>
                  )}
                </button>
              ))}
            </div>
          )}
        </div>
        
        {/* Memory items panel */}
        <div className="flex-1 p-4 overflow-auto" style={{ maxHeight: '70vh' }}>
          <div className="mb-4">
            <div className="flex items-center space-x-2 mb-2">
              <input
                type="text"
                placeholder="Search memory..."
                className="flex-1 p-2 text-sm border rounded"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="vector-search"
                  checked={isVectorSearch}
                  onChange={(e) => setIsVectorSearch(e.target.checked)}
                  className="mr-2"
                />
                <label htmlFor="vector-search" className="text-xs text-gray-700">Vector search</label>
              </div>
              <button
                onClick={() => fetchItems(activeSession!)}
                className="p-2 bg-gray-100 rounded hover:bg-gray-200"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </button>
            </div>
            
            {activeSession && (
              <div className="p-3 bg-white rounded border border-gray-200">
                <div className="flex space-x-2 mb-2">
                  <input
                    type="text"
                    placeholder="Memory key"
                    className="flex-1 p-2 text-sm border rounded"
                    value={newItemKey}
                    onChange={(e) => setNewItemKey(e.target.value)}
                  />
                  <select
                    className="p-2 text-sm border rounded bg-white"
                    value={selectedMemoryType}
                    onChange={(e) => setSelectedMemoryType(e.target.value)}
                  >
                    <option value="json">JSON</option>
                    <option value="text">Text</option>
                    <option value="embedding">Embedding</option>
                  </select>
                </div>
                <textarea
                  placeholder={selectedMemoryType === 'json' ? '{"example": "value"}' : 'Memory value'}
                  className="w-full p-2 text-sm border rounded mb-2 font-mono"
                  rows={3}
                  value={newItemValue}
                  onChange={(e) => setNewItemValue(e.target.value)}
                />
                <button
                  onClick={handleCreateItem}
                  disabled={!newItemKey.trim() || isLoading}
                  className="w-full bg-blue-600 text-white text-xs py-2 rounded disabled:opacity-50"
                >
                  {isLoading ? 'Saving...' : 'Save to Memory'}
                </button>
              </div>
            )}
          </div>
          
          {error && (
            <div className="mb-4 p-3 bg-red-50 border-l-4 border-red-500 text-red-700 text-sm">
              {error}
            </div>
          )}
          
          {!activeSession ? (
            <div className="text-center py-8 text-gray-500">
              Select a memory session to view items
            </div>
          ) : items.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              No memory items in this session
            </div>
          ) : (
            <div className="space-y-4">
              {items.map((item) => (
                <div key={item.key} className="p-4 border rounded-lg">
                  <div className="flex justify-between items-start mb-2">
                    <div>
                      <h4 className="text-sm font-medium text-gray-900 flex items-center">
                        {item.key}
                        {item.embedding && (
                          <span className="ml-2 text-xs px-1.5 py-0.5 bg-purple-100 text-purple-800 rounded-full">Embedding</span>
                        )}
                      </h4>
                      <p className="text-xs text-gray-500">
                        {new Date(item.timestamp).toLocaleString()} · {item.usage_count} uses
                      </p>
                    </div>
                    <button
                      onClick={() => handleDeleteItem(item.key)}
                      className="text-red-500 hover:text-red-700"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                  <div className="mt-2">
                    {renderMemoryValue(item)}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default MemoryManager;