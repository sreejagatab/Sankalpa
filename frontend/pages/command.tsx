import React, { useState } from 'react';
import { NextPage } from 'next';
import Head from 'next/head';
import { useRouter } from 'next/router';

import Layout from '../components/layout/Layout';
import { apiClient } from '../lib/api-client';
import { useAlerts } from '../components/alerts/GlobalAlertProvider';

const CommandPage: NextPage = () => {
  const [command, setCommand] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [showChain, setShowChain] = useState(false);
  
  const router = useRouter();
  const { addAlert } = useAlerts();
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!command.trim()) {
      addAlert({
        type: 'warning',
        message: 'Please enter a command',
      });
      return;
    }
    
    setIsProcessing(true);
    setResult(null);
    
    try {
      const response = await apiClient.post('/api/nlp/process', {
        command,
        context: {},
        options: {}
      });
      
      if (response.success) {
        setResult(response.data);
        addAlert({
          type: 'success',
          message: 'Command processed successfully',
        });
      } else {
        addAlert({
          type: 'error',
          message: 'Failed to process command',
        });
      }
    } catch (error) {
      console.error('Error processing command:', error);
      addAlert({
        type: 'error',
        message: 'Error processing command',
      });
    } finally {
      setIsProcessing(false);
    }
  };
  
  const handleExecute = () => {
    if (!result || !result.chain) return;
    
    // Store the chain in local storage to be loaded in the composer
    localStorage.setItem('pendingChain', JSON.stringify(result.chain));
    
    // Navigate to the composer page
    router.push('/composer?load=pending');
  };
  
  const renderAnalysis = () => {
    if (!result || !result.analysis) return null;
    
    const { analysis } = result;
    
    return (
      <div className="mt-6 bg-white shadow rounded-lg p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Command Analysis</h3>
        
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <div className="border rounded-md p-4">
            <h4 className="font-medium text-gray-700 mb-2">Complexity</h4>
            <div className="flex items-center">
              <div className={`h-2.5 w-2.5 rounded-full mr-2 ${
                analysis.estimated_complexity === 'simple' ? 'bg-green-500' :
                analysis.estimated_complexity === 'moderate' ? 'bg-yellow-500' :
                'bg-red-500'
              }`}></div>
              <span className="capitalize">{analysis.estimated_complexity}</span>
            </div>
          </div>
          
          <div className="border rounded-md p-4">
            <h4 className="font-medium text-gray-700 mb-2">Chain Type</h4>
            <div className="flex items-center">
              <span className="capitalize">{analysis.chain_type}</span>
              <span className="ml-2 text-sm text-gray-500">({analysis.agent_count} agents)</span>
            </div>
          </div>
        </div>
        
        <div className="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-2">
          <div className="border rounded-md p-4">
            <h4 className="font-medium text-gray-700 mb-2">Identified Entities</h4>
            {analysis.identified_entities.length > 0 ? (
              <div className="flex flex-wrap gap-2">
                {analysis.identified_entities.map((entity: string, index: number) => (
                  <span 
                    key={index}
                    className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
                  >
                    {entity}
                  </span>
                ))}
              </div>
            ) : (
              <p className="text-sm text-gray-500">No entities identified</p>
            )}
          </div>
          
          <div className="border rounded-md p-4">
            <h4 className="font-medium text-gray-700 mb-2">Identified Requirements</h4>
            {analysis.identified_requirements.length > 0 ? (
              <ul className="text-sm text-gray-500 list-disc list-inside">
                {analysis.identified_requirements.map((req: string, index: number) => (
                  <li key={index}>{req}</li>
                ))}
              </ul>
            ) : (
              <p className="text-sm text-gray-500">No specific requirements identified</p>
            )}
          </div>
        </div>
      </div>
    );
  };
  
  const renderChain = () => {
    if (!result || !result.chain) return null;
    
    const { chain } = result;
    
    return (
      <div className="mt-6 bg-white shadow rounded-lg p-6">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-medium text-gray-900">Generated Chain</h3>
          <button
            onClick={() => setShowChain(!showChain)}
            className="text-sm text-blue-600 hover:text-blue-500"
          >
            {showChain ? 'Hide Details' : 'Show Details'}
          </button>
        </div>
        
        <div className="mb-4">
          <h4 className="text-sm font-medium text-gray-700">Name</h4>
          <p className="mt-1">{chain.name}</p>
        </div>
        
        <div className="mb-4">
          <h4 className="text-sm font-medium text-gray-700">Description</h4>
          <p className="mt-1 text-sm text-gray-500">{chain.description}</p>
        </div>
        
        <div className="mb-4">
          <h4 className="text-sm font-medium text-gray-700">Chain Type</h4>
          <p className="mt-1 capitalize">{chain.type}</p>
        </div>
        
        {showChain && (
          <>
            <div className="mb-4">
              <h4 className="text-sm font-medium text-gray-700">Agents</h4>
              <div className="mt-2 border rounded-md overflow-hidden">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Name
                      </th>
                      <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Type
                      </th>
                      <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Parameters
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {chain.agents.map((agent: any, index: number) => (
                      <tr key={index}>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                          {agent.name}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {agent.type}
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-500">
                          {agent.parameters ? (
                            <pre className="text-xs overflow-x-auto">
                              {JSON.stringify(agent.parameters, null, 2)}
                            </pre>
                          ) : (
                            <span className="text-gray-400">No parameters</span>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
            
            {chain.type === 'conditional' && chain.condition_key && (
              <div className="mb-4">
                <h4 className="text-sm font-medium text-gray-700">Condition</h4>
                <p className="mt-1 mb-2">
                  <span className="font-mono bg-gray-100 px-2 py-1 rounded">
                    {chain.condition_key}
                  </span>
                </p>
                
                <div className="mt-2 border rounded-md overflow-hidden">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Value
                        </th>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Agents
                        </th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {Object.entries(chain.condition_branches || {}).map(([value, agents]: [string, any], index: number) => (
                        <tr key={index}>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                            {value}
                          </td>
                          <td className="px-6 py-4 text-sm text-gray-500">
                            {Array.isArray(agents) ? agents.join(', ') : 'N/A'}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
            
            <div className="mt-6">
              <h4 className="text-sm font-medium text-gray-700">Raw JSON</h4>
              <pre className="mt-2 p-4 bg-gray-50 rounded-md overflow-auto text-xs">
                {JSON.stringify(chain, null, 2)}
              </pre>
            </div>
          </>
        )}
        
        <div className="mt-6">
          <button
            onClick={handleExecute}
            disabled={!result.execution_ready}
            className={`inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white ${
              result.execution_ready 
                ? 'bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500'
                : 'bg-gray-300 cursor-not-allowed'
            }`}
          >
            {result.execution_ready 
              ? 'Load in Composer' 
              : 'Chain Not Ready for Execution'}
          </button>
          
          {!result.execution_ready && (
            <p className="mt-2 text-sm text-red-600">
              This chain needs more configuration before it can be executed.
            </p>
          )}
        </div>
      </div>
    );
  };
  
  return (
    <Layout>
      <Head>
        <title>Natural Language Command | Sankalpa</title>
      </Head>
      
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white shadow rounded-lg p-6">
          <h1 className="text-2xl font-bold text-gray-900 mb-6">Natural Language Command</h1>
          
          <form onSubmit={handleSubmit}>
            <div className="mb-6">
              <label htmlFor="command" className="block text-sm font-medium text-gray-700 mb-1">
                Describe what you want to build
              </label>
              
              <textarea
                id="command"
                name="command"
                rows={4}
                className="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
                placeholder="E.g., Create a blog website with a modern design, newsletter subscription, and comment section"
                value={command}
                onChange={(e) => setCommand(e.target.value)}
              />
              
              <p className="mt-2 text-sm text-gray-500">
                Be as specific as possible. Include the type of project, features, and any special requirements.
              </p>
            </div>
            
            <div className="flex justify-end">
              <button
                type="submit"
                disabled={isProcessing || !command.trim()}
                className={`inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white ${
                  isProcessing || !command.trim()
                    ? 'bg-gray-300 cursor-not-allowed'
                    : 'bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500'
                }`}
              >
                {isProcessing ? (
                  <>
                    <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Processing...
                  </>
                ) : (
                  'Process Command'
                )}
              </button>
            </div>
          </form>
        </div>
        
        {/* Example suggestions */}
        <div className="mt-6 bg-white shadow rounded-lg p-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Example Commands</h2>
          
          <div className="grid grid-cols-1 gap-4">
            {[
              "Create a blog website with a modern design, newsletter subscription, and comment section",
              "Build a dashboard application for tracking expenses with user authentication and data visualization",
              "Generate a REST API for a social media platform with user profiles, posts, and comments",
              "Make a portfolio website template with a projects section, contact form, and responsive design"
            ].map((example, index) => (
              <button
                key={index}
                onClick={() => setCommand(example)}
                className="text-left p-3 border border-gray-300 rounded-md hover:bg-gray-50 transition-colors"
              >
                <p className="text-sm text-gray-700">{example}</p>
              </button>
            ))}
          </div>
        </div>
        
        {/* Results section */}
        {result && (
          <>
            {renderAnalysis()}
            {renderChain()}
          </>
        )}
      </div>
    </Layout>
  );
};

export default CommandPage;