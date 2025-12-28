import React from 'react';
import Link from 'next/link';

export interface Agent {
  id: string;
  name: string;
  description: string;
  category: string;
  capabilities?: string[];
  success_rate?: number;
  execution_count?: number;
  avatar?: string;
  is_self_improving?: boolean;
  model_type?: string;
  memory_enabled?: boolean;
  marketplace_status?: 'private' | 'public' | 'marketplace';
  can_replicate?: boolean;
}

interface AgentCardProps {
  agent: Agent;
  onExecute?: (agent: Agent) => void;
}

const AgentCard: React.FC<AgentCardProps> = ({ agent, onExecute }) => {
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

  const getAgentCategoryIcon = (category: string) => {
    const categoryIcons: Record<string, JSX.Element> = {
      'builder': (
        <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
          <path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z"></path>
        </svg>
      ),
      'testing': (
        <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"></path>
        </svg>
      ),
      'deployment': (
        <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
          <path fillRule="evenodd" d="M2 5a2 2 0 012-2h12a2 2 0 012 2v10a2 2 0 01-2 2H4a2 2 0 01-2-2V5zm3.293 1.293a1 1 0 011.414 0l3 3a1 1 0 010 1.414l-3 3a1 1 0 01-1.414-1.414L7.586 10 5.293 7.707a1 1 0 010-1.414zM13 8a1 1 0 011 1v2a1 1 0 01-1 1h-3a1 1 0 110-2h2V9a1 1 0 011-1z" clipRule="evenodd"></path>
        </svg>
      ),
      'autonomous': (
        <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
          <path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3zM6 8a2 2 0 11-4 0 2 2 0 014 0zM16 18v-3a5.972 5.972 0 00-.75-2.906A3.005 3.005 0 0119 15v3h-3zM4.75 12.094A5.973 5.973 0 004 15v3H1v-3a3 3 0 013.75-2.906z"></path>
        </svg>
      ),
      'fine-tuning': (
        <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
          <path d="M5 4a1 1 0 00-2 0v7.268a2 2 0 000 3.464V16a1 1 0 102 0v-1.268a2 2 0 000-3.464V4zM11 4a1 1 0 10-2 0v1.268a2 2 0 000 3.464V16a1 1 0 102 0V8.732a2 2 0 000-3.464V4zM16 3a1 1 0 011 1v7.268a2 2 0 010 3.464V16a1 1 0 11-2 0v-1.268a2 2 0 010-3.464V4a1 1 0 011-1z"></path>
        </svg>
      ),
      'self-improving': (
        <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
          <path fillRule="evenodd" d="M12 7a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0V8.414l-4.293 4.293a1 1 0 01-1.414 0L8 10.414l-4.293 4.293a1 1 0 01-1.414-1.414l5-5a1 1 0 011.414 0L11 10.586 14.586 7H12z" clipRule="evenodd"></path>
        </svg>
      ),
      'default': (
        <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
          <path fillRule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clipRule="evenodd"></path>
        </svg>
      )
    };
    
    return categoryIcons[category.toLowerCase()] || categoryIcons['default'];
  };

  const defaultAvatar = `https://ui-avatars.com/api/?name=${encodeURIComponent(agent.name)}&background=random&color=fff`;

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300">
      <div className="p-4">
        <div className="flex justify-between items-start">
          <div className="flex items-center space-x-3">
            <div className="flex-shrink-0 relative">
              <img 
                src={agent.avatar || defaultAvatar} 
                alt={agent.name} 
                className="h-10 w-10 rounded-full bg-gray-200"
              />
              {agent.is_self_improving && (
                <div className="absolute -top-1 -right-1 bg-emerald-500 rounded-full w-3 h-3" title="Self-improving agent"></div>
              )}
            </div>
            <div>
              <h3 className="text-lg font-medium text-gray-900 flex items-center">
                {agent.name}
                {agent.can_replicate && (
                  <span className="ml-2 text-xs px-1.5 py-0.5 bg-purple-100 text-purple-800 rounded-full" title="Can create new agents">DNA</span>
                )}
              </h3>
              <div className="flex flex-wrap gap-1">
                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getAgentCategoryColor(agent.category)}`}>
                  {getAgentCategoryIcon(agent.category)}
                  <span className="ml-1">{agent.category}</span>
                </span>
                {agent.model_type && (
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                    {agent.model_type}
                  </span>
                )}
              </div>
            </div>
          </div>
          {agent.success_rate !== undefined && (
            <div className="text-right">
              <span className="text-sm font-medium text-gray-500">Success rate</span>
              <p className="font-semibold text-green-600">{agent.success_rate}%</p>
            </div>
          )}
        </div>
        
        <p className="mt-3 text-sm text-gray-600">{agent.description}</p>

        {agent.capabilities && agent.capabilities.length > 0 && (
          <div className="mt-2">
            <div className="flex flex-wrap gap-1">
              {agent.capabilities.slice(0, 3).map((capability, idx) => (
                <span key={idx} className="text-xs px-2 py-0.5 bg-blue-50 text-blue-700 rounded-full">
                  {capability}
                </span>
              ))}
              {agent.capabilities.length > 3 && (
                <span className="text-xs px-2 py-0.5 bg-gray-50 text-gray-600 rounded-full">
                  +{agent.capabilities.length - 3} more
                </span>
              )}
            </div>
          </div>
        )}
        
        <div className="mt-4 flex justify-between items-center">
          <div className="flex items-center text-sm text-gray-500">
            {agent.execution_count !== undefined && (
              <>
                <svg className="flex-shrink-0 mr-1.5 h-5 w-5 text-gray-400" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                  <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                  <path fillRule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clipRule="evenodd" />
                </svg>
                {agent.execution_count} executions
              </>
            )}
            {agent.memory_enabled && (
              <div className="ml-3 flex items-center" title="Memory enabled">
                <svg className="h-4 w-4 text-blue-500 mr-1" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                  <path d="M5 3a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2V5a2 2 0 00-2-2H5zM5 11a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2v-2a2 2 0 00-2-2H5zM11 5a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V5zM14 11a1 1 0 011 1v1h1a1 1 0 110 2h-1v1a1 1 0 11-2 0v-1h-1a1 1 0 110-2h1v-1a1 1 0 011-1z" />
                </svg>
                <span className="text-xs">Memory</span>
              </div>
            )}
          </div>
          <div className="flex space-x-2">
            <Link 
              href={`/agents/${agent.id}`}
              className="inline-flex items-center px-3 py-1.5 border border-gray-300 text-xs font-medium rounded shadow-sm text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <svg className="-ml-0.5 mr-1.5 h-3 w-3" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                <path fillRule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clipRule="evenodd" />
              </svg>
              Details
            </Link>
            {onExecute && (
              <button
                onClick={() => onExecute(agent)}
                className="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                <svg className="-ml-0.5 mr-1.5 h-3 w-3" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clipRule="evenodd" />
                </svg>
                Execute
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AgentCard;
