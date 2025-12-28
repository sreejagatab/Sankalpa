import React, { useState, useEffect } from 'react';
import { NextPage } from 'next';
import dynamic from 'next/dynamic';
import Head from 'next/head';
import { useRouter } from 'next/router';

import { apiClient } from '../../lib/api-client';
import { useAlerts } from '../../components/alerts/GlobalAlertProvider';
import MainLayout from '../../components/layout/MainLayout';

// Dynamically import charts to avoid SSR issues
const AgentExecutionChart = dynamic(() => import('../../components/dashboard/AgentExecutionChart'), { ssr: false });
const ChainExecutionChart = dynamic(() => import('../../components/dashboard/ChainExecutionChart'), { ssr: false });
const SystemMetricsChart = dynamic(() => import('../../components/dashboard/SystemMetricsChart'), { ssr: false });
const ApiMetricsChart = dynamic(() => import('../../components/dashboard/ApiMetricsChart'), { ssr: false });

interface MetricsData {
  system: {
    cpu_percent: number;
    memory_percent: number;
    disk_percent: number;
    load_average?: number[];
    uptime: number;
  };
  api: {
    total_requests: number;
    successful_requests: number;
    failed_requests: number;
    average_response_time: number;
    success_rate: number;
  };
  agents: {
    total_executions: number;
    successful_executions: number;
    failed_executions: number;
    average_execution_time: number;
    success_rate: number;
    executions_by_agent?: Record<string, any>;
  };
}

interface HealthData {
  status: string;
  version: string;
  timestamp: number;
  health: {
    status: 'healthy' | 'warning' | 'critical';
    metrics: {
      system: any;
      api: any;
      agents: any;
    };
  };
}

