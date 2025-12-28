import React from 'react'

export default function Memory() {
  // Mock data for memory sessions and items
  const memoryData = {
    sessions: [
      { id: 'session-1', name: 'Blog Project Session', created_at: '2023-05-15T14:30:00Z' },
      { id: 'session-2', name: 'E-commerce Build', created_at: '2023-05-14T09:15:00Z' }
    ],
    items: [
      { 
        key: 'project_requirements', 
        value: {
          name: 'Personal Blog',
          features: ['Authentication', 'Markdown Editor', 'Comments']
        }
      },
      {
        key: 'generated_schema',
        value: {
          tables: ['users', 'posts', 'comments'],
          relationships: ['User has many Posts', 'Post has many Comments']
        }
      },
      {
        key: 'agent_outputs',
        value: [
          'Generated project structure',
          'Created authentication system',
          'Implemented markdown editor'
        ]
      }
    ]
  }
  
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Memory Dashboard</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="border rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Memory Sessions</h2>
          
          {memoryData.sessions.length > 0 ? (
            <div className="divide-y">
              {memoryData.sessions.map(session => (
                <div key={session.id} className="py-3">
                  <div className="flex justify-between items-center">
                    <div>
                      <p className="font-medium">{session.name}</p>
                      <p className="text-sm text-gray-500">ID: {session.id}</p>
                    </div>
                    <span className="text-xs text-gray-500">
                      {new Date(session.created_at).toLocaleString()}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-center text-gray-500 py-4">No sessions found</p>
          )}
        </div>
        
        <div className="border rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Memory Items</h2>
          
          {memoryData.items.length > 0 ? (
            <div className="divide-y">
              {memoryData.items.map((item, index) => (
                <div key={index} className="py-3">
                  <p className="font-medium">{item.key}</p>
                  <pre className="mt-1 text-sm bg-gray-50 p-2 rounded overflow-x-auto">
                    {JSON.stringify(item.value, null, 2)}
                  </pre>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-center text-gray-500 py-4">No memory items found</p>
          )}
        </div>
      </div>
    </div>
  )
}