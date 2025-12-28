import React, { useState, useEffect } from 'react';
import { NextPage } from 'next';
import Head from 'next/head';
import { useRouter } from 'next/router';

import { apiClient } from '../../lib/api-client';
import { useAlerts } from '../../components/alerts/GlobalAlertProvider';
import Layout from '../../components/layout/Layout';
import AgentDetail from '../../components/agents/AgentDetail';
import { Agent } from '../../components/agents/AgentCard';

const AgentDetailPage: NextPage = () => {
  const [agent, setAgent] = useState<Agent | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  const router = useRouter();
  const { id } = router.query;
  const { addAlert } = useAlerts();

  useEffect(() => {
    if (id) {
      fetchAgent(id as string);
    }
  }, [id]);

  const fetchAgent = async (agentId: string) => {
    setLoading(true);
    setError(null);

    try {
      // Attempt to fetch from the API first
      const response = await apiClient.getAgentById(agentId);
      
      if (response.success && response.data) {
        setAgent(response.data);
      } else {
        // Fall back to mock data for development
        const mockAgent = createMockAgent(agentId);
        if (mockAgent) {
          setAgent(mockAgent);
        } else {
          setError('Agent not found');
          addAlert({
            type: 'error',
            title: 'Error',
            message: 'Agent not found',
            autoClose: true,
            duration: 5000
          });
        }
      }
    } catch (err) {
      console.error('Error fetching agent:', err);
      // Fall back to mock data on error
      const mockAgent = createMockAgent(id as string);
      if (mockAgent) {
        setAgent(mockAgent);
      } else {
        setError('Failed to load agent details');
        addAlert({
          type: 'error',
          title: 'Error',
          message: 'Failed to load agent details',
          autoClose: true,
          duration: 5000
        });
      }
    } finally {
      setLoading(false);
    }
  };

  const createMockAgent = (agentId: string): Agent | null => {
    // Map of agent IDs to mock data
    const agentMap: Record<string, Agent> = {
      'frontend-builder': {
        id: 'frontend-builder',
        name: 'Frontend Builder',
        description: 'Builds complex React, Next.js or Vue.js frontend code from specifications. This agent specializes in creating responsive, accessible, and well-structured frontend components, pages, and layouts based on high-level requirements. It can handle different styling approaches including CSS, Tailwind, and styled-components.',
        category: 'builder',
        success_rate: 94,
        execution_count: 128
      },
      'backend-builder': {
        id: 'backend-builder',
        name: 'Backend Builder',
        description: 'Creates backend services with FastAPI, Flask, or Django based on specifications. This agent handles database integration, authentication systems, middleware, and API endpoints. It follows best practices for security, performance, and code organization.',
        category: 'builder',
        success_rate: 91,
        execution_count: 103
      },
      'api-builder': {
        id: 'api-builder',
        name: 'API Builder',
        description: 'Designs RESTful or GraphQL APIs with comprehensive documentation. This agent creates API specifications, route definitions, validation rules, and authentication mechanisms. It generates OpenAPI/Swagger documentation and handles versioning considerations.',
        category: 'builder',
        success_rate: 88,
        execution_count: 89
      },
      'planner': {
        id: 'planner',
        name: 'Planner Agent',
        description: 'Creates development plans and roadmaps for projects with timeline estimates. This agent breaks down complex projects into manageable tasks, estimates effort, identifies dependencies, and creates sprint plans. It can adapt to changing requirements and update plans accordingly.',
        category: 'orchestration',
        success_rate: 89,
        execution_count: 41
      },
      'copilot': {
        id: 'copilot',
        name: 'Copilot Agent',
        description: 'Provides real-time assistance for developers with code suggestions and problem-solving. This enhanced agent serves as an AI pair programmer, offering contextual code suggestions, debugging help, and architectural guidance. It learns from your coding patterns and adapts to your preferred style over time.',
        category: 'enhanced',
        success_rate: 95,
        execution_count: 312
      }
    };
    
    return agentMap[agentId] || null;
  };

  const handleExecuteWithInput = async (agent: Agent, input: string) => {
    try {
      // Call the API to generate with the agent
      const response = await apiClient.generateWithAgent(agent.id, input);
      
      if (response.success) {
        addAlert({
          type: 'success',
          title: 'Agent Executed',
          message: `${agent.name} has been executed successfully`,
          autoClose: true,
          duration: 5000
        });
        return response.data;
      } else {
        throw new Error(response.error || 'Unknown error');
      }
    } catch (err) {
      console.error('Error executing agent:', err);
      addAlert({
        type: 'error',
        title: 'Execution Failed',
        message: `Failed to execute ${agent.name}: ${err instanceof Error ? err.message : String(err)}`,
        autoClose: true,
        duration: 5000
      });
      throw err;
    }
  };

  const handleBackToList = () => {
    router.push('/agents');
  };

  return (
    <Layout>
      <Head>
        <title>{agent ? `${agent.name} | Sankalpa` : 'Agent Details | Sankalpa'}</title>
      </Head>
      
      <div className="py-6">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="mb-6">
            <button
              onClick={handleBackToList}
              className="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <svg className="-ml-0.5 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
              </svg>
              Back to Agents
            </button>
          </div>
          
          {error && (
            <div className="mb-6 bg-red-50 border-l-4 border-red-400 p-4">
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
          )}
          
          {loading ? (
            <div className="flex justify-center items-center h-64">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-700"></div>
            </div>
          ) : agent ? (
            <AgentDetail 
              agent={agent} 
              onExecute={handleExecuteWithInput}
            />
          ) : null}
        </div>
      </div>
    </Layout>
  );
};

export default AgentDetailPage;