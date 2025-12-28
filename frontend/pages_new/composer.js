import React, { useState } from 'react'

export default function Composer() {
  const [nodes, setNodes] = useState([
    { id: '1', label: 'Planner Agent', position: { x: 50, y: 50 } }
  ])
  const [output, setOutput] = useState('')
  const [showChat, setShowChat] = useState(false)
  const [messages, setMessages] = useState([
    { user: 'System', text: 'Welcome to Sankalpa Collaboration Chat' }
  ])
  const [newMessage, setNewMessage] = useState('')
  
  const addNode = () => {
    const id = (nodes.length + 1).toString()
    setNodes([
      ...nodes,
      { 
        id, 
        label: `Agent ${id}`, 
        position: { 
          x: 50 + Math.random() * 200, 
          y: 50 + Math.random() * 200 
        } 
      }
    ])
  }
  
  const runChain = () => {
    const chainOutput = {
      status: 'success',
      agents: nodes.map(n => n.label),
      result: `Chain executed with ${nodes.length} agents: ${nodes.map(n => n.label).join(' → ')}`,
      timestamp: new Date().toISOString()
    }
    
    setOutput(JSON.stringify(chainOutput, null, 2))
  }
  
  const saveChain = () => {
    alert('Chain saved successfully!')
  }
  
  const sendMessage = (e) => {
    e.preventDefault()
    if (!newMessage.trim()) return
    
    setMessages([
      ...messages,
      { user: 'You', text: newMessage }
    ])
    
    // Simulate response
    setTimeout(() => {
      setMessages(prev => [
        ...prev,
        { user: 'Assistant', text: `Response to: "${newMessage}"` }
      ])
    }, 1000)
    
    setNewMessage('')
  }
  
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Agent Chain Composer</h1>
      
      <div className="flex flex-col md:flex-row gap-4">
        <div className="flex-1 border rounded-lg p-4">
          <div className="flex gap-2 mb-4">
            <button 
              onClick={addNode}
              className="bg-blue-600 text-white px-3 py-1 rounded"
            >
              Add Agent
            </button>
            
            <button 
              onClick={runChain}
              className="bg-green-600 text-white px-3 py-1 rounded"
            >
              Run Chain
            </button>
            
            <button 
              onClick={saveChain}
              className="bg-purple-600 text-white px-3 py-1 rounded"
            >
              Save Chain
            </button>
            
            <button 
              onClick={() => setShowChat(!showChat)}
              className="bg-gray-600 text-white px-3 py-1 rounded ml-auto"
            >
              {showChat ? 'Hide Chat' : 'Show Chat'}
            </button>
          </div>
          
          <div className="border-2 border-dashed rounded-lg h-64 p-4 mb-4 relative bg-gray-50">
            <div className="text-center text-gray-500 mb-4">Agent Workflow Canvas</div>
            
            {nodes.map(node => (
              <div 
                key={node.id}
                className="absolute bg-white border rounded p-2 shadow-sm"
                style={{ 
                  left: `${node.position.x}px`, 
                  top: `${node.position.y}px`,
                  minWidth: '100px',
                  textAlign: 'center'
                }}
              >
                {node.label}
              </div>
            ))}
          </div>
          
          {output && (
            <div className="border rounded p-3 bg-gray-50">
              <h3 className="font-semibold mb-2">Output:</h3>
              <pre className="text-sm overflow-auto max-h-32">{output}</pre>
            </div>
          )}
        </div>
        
        {showChat && (
          <div className="w-full md:w-80 border rounded-lg flex flex-col h-96">
            <div className="p-3 bg-gray-100 border-b font-medium">Collaboration Chat</div>
            
            <div className="flex-1 p-3 overflow-auto">
              {messages.map((msg, i) => (
                <div key={i} className="mb-2">
                  <span className="font-semibold">{msg.user}:</span> {msg.text}
                </div>
              ))}
            </div>
            
            <form onSubmit={sendMessage} className="p-3 border-t flex">
              <input
                type="text"
                value={newMessage}
                onChange={(e) => setNewMessage(e.target.value)}
                className="flex-1 p-2 border rounded-l"
                placeholder="Type a message..."
              />
              <button 
                type="submit"
                className="bg-indigo-600 text-white px-3 py-2 rounded-r"
              >
                Send
              </button>
            </form>
          </div>
        )}
      </div>
    </div>
  )
}