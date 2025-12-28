import React from 'react';

interface AgentExecutionProps {
  data: {
    total_executions: number;
    successful_executions: number;
    failed_executions: number;
    average_execution_time: number;
    success_rate: number;
    executions_by_agent?: Record<string, any>;
  };
}

// Mock data for executions by agent type
const mockAgentTypeData = [
  { name: 'Builder', value: 342 },
  { name: 'Testing', value: 267 },
  { name: 'Deployment', value: 185 },
  { name: 'Marketing', value: 123 },
  { name: 'Enhanced', value: 95 }
];

// Mock data for top agents by execution time
const topAgentsByTimeData = [
  { name: 'api_builder', time: 1.2 },
  { name: 'test_suite', time: 0.9 },
  { name: 'frontend_builder', time: 0.8 },
  { name: 'deploy_executor', time: 0.7 },
  { name: 'project_architect', time: 0.6 }
];

const AgentExecutionChart: React.FC<AgentExecutionProps> = ({ data }) => {
  // Calculate success percentage
  const successPercentage = data.total_executions > 0
    ? (data.successful_executions / data.total_executions) * 100
    : 0;
  
  const failPercentage = data.total_executions > 0
    ? (data.failed_executions / data.total_executions) * 100
    : 0;
  
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Execution Status Chart (simplified as progress bars) */}
        <div className="p-4 bg-white rounded-lg shadow">
          <h4 className="text-sm font-medium text-gray-500 mb-4 text-center">Execution Status</h4>
          
          <div className="space-y-4">
            <div>
              <div className="flex justify-between mb-1">
                <span className="text-sm font-medium">Successful ({data.successful_executions})</span>
                <span className="text-sm font-medium">{successPercentage.toFixed(1)}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2.5">
                <div className="bg-green-500 h-2.5 rounded-full" style={{ width: `${successPercentage}%` }}></div>
              </div>
            </div>
            
            <div>
              <div className="flex justify-between mb-1">
                <span className="text-sm font-medium">Failed ({data.failed_executions})</span>
                <span className="text-sm font-medium">{failPercentage.toFixed(1)}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2.5">
                <div className="bg-red-500 h-2.5 rounded-full" style={{ width: `${failPercentage}%` }}></div>
              </div>
            </div>
          </div>
        </div>
        
        {/* Agent Type Distribution Chart (simplified as vertical bars) */}
        <div className="p-4 bg-white rounded-lg shadow">
          <h4 className="text-sm font-medium text-gray-500 mb-4 text-center">Agents by Type</h4>
          
          <div className="flex h-40 items-end space-x-2">
            {mockAgentTypeData.map((item, index) => {
              // Calculate relative height (0-100%)
              const maxValue = Math.max(...mockAgentTypeData.map(d => d.value));
              const heightPercent = (item.value / maxValue) * 100;
              
              // Get color based on index
              const colors = ['bg-blue-500', 'bg-green-500', 'bg-yellow-500', 'bg-orange-500', 'bg-purple-500'];
              const color = colors[index % colors.length];
              
              return (
                <div key={item.name} className="flex flex-col items-center flex-1">
                  <div className={`${color} w-full rounded-t-sm`} style={{ height: `${heightPercent}%` }}></div>
                  <div className="text-xs mt-1 text-center font-medium">{item.name}</div>
                  <div className="text-xs text-gray-500">{item.value}</div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
      
      {/* Top Agents by Execution Time (simplified as horizontal bars) */}
      <div className="p-4 bg-white rounded-lg shadow">
        <h4 className="text-sm font-medium text-gray-500 mb-4">Top Agents by Execution Time</h4>
        
        <div className="space-y-4">
          {topAgentsByTimeData.map((item) => {
            // Calculate relative width (0-100%)
            const maxTime = Math.max(...topAgentsByTimeData.map(d => d.time));
            const widthPercent = (item.time / maxTime) * 100;
            
            return (
              <div key={item.name}>
                <div className="flex justify-between mb-1">
                  <span className="text-sm font-medium truncate w-32">{item.name}</span>
                  <span className="text-sm font-medium">{item.time.toFixed(2)}s</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2.5">
                  <div className="bg-indigo-500 h-2.5 rounded-full" style={{ width: `${widthPercent}%` }}></div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default AgentExecutionChart;