const Dashboard: NextPage = () => {
  const [metricsData, setMetricsData] = useState<MetricsData | null>(null);
  const [healthData, setHealthData] = useState<HealthData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [refreshInterval, setRefreshInterval] = useState<number>(30);
  
  // For demo purposes, we'll use simulated data
  const isAuthenticated = true;
  const router = useRouter();
  const { addAlert } = useAlerts();
  
  // Create mock metrics data if we can't fetch it from the API
  const createMockMetrics = () => {
    const mockData: MetricsData = {
      system: {
        cpu_percent: 32.5,
        memory_percent: 47.8,
        disk_percent: 68.2,
        uptime: 345600 // 4 days in seconds
      },
      api: {
        total_requests: 1582,
        successful_requests: 1520,
        failed_requests: 62,
        average_response_time: 128.4,
        success_rate: 96.1
      },
      agents: {
        total_executions: 842,
        successful_executions: 795,
        failed_executions: 47,
        average_execution_time: 3.2,
        success_rate: 94.4
      }
    };
    
    return mockData;
  };
  
  // Create mock health data
  const createMockHealth = () => {
    const mockHealth: HealthData = {
      status: 'ok',
      version: '1.0.0',
      timestamp: Date.now() / 1000,
      health: {
        status: 'healthy',
        metrics: {
          system: {
            cpu_percent: 32.5,
            memory_percent: 47.8,
            disk_percent: 68.2
          },
          api: {
            success_rate: 96.1
          },
          agents: {
            success_rate: 94.4
          }
        }
      }
    };
    
    return mockHealth;
  };
  
  // Fetch metrics data
  const fetchMetrics = async () => {
    try {
      const response = await apiClient.get<MetricsData>('/api/metrics');
      
      if (response.success) {
        setMetricsData(response.data);
      } else {
        // Use mock data if API fails
        setMetricsData(createMockMetrics());
      }
    } catch (err) {
      console.log('Using mock metrics data');
      setMetricsData(createMockMetrics());
    }
  };
  
  // Fetch health data
  const fetchHealth = async () => {
    try {
      const response = await apiClient.get<HealthData>('/api/health');
      
      if (response.success) {
        setHealthData(response.data);
        
        // Show alert for non-healthy status
        if (response.data.health.status !== 'healthy') {
          addAlert({
            type: response.data.health.status === 'warning' ? 'warning' : 'error',
            title: `System status: ${response.data.health.status}`,
            message: 'Check dashboard for details',
            autoClose: true,
            duration: 5000
          });
        }
      } else {
        // Use mock data if API fails
        setHealthData(createMockHealth());
      }
    } catch (err) {
      console.log('Using mock health data');
      setHealthData(createMockHealth());
    } finally {
      setLoading(false);
    }
  };
  
  // Fetch data on component mount
  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      await Promise.all([fetchMetrics(), fetchHealth()]);
      setLoading(false);
    };
    
    fetchData();
    
    // Set up auto-refresh interval
    const intervalId = setInterval(() => {
      fetchData();
    }, refreshInterval * 1000);
    
    // Clean up interval on unmount
    return () => clearInterval(intervalId);
  }, [refreshInterval]);
  
  // Handle refresh interval change
  const handleRefreshIntervalChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setRefreshInterval(Number(e.target.value));
  };
  
  // Calculate status color
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy':
        return 'bg-green-500';
      case 'warning':
        return 'bg-yellow-500';
      case 'critical':
        return 'bg-red-500';
      default:
        return 'bg-gray-500';
    }
  };
  
  return (
    <>
      <Head>
        <title>Dashboard | Sankalpa</title>
      </Head>
      
      <div className="py-6">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center mb-6">
            <h1 className="text-2xl font-semibold text-gray-900">System Dashboard</h1>
            
            <div className="flex items-center space-x-4">
              <div className="flex items-center">
                <span className="mr-2 text-sm text-gray-700">Refresh interval:</span>
                <select
                  value={refreshInterval}
                  onChange={handleRefreshIntervalChange}
                  className="block w-32 pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
                >
                  <option value={10}>10 seconds</option>
                  <option value={30}>30 seconds</option>
                  <option value={60}>1 minute</option>
                  <option value={300}>5 minutes</option>
                </select>
              </div>
              
              <button
                onClick={() => {
                  setLoading(true);
                  Promise.all([fetchMetrics(), fetchHealth()]).then(() => setLoading(false));
                }}
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                <svg
                  className={`mr-2 h-4 w-4 ${loading ? 'animate-spin' : ''}`}
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                  ></circle>
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  ></path>
                </svg>
                Refresh
              </button>
            </div>
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
          
          {loading && !metricsData && !healthData ? (
            <div className="flex justify-center items-center h-64">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-700"></div>
            </div>
          ) : (
            <>
              {/* System Status Card */}
              {healthData && (
                <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-6">
                  <div className="bg-white overflow-hidden shadow rounded-lg">
                    <div className="px-4 py-5 sm:p-6">
                      <div className="flex items-center">
                        <div className="flex-shrink-0 bg-blue-500 rounded-md p-3">
                          <svg
                            className="h-6 w-6 text-white"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                          >
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              strokeWidth="2"
                              d="M13 10V3L4 14h7v7l9-11h-7z"
                            />
                          </svg>
                        </div>
                        <div className="ml-5 w-0 flex-1">
                          <dl>
                            <dt className="text-sm font-medium text-gray-500 truncate">System Status</dt>
                            <dd>
                              <div className="flex items-center">
                                <div className={`h-3 w-3 rounded-full ${getStatusColor(healthData.health.status)} mr-2`}></div>
                                <div className="text-lg font-medium text-gray-900">
                                  {healthData.health.status.charAt(0).toUpperCase() + healthData.health.status.slice(1)}
                                </div>
                              </div>
                            </dd>
                          </dl>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  {/* CPU Usage Card */}
                  <div className="bg-white overflow-hidden shadow rounded-lg">
                    <div className="px-4 py-5 sm:p-6">
                      <div className="flex items-center">
                        <div className="flex-shrink-0 bg-green-500 rounded-md p-3">
                          <svg
                            className="h-6 w-6 text-white"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                          >
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              strokeWidth="2"
                              d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z"
                            />
                          </svg>
                        </div>
                        <div className="ml-5 w-0 flex-1">
                          <dl>
                            <dt className="text-sm font-medium text-gray-500 truncate">CPU Usage</dt>
                            <dd>
                              <div className="flex items-center">
                                <div className="text-lg font-medium text-gray-900">
                                  {healthData.health.metrics.system.cpu_percent.toFixed(1)}%
                                </div>
                                <div className="ml-2 w-full bg-gray-200 rounded-full h-2.5">
                                  <div
                                    className={`h-2.5 rounded-full ${
                                      healthData.health.metrics.system.cpu_percent > 80
                                        ? 'bg-red-500'
                                        : healthData.health.metrics.system.cpu_percent > 50
                                        ? 'bg-yellow-500'
                                        : 'bg-green-500'
                                    }`}
                                    style={{ width: `${healthData.health.metrics.system.cpu_percent}%` }}
                                  ></div>
                                </div>
                              </div>
                            </dd>
                          </dl>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  {/* Memory Usage Card */}
                  <div className="bg-white overflow-hidden shadow rounded-lg">
                    <div className="px-4 py-5 sm:p-6">
                      <div className="flex items-center">
                        <div className="flex-shrink-0 bg-purple-500 rounded-md p-3">
                          <svg
                            className="h-6 w-6 text-white"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                          >
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              strokeWidth="2"
                              d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"
                            />
                          </svg>
                        </div>
                        <div className="ml-5 w-0 flex-1">
                          <dl>
                            <dt className="text-sm font-medium text-gray-500 truncate">Memory Usage</dt>
                            <dd>
                              <div className="flex items-center">
                                <div className="text-lg font-medium text-gray-900">
                                  {healthData.health.metrics.system.memory_percent.toFixed(1)}%
                                </div>
                                <div className="ml-2 w-full bg-gray-200 rounded-full h-2.5">
                                  <div
                                    className={`h-2.5 rounded-full ${
                                      healthData.health.metrics.system.memory_percent > 80
                                        ? 'bg-red-500'
                                        : healthData.health.metrics.system.memory_percent > 50
                                        ? 'bg-yellow-500'
                                        : 'bg-green-500'
                                    }`}
                                    style={{ width: `${healthData.health.metrics.system.memory_percent}%` }}
                                  ></div>
                                </div>
                              </div>
                            </dd>
                          </dl>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  {/* API Success Rate Card */}
                  <div className="bg-white overflow-hidden shadow rounded-lg">
                    <div className="px-4 py-5 sm:p-6">
                      <div className="flex items-center">
                        <div className="flex-shrink-0 bg-indigo-500 rounded-md p-3">
                          <svg
                            className="h-6 w-6 text-white"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                          >
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              strokeWidth="2"
                              d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                            />
                          </svg>
                        </div>
                        <div className="ml-5 w-0 flex-1">
                          <dl>
                            <dt className="text-sm font-medium text-gray-500 truncate">API Success Rate</dt>
                            <dd>
                              <div className="flex items-center">
                                <div className="text-lg font-medium text-gray-900">
                                  {healthData.health.metrics.api.success_rate.toFixed(1)}%
                                </div>
                                <div className="ml-2 w-full bg-gray-200 rounded-full h-2.5">
                                  <div
                                    className={`h-2.5 rounded-full ${
                                      healthData.health.metrics.api.success_rate < 90
                                        ? 'bg-red-500'
                                        : healthData.health.metrics.api.success_rate < 95
                                        ? 'bg-yellow-500'
                                        : 'bg-green-500'
                                    }`}
                                    style={{ width: `${healthData.health.metrics.api.success_rate}%` }}
                                  ></div>
                                </div>
                              </div>
                            </dd>
                          </dl>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
              
              {/* Charts */}
              <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
                {/* Agent Execution Chart */}
                <div className="bg-white overflow-hidden shadow rounded-lg">
                  <div className="px-4 py-5 sm:p-6">
                    <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">Agent Executions</h3>
                    {metricsData ? (
                      <AgentExecutionChart data={metricsData.agents} />
                    ) : (
                      <div className="h-64 flex items-center justify-center">
                        <p className="text-gray-500">No data available</p>
                      </div>
                    )}
                  </div>
                </div>
                
                {/* Chain Execution Chart */}
                <div className="bg-white overflow-hidden shadow rounded-lg">
                  <div className="px-4 py-5 sm:p-6">
                    <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">Chain Executions</h3>
                    {metricsData ? (
                      <ChainExecutionChart data={metricsData.agents} />
                    ) : (
                      <div className="h-64 flex items-center justify-center">
                        <p className="text-gray-500">No data available</p>
                      </div>
                    )}
                  </div>
                </div>
                
                {/* System Metrics Chart */}
                <div className="bg-white overflow-hidden shadow rounded-lg">
                  <div className="px-4 py-5 sm:p-6">
                    <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">System Metrics</h3>
                    {metricsData?.system ? (
                      <SystemMetricsChart data={metricsData.system} />
                    ) : (
                      <div className="h-64 flex items-center justify-center">
                        <p className="text-gray-500">No data available</p>
                      </div>
                    )}
                  </div>
                </div>
                
                {/* API Metrics Chart */}
                <div className="bg-white overflow-hidden shadow rounded-lg">
                  <div className="px-4 py-5 sm:p-6">
                    <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">API Metrics</h3>
                    {metricsData?.api ? (
                      <ApiMetricsChart data={metricsData.api} />
                    ) : (
                      <div className="h-64 flex items-center justify-center">
                        <p className="text-gray-500">No data available</p>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </>
  );
};

export default Dashboard;