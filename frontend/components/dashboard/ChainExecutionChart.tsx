import React from 'react';

interface ChainExecutionProps {
  data: {
    total_executions: number;
    successful_executions: number;
    failed_executions: number;
    average_execution_time: number;
    success_rate: number;
  };
}

// Create mock historical chain execution data
const createHistoricalData = () => {
  const data = [];
  const now = new Date();
  
  // Chain types
  const chainTypes = ['sequential', 'parallel', 'conditional'];
  
  // Generate data for the last 15 days
  for (let i = 14; i >= 0; i--) {
    const date = new Date(now.getTime() - i * 24 * 60 * 60 * 1000);
    const dateStr = date.toLocaleDateString([], { month: 'short', day: 'numeric' });
    
    // Generate random execution counts for each chain type
    const sequential = Math.floor(Math.random() * 20) + 10;
    const parallel = Math.floor(Math.random() * 15) + 5;
    const conditional = Math.floor(Math.random() * 10) + 3;
    
    data.push({
      date: dateStr,
      sequential,
      parallel,
      conditional,
      total: sequential + parallel + conditional
    });
  }
  
  return data;
};

// Mock data for chain type distribution
const chainTypeData = [
  { name: 'Sequential', value: 62, color: 'bg-blue-500' },
  { name: 'Parallel', value: 26, color: 'bg-green-500' },
  { name: 'Conditional', value: 12, color: 'bg-yellow-500' }
];

// Mock data for popular chain templates
const popularChainTemplates = [
  { name: 'Full-Stack App', executions: 86, success_rate: 94 },
  { name: 'Blog Generator', executions: 73, success_rate: 97 },
  { name: 'API Builder', executions: 65, success_rate: 92 },
  { name: 'Test Suite', executions: 54, success_rate: 89 },
  { name: 'Deployment Pipeline', executions: 43, success_rate: 91 }
];

const ChainExecutionChart: React.FC<ChainExecutionProps> = ({ data }) => {
  const historicalData = createHistoricalData();
  
  return (
    <div className="space-y-6">
      {/* Chain Executions Over Time */}
      <div className="p-4 bg-white rounded-lg shadow">
        <h4 className="text-sm font-medium text-gray-500 mb-4">Chain Executions Over Time</h4>
        
        <div className="h-40">
          {/* Simple line chart alternative */}
          <div className="relative h-full w-full">
            {/* Y-axis labels */}
            <div className="absolute left-0 top-0 bottom-0 flex flex-col justify-between text-xs text-gray-500">
              <span>High</span>
              <span>Med</span>
              <span>Low</span>
            </div>
            
            {/* Lines for each chain type */}
            <div className="absolute left-8 right-0 top-0 bottom-0 flex flex-col justify-between">
              {/* Grid lines */}
              <div className="border-b border-gray-200 h-1/3"></div>
              <div className="border-b border-gray-200 h-1/3"></div>
              <div className="border-b border-gray-200 h-1/3"></div>
              
              {/* Sequential line */}
              <div className="absolute top-1/6 left-0 right-0 border-t-2 border-blue-500 border-dashed"></div>
              
              {/* Parallel line */}
              <div className="absolute top-2/4 left-0 right-0 border-t-2 border-green-500 border-dashed"></div>
              
              {/* Conditional line */}
              <div className="absolute top-3/4 left-0 right-0 border-t-2 border-yellow-500 border-dashed"></div>
            </div>
          </div>
          
          {/* Legend */}
          <div className="flex justify-center gap-4 mt-4">
            <div className="flex items-center">
              <div className="w-3 h-3 bg-blue-500 mr-1"></div>
              <span className="text-xs">Sequential</span>
            </div>
            <div className="flex items-center">
              <div className="w-3 h-3 bg-green-500 mr-1"></div>
              <span className="text-xs">Parallel</span>
            </div>
            <div className="flex items-center">
              <div className="w-3 h-3 bg-yellow-500 mr-1"></div>
              <span className="text-xs">Conditional</span>
            </div>
          </div>
        </div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Chain Type Distribution */}
        <div className="p-4 bg-white rounded-lg shadow">
          <h4 className="text-sm font-medium text-gray-500 mb-4 text-center">Chain Type Distribution</h4>
          
          {/* Simple donut chart alternative */}
          <div className="relative w-40 h-40 mx-auto">
            <svg viewBox="0 0 36 36" className="w-full h-full">
              {/* Calculate stroke dasharray and dashoffset for each segment */}
              {(() => {
                const total = chainTypeData.reduce((acc, item) => acc + item.value, 0);
                let accumulatedPercent = 0;
                
                return chainTypeData.map((item, index) => {
                  const percent = (item.value / total) * 100;
                  const startPercent = accumulatedPercent;
                  accumulatedPercent += percent;
                  
                  // Calculate stroke-dasharray and stroke-dashoffset
                  const circumference = 2 * Math.PI * 16; // 2πr where r=16 (radius)
                  const dasharray = circumference;
                  const dashoffset = circumference * (1 - percent / 100);
                  const rotation = startPercent * 3.6; // 3.6 = 360/100
                  
                  return (
                    <circle
                      key={index}
                      className={item.color}
                      cx="18"
                      cy="18"
                      r="16"
                      fill="transparent"
                      strokeWidth="4"
                      strokeDasharray={`${dasharray}`}
                      strokeDashoffset={`${dashoffset}`}
                      style={{
                        transformOrigin: 'center',
                        transform: `rotate(${rotation}deg)`
                      }}
                    />
                  );
                });
              })()}
              <circle cx="18" cy="18" r="12" fill="white" />
            </svg>
          </div>
          
          {/* Legend */}
          <div className="mt-4 space-y-2">
            {chainTypeData.map((item, index) => (
              <div key={index} className="flex items-center justify-between">
                <div className="flex items-center">
                  <div className={`w-3 h-3 ${item.color} mr-2`}></div>
                  <span className="text-sm">{item.name}</span>
                </div>
                <div className="text-sm font-medium">{item.value}%</div>
              </div>
            ))}
          </div>
        </div>
        
        {/* Popular Chain Templates */}
        <div className="p-4 bg-white rounded-lg shadow">
          <h4 className="text-sm font-medium text-gray-500 mb-4 text-center">Popular Chain Templates</h4>
          <div className="max-h-48 overflow-y-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Template
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Executions
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Success Rate
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {popularChainTemplates.map((template, idx) => (
                  <tr key={idx}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {template.name}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {template.executions}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      <div className="flex items-center">
                        <span className={`mr-2 ${template.success_rate >= 95 ? 'text-green-600' : template.success_rate >= 90 ? 'text-yellow-600' : 'text-red-600'}`}>
                          {template.success_rate}%
                        </span>
                        <div className="w-20 bg-gray-200 rounded-full h-2.5">
                          <div 
                            className={`h-2.5 rounded-full ${template.success_rate >= 95 ? 'bg-green-600' : template.success_rate >= 90 ? 'bg-yellow-600' : 'bg-red-600'}`}
                            style={{ width: `${template.success_rate}%` }}
                          ></div>
                        </div>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChainExecutionChart;