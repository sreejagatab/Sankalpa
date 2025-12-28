import React, { useState, useEffect } from 'react';
import { NextPage } from 'next';
import Head from 'next/head';
import dynamic from 'next/dynamic';

import { apiClient } from '../lib/api-client';
import Layout from '../components/layout/Layout';
import { Agent } from '../components/agents/AgentCard';

// Dynamically import AgentChat to avoid SSR issues with WebSocket
const AgentChat = dynamic(() => import('../components/agents/AgentChat'), { ssr: false });

const AgentChatPage: NextPage = () => {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchAgents();
  }, []);

  const fetchAgents = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await apiClient.listAgents();
      
      if (response.success && response.data) {
        // Normally we'd transform the API response to match our Agent interface
        // For now, we'll use mock data since we're building the UI first
        const mockAgents = createMockAgents();
        setAgents(mockAgents);
      } else {
        setError('Failed to load agents');
      }
    } catch (err) {
      console.error('Error fetching agents:', err);
      const mockAgents = createMockAgents();
      setAgents(mockAgents);
    } finally {
      setLoading(false);
    }
  };

  const createMockAgents = (): Agent[] => {
    // These agents correspond to what we found in the agents folder
    return [
      {
        id: 'frontend-builder',
        name: 'Frontend Builder',
        description: 'Builds complex React, Next.js or Vue.js frontend code from specifications.',
        category: 'builder',
        success_rate: 94,
        execution_count: 128
      },
      {
        id: 'backend-builder',
        name: 'Backend Builder',
        description: 'Creates backend services with FastAPI, Flask, or Django based on specifications.',
        category: 'builder',
        success_rate: 91,
        execution_count: 103
      },
      {
        id: 'api-builder',
        name: 'API Builder',
        description: 'Designs RESTful or GraphQL APIs with comprehensive documentation.',
        category: 'builder',
        success_rate: 88,
        execution_count: 89
      },
      {
        id: 'test-suite',
        name: 'Test Suite Agent',
        description: 'Creates comprehensive test suites for frontend and backend code.',
        category: 'testing',
        success_rate: 93,
        execution_count: 105
      },
      {
        id: 'copilot',
        name: 'Copilot Agent',
        description: 'Provides real-time assistance for developers with code suggestions and problem-solving.',
        category: 'enhanced',
        success_rate: 95,
        execution_count: 312
      },
      {
        id: 'planner',
        name: 'Planner Agent',
        description: 'Creates development plans and roadmaps for projects with timeline estimates.',
        category: 'orchestration',
        success_rate: 89,
        execution_count: 41
      }
    ];
  };

  const handleAgentSelect = (agent: Agent) => {
    console.log(`Selected agent: ${agent.name}`);
    // Additional actions can be added here
  };

  return (
    <Layout>
      <Head>
        <title>Agent Chat | Sankalpa</title>
      </Head>
      
      <div className="h-[calc(100vh-8rem)]">
        {loading ? (
          <div className="flex justify-center items-center h-full">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-700"></div>
          </div>
        ) : error ? (
          <div className="flex justify-center items-center h-full">
            <div className="bg-red-50 border-l-4 border-red-400 p-4">
              <div className="flex">
                <div className="flex-shrink-0">
                  <svg
                    className="h-5 w-5 text-red-400"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                  >
                    <path
                      fillRule="evenodd"
                      d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                      clipRule="evenodd"
                    />
                  </svg>
                </div>
                <div className="ml-3">
                  <p className="text-sm text-red-700">{error}</p>
                </div>
              </div>
            </div>
          </div>
        ) : (
          <AgentChat agents={agents} onAgentSelect={handleAgentSelect} />
        )}
      </div>
    </Layout>
  );
};

export default AgentChatPage;