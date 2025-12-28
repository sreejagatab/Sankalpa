import { useState } from 'react';
import Head from 'next/head';

export default function Playground() {
  const [agentInput, setAgentInput] = useState('');
  const [selectedAgent, setSelectedAgent] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const availableAgents = [
    { id: 'project_architect', name: 'Project Architect' },
    { id: 'frontend_builder', name: 'Frontend Builder' },
    { id: 'backend_builder', name: 'Backend Builder' },
    { id: 'db_schema', name: 'Database Schema Designer' },
    { id: 'api_builder', name: 'API Builder' },
  ];

  const handleAgentExecution = async (e) => {
    e.preventDefault();
    
    if (!selectedAgent) {
      setError('Please select an agent');
      return;
    }
    
    if (!agentInput.trim()) {
      setError('Please provide input for the agent');
      return;
    }
    
    setLoading(true);
    setError('');
    
    try {
      // For demo purposes, we'll just simulate a response
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      setResult({
        agent: selectedAgent,
        input: agentInput,
        output: `Sample output for ${selectedAgent} with input: "${agentInput}"`,
        timestamp: new Date().toISOString()
      });
    } catch (err) {
      setError('Failed to execute agent. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Head>
        <title>Playground - Sankalpa</title>
      </Head>
      
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold mb-2">Agent Playground</h1>
          <p className="text-gray-600">
            Test different AI agents with your prompts and see the results.
          </p>
        </div>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <form onSubmit={handleAgentExecution} className="space-y-4 border rounded-lg p-4">
            <div>
              <label htmlFor="agent-select" className="block text-sm font-medium text-gray-700 mb-1">
                Select Agent
              </label>
              <select
                id="agent-select"
                value={selectedAgent}
                onChange={(e) => setSelectedAgent(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md"
              >
                <option value="">Select an agent...</option>
                {availableAgents.map((agent) => (
                  <option key={agent.id} value={agent.id}>
                    {agent.name}
                  </option>
                ))}
              </select>
            </div>
            
            <div>
              <label htmlFor="agent-input" className="block text-sm font-medium text-gray-700 mb-1">
                Agent Input
              </label>
              <textarea
                id="agent-input"
                value={agentInput}
                onChange={(e) => setAgentInput(e.target.value)}
                placeholder="Enter instructions for the agent..."
                rows={6}
                className="w-full px-3 py-2 border border-gray-300 rounded-md"
              ></textarea>
            </div>
            
            {error && (
              <div className="p-3 bg-red-100 text-red-700 rounded-md">
                {error}
              </div>
            )}
            
            <button
              type="submit"
              disabled={loading}
              className="w-full py-2 px-4 rounded-md text-white bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50"
            >
              {loading ? 'Executing...' : 'Execute Agent'}
            </button>
          </form>
          
          <div className="border rounded-lg p-4">
            <h2 className="text-xl font-semibold mb-4">Agent Results</h2>
            {loading ? (
              <div className="p-8 text-center">
                <div className="animate-spin h-8 w-8 mx-auto border-4 border-indigo-600 border-t-transparent rounded-full"></div>
                <p className="mt-2 text-gray-600">Executing agent...</p>
              </div>
            ) : result ? (
              <div>
                <div className="mb-2">
                  <span className="font-medium">Agent:</span>{' '}
                  {availableAgents.find(a => a.id === result.agent)?.name || result.agent}
                </div>
                <div className="mb-2">
                  <span className="font-medium">Input:</span>
                  <div className="mt-1 p-2 bg-gray-50 border rounded">{result.input}</div>
                </div>
                <div>
                  <span className="font-medium">Output:</span>
                  <div className="mt-1 p-2 bg-gray-50 border rounded whitespace-pre-wrap">
                    {result.output}
                  </div>
                </div>
                <div className="mt-2 text-xs text-gray-500">
                  {new Date(result.timestamp).toLocaleString()}
                </div>
              </div>
            ) : (
              <div className="p-8 text-center text-gray-500">
                No results yet. Execute an agent to see results here.
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  );
}