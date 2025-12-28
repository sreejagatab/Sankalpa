import React, { useState } from 'react'

export default function Playground() {
  const [prompt, setPrompt] = useState('')
  const [agent, setAgent] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  
  const agents = [
    { id: 'planner', name: 'Planner Agent' },
    { id: 'frontend_builder', name: 'Frontend Builder' },
    { id: 'backend_builder', name: 'Backend Builder' },
    { id: 'db_schema', name: 'Database Schema' },
  ]
  
  const handleSubmit = (e) => {
    e.preventDefault()
    if (!agent || !prompt) return
    
    setLoading(true)
    
    // Simulate API call
    setTimeout(() => {
      setResult({
        status: 'success',
        output: `Generated output for ${agent} with prompt: "${prompt}"`,
        timestamp: new Date().toISOString()
      })
      setLoading(false)
    }, 1500)
  }
  
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Agent Playground</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div>
          <form onSubmit={handleSubmit} className="border rounded-lg p-6">
            <div className="mb-4">
              <label className="block text-gray-700 mb-2">Select Agent</label>
              <select 
                value={agent}
                onChange={(e) => setAgent(e.target.value)}
                className="w-full p-2 border rounded"
              >
                <option value="">Select an agent...</option>
                {agents.map(a => (
                  <option key={a.id} value={a.id}>{a.name}</option>
                ))}
              </select>
            </div>
            
            <div className="mb-4">
              <label className="block text-gray-700 mb-2">Prompt</label>
              <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                className="w-full p-2 border rounded"
                rows={6}
                placeholder="Enter your prompt..."
              />
            </div>
            
            <button 
              type="submit" 
              className="bg-indigo-600 text-white py-2 px-4 rounded"
              disabled={loading || !agent || !prompt}
            >
              {loading ? 'Running...' : 'Run Agent'}
            </button>
          </form>
        </div>
        
        <div className="border rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Result</h2>
          
          {loading ? (
            <div className="flex justify-center items-center h-32">
              <div className="animate-spin h-8 w-8 border-4 border-indigo-500 border-t-transparent rounded-full"></div>
            </div>
          ) : result ? (
            <div>
              <div className="mb-2"><span className="font-medium">Status:</span> {result.status}</div>
              <div className="mb-2"><span className="font-medium">Output:</span></div>
              <div className="bg-gray-100 p-3 rounded whitespace-pre-wrap mb-2">{result.output}</div>
              <div className="text-sm text-gray-500">{new Date(result.timestamp).toLocaleString()}</div>
            </div>
          ) : (
            <div className="text-gray-500 text-center py-8">No results yet. Run an agent to see results.</div>
          )}
        </div>
      </div>
    </div>
  )
}