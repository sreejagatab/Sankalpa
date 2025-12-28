import React, { useState } from 'react';
import { Agent } from './AgentCard';

interface AgentDetailProps {
  agent: Agent;
  onExecute?: (agent: Agent, input: string) => void;
  onClose?: () => void;
}

const AgentDetail: React.FC<AgentDetailProps> = ({ agent, onExecute, onClose }) => {
  const [inputData, setInputData] = useState('');
  const [outputData, setOutputData] = useState('');
  const [isExecuting, setIsExecuting] = useState(false);
  const [showAdvancedOptions, setShowAdvancedOptions] = useState(false);
  const [modelType, setModelType] = useState(agent.model_type || 'default');
  const [useMemory, setUseMemory] = useState(agent.memory_enabled || false);
  const [selectedMemorySession, setSelectedMemorySession] = useState<string | null>(null);

  const getAgentCategoryColor = (category: string) => {
    const categoryColors: Record<string, string> = {
      'builder': 'bg-blue-100 text-blue-800',
      'testing': 'bg-green-100 text-green-800',
      'deployment': 'bg-purple-100 text-purple-800',
      'marketing': 'bg-yellow-100 text-yellow-800',
      'enhanced': 'bg-indigo-100 text-indigo-800',
      'orchestration': 'bg-red-100 text-red-800',
      'implementation': 'bg-gray-100 text-gray-800',
      'meta': 'bg-pink-100 text-pink-800',
      'autonomous': 'bg-violet-100 text-violet-800',
      'fine-tuning': 'bg-cyan-100 text-cyan-800',
      'self-improving': 'bg-emerald-100 text-emerald-800',
    };
    
    return categoryColors[category.toLowerCase()] || 'bg-gray-100 text-gray-800';
  };

  const handleExecute = async () => {
    if (!inputData.trim() || !onExecute) return;
    
    setIsExecuting(true);
    setOutputData('');

    try {
      // Include additional execution parameters
      const executionParams = {
        input: inputData,
        config: {
          model_type: modelType,
          use_memory: useMemory,
          memory_session_id: selectedMemorySession
        }
      };
      
      // Call the onExecute function passed from parent with stringified params
      const result = await onExecute(agent, JSON.stringify(executionParams));
      
      // Display the result
      setOutputData(typeof result === 'string' ? result : JSON.stringify(result, null, 2));
    } catch (error) {
      setOutputData(`Error: ${error instanceof Error ? error.message : String(error)}`);
    } finally {
      setIsExecuting(false);
    }
  };

  const defaultAvatar = `https://ui-avatars.com/api/?name=${encodeURIComponent(agent.name)}&background=random&color=fff`;

  const mockMemorySessions = [
    { id: 'session-1', name: 'Project Alpha' },
    { id: 'session-2', name: 'Project Beta' },
    { id: 'session-3', name: 'Personal Workspace' }
  ];

  return (
    <div className="bg-white shadow overflow-hidden sm:rounded-lg">
      {onClose && (
        <div className="px-4 py-5 sm:px-6 flex justify-between items-center">
          <h3 className="text-lg leading-6 font-medium text-gray-900">Agent Details</h3>
          <button
            onClick={onClose}
            className="inline-flex items-center p-1.5 border border-transparent rounded-full shadow-sm text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      )}
      <div className="border-t border-gray-200 px-4 py-5 sm:p-6">
        <div className="flex items-center space-x-4">
          <div className="relative">
            <img 
              src={agent.avatar || defaultAvatar} 
              alt={agent.name} 
              className="h-16 w-16 rounded-full bg-gray-200"
            />
            {agent.is_self_improving && (
              <div className="absolute -top-1 -right-1 bg-emerald-500 rounded-full w-3 h-3" title="Self-improving agent"></div>
            )}
          </div>
          <div>
            <h2 className="text-2xl font-bold text-gray-900 flex items-center">
              {agent.name}
              {agent.can_replicate && (
                <span className="ml-2 text-xs px-1.5 py-0.5 bg-purple-100 text-purple-800 rounded-full" title="Can create new agents">DNA</span>
              )}
            </h2>
            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getAgentCategoryColor(agent.category)}`}>
              {agent.category}
            </span>
            {agent.model_type && (
              <span className="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                {agent.model_type}
              </span>
            )}
          </div>
        </div>
        
        <div className="mt-6">
          <h3 className="text-lg font-medium text-gray-900">Description</h3>
          <p className="mt-2 text-gray-600">{agent.description}</p>
        </div>
        
        {agent.capabilities && agent.capabilities.length > 0 && (
          <div className="mt-6">
            <h3 className="text-lg font-medium text-gray-900">Capabilities</h3>
            <div className="mt-2 flex flex-wrap gap-2">
              {agent.capabilities.map((capability, idx) => (
                <span key={idx} className="px-2 py-1 bg-blue-50 text-blue-700 rounded-full text-sm">
                  {capability}
                </span>
              ))}
            </div>
          </div>
        )}
        
        {agent.success_rate !== undefined && (
          <div className="mt-6">
            <h3 className="text-lg font-medium text-gray-900">Performance</h3>
            <div className="mt-2 grid grid-cols-2 gap-5 sm:grid-cols-3">
              <div className="bg-white overflow-hidden shadow rounded-lg p-4">
                <dt className="text-sm font-medium text-gray-500 truncate">Success Rate</dt>
                <dd className="mt-1 text-3xl font-semibold text-green-600">{agent.success_rate}%</dd>
              </div>
              
              {agent.execution_count !== undefined && (
                <div className="bg-white overflow-hidden shadow rounded-lg p-4">
                  <dt className="text-sm font-medium text-gray-500 truncate">Total Executions</dt>
                  <dd className="mt-1 text-3xl font-semibold text-blue-600">{agent.execution_count}</dd>
                </div>
              )}
            </div>
          </div>
        )}
        
        {onExecute && (
          <div className="mt-6">
            <h3 className="text-lg font-medium text-gray-900">Execute Agent</h3>
            
            <div className="mt-2">
              <button
                type="button"
                onClick={() => setShowAdvancedOptions(!showAdvancedOptions)}
                className="inline-flex items-center px-3 py-1 text-sm font-medium text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200"
              >
                {showAdvancedOptions ? 'Hide' : 'Show'} Advanced Options
                <svg className={`ml-1.5 h-4 w-4 transform ${showAdvancedOptions ? 'rotate-180' : ''}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>
            </div>
            
            {showAdvancedOptions && (
              <div className="mt-3 p-3 bg-gray-50 rounded-md">
                <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                  <div>
                    <label htmlFor="model-type" className="block text-sm font-medium text-gray-700">Model Type</label>
                    <select
                      id="model-type"
                      className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
                      value={modelType}
                      onChange={(e) => setModelType(e.target.value)}
                    >
                      <option value="default">Default</option>
                      <option value="gpt-4o">GPT-4o</option>
                      <option value="claude-3-opus">Claude 3 Opus</option>
                      <option value="claude-3-sonnet">Claude 3 Sonnet</option>
                      <option value="gemini-pro">Gemini Pro</option>
                      <option value="llama-3-70b">Llama 3 70B</option>
                    </select>
                  </div>
                  
                  <div className="flex flex-col">
                    <label className="flex items-center mb-2">
                      <input
                        type="checkbox"
                        checked={useMemory}
                        onChange={(e) => setUseMemory(e.target.checked)}
                        className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                      />
                      <span className="ml-2 text-sm text-gray-700">Enable Memory</span>
                    </label>
                    
                    {useMemory && (
                      <select
                        className="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
                        value={selectedMemorySession || ''}
                        onChange={(e) => setSelectedMemorySession(e.target.value)}
                      >
                        <option value="">Select Memory Session</option>
                        {mockMemorySessions.map(session => (
                          <option key={session.id} value={session.id}>{session.name}</option>
                        ))}
                      </select>
                    )}
                  </div>
                </div>
              </div>
            )}
            
            <div className="mt-4 space-y-4">
              <div>
                <label htmlFor="input-data" className="block text-sm font-medium text-gray-700">Input Prompt</label>
                <div className="mt-1">
                  <textarea
                    id="input-data"
                    name="input-data"
                    rows={5}
                    className="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
                    placeholder="Enter your instructions for the agent..."
                    value={inputData}
                    onChange={(e) => setInputData(e.target.value)}
                  />
                </div>
              </div>
              
              <div className="flex justify-end">
                <button
                  onClick={handleExecute}
                  disabled={!inputData.trim() || isExecuting}
                  className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
                >
                  {isExecuting ? (
                    <>
                      <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Executing...
                    </>
                  ) : 'Execute'}
                </button>
              </div>
              
              {outputData && (
                <div>
                  <label className="block text-sm font-medium text-gray-700">Output</label>
                  <div className="mt-1">
                    <pre className="bg-gray-100 p-4 rounded-md overflow-auto max-h-80 text-sm">
                      {outputData}
                    </pre>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AgentDetail;