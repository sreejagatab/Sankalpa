import React from 'react';

interface SystemMetricsProps {
  data: {
    cpu_percent: number;
    memory_percent: number;
    disk_percent: number;
    [key: string]: any;
  };
}

// Create fake historical data for demo purposes
const createHistoricalData = (currentData: any) => {
  const data = [];
  const now = new Date();
  
  // Generate data for the last 15 minutes
  for (let i = 14; i >= 0; i--) {
    const time = new Date(now.getTime() - i * 60000);
    const timeStr = time.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    
    // Add some randomness to the historical values
    const randomFactor = () => Math.random() * 0.2 + 0.9;
    
    data.push({
      time: timeStr,
      cpu: i === 0 ? currentData.cpu_percent : Math.min(100, Math.max(0, currentData.cpu_percent * randomFactor())),
      memory: i === 0 ? currentData.memory_percent : Math.min(100, Math.max(0, currentData.memory_percent * randomFactor())),
      disk: i === 0 ? currentData.disk_percent : Math.min(100, Math.max(0, currentData.disk_percent * randomFactor())),
    });
  }
  
  return data;
};

const SystemMetricsChart: React.FC<SystemMetricsProps> = ({ data }) => {
  const chartData = createHistoricalData(data);
  
  return (
    <div className="p-4 bg-white rounded-lg shadow">
      <h4 className="text-sm font-medium text-gray-500 mb-4">System Metrics</h4>
      
      {/* Current Metrics */}
      <div className="grid grid-cols-3 gap-4 mb-6">
        <div className="text-center">
          <div className="text-2xl font-bold text-indigo-600">{data.cpu_percent}%</div>
          <div className="text-sm text-gray-500">CPU</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold text-green-600">{data.memory_percent}%</div>
          <div className="text-sm text-gray-500">Memory</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold text-yellow-600">{data.disk_percent}%</div>
          <div className="text-sm text-gray-500">Disk</div>
        </div>
      </div>
      
      {/* Metrics Over Time (simplified) */}
      <div className="h-48">
        <div className="flex h-40 items-end gap-1 mb-2">
          {chartData.map((item, idx) => (
            <div key={idx} className="flex flex-col h-full justify-end gap-1 flex-1">
              {/* CPU Usage */}
              <div 
                className="bg-indigo-500 w-full rounded-t-sm" 
                style={{ height: `${item.cpu}%` }}
                title={`CPU: ${item.cpu.toFixed(1)}% at ${item.time}`}
              ></div>
              
              {/* Memory Usage */}
              <div 
                className="bg-green-500 w-full rounded-t-sm" 
                style={{ height: `${item.memory}%` }}
                title={`Memory: ${item.memory.toFixed(1)}% at ${item.time}`}
              ></div>
              
              {/* Disk Usage */}
              <div 
                className="bg-yellow-500 w-full rounded-t-sm" 
                style={{ height: `${item.disk}%` }}
                title={`Disk: ${item.disk.toFixed(1)}% at ${item.time}`}
              ></div>
            </div>
          ))}
        </div>
        
        {/* Time labels - Only show a few for clarity */}
        <div className="flex justify-between text-xs text-gray-500">
          <span>{chartData[0].time}</span>
          <span>{chartData[Math.floor(chartData.length / 2)].time}</span>
          <span>{chartData[chartData.length - 1].time}</span>
        </div>
      </div>
      
      {/* Legend */}
      <div className="flex justify-center gap-4 mt-2">
        <div className="flex items-center">
          <div className="w-3 h-3 bg-indigo-500 mr-1"></div>
          <span className="text-xs">CPU</span>
        </div>
        <div className="flex items-center">
          <div className="w-3 h-3 bg-green-500 mr-1"></div>
          <span className="text-xs">Memory</span>
        </div>
        <div className="flex items-center">
          <div className="w-3 h-3 bg-yellow-500 mr-1"></div>
          <span className="text-xs">Disk</span>
        </div>
      </div>
    </div>
  );
};

export default SystemMetricsChart;