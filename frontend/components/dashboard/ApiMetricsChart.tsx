import React from 'react';

interface ApiMetricsProps {
  data: {
    total_requests: number;
    successful_requests: number;
    failed_requests: number;
    average_response_time: number;
    success_rate: number;
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
    
    // Add some randomness to the historical values, ensure total = success + fail
    const randomFactor = () => Math.random() * 0.4 + 0.8;
    const randomSuccessRate = () => Math.random() * 0.05 + 0.95;
    
    const successRate = i === 0 ? currentData.success_rate : Math.min(100, Math.max(90, currentData.success_rate * randomSuccessRate()));
    
    // Calculate the total, successful, and failed requests
    let total = i === 0 ? currentData.total_requests : Math.floor(currentData.total_requests * randomFactor());
    const successful = Math.floor(total * (successRate / 100));
    const failed = total - successful;
    
    data.push({
      time: timeStr,
      total,
      successful,
      failed,
      avg_time: i === 0 ? currentData.average_response_time : currentData.average_response_time * randomFactor(),
      success_rate: successRate
    });
  }
  
  return data;
};

const ApiMetricsChart: React.FC<ApiMetricsProps> = ({ data }) => {
  const chartData = createHistoricalData(data);
  
  // Get the latest data point for display
  const latestData = chartData[chartData.length - 1];
  
  return (
    <div className="space-y-6">
      {/* Request Volume - Simple bar representation */}
      <div className="p-4 bg-white rounded-lg shadow">
        <h4 className="text-sm font-medium text-gray-500 mb-4">Request Volume</h4>
        
        <div className="flex flex-wrap gap-2">
          {chartData.map((item, index) => {
            // Calculate height percentage for both successful and failed requests
            const maxTotal = Math.max(...chartData.map(d => d.total));
            const successHeight = (item.successful / maxTotal) * 100;
            const failedHeight = (item.failed / maxTotal) * 100;
            
            return (
              <div key={index} className="flex flex-col items-center">
                <div className="w-8 flex flex-col-reverse">
                  {/* Failed requests (red) */}
                  {item.failed > 0 && (
                    <div 
                      className="w-full bg-red-500" 
                      style={{ height: `${failedHeight}px` }}
                    ></div>
                  )}
                  
                  {/* Successful requests (green) */}
                  {item.successful > 0 && (
                    <div 
                      className="w-full bg-green-500" 
                      style={{ height: `${successHeight}px` }}
                    ></div>
                  )}
                </div>
                <div className="text-xs mt-1">{item.time.split(':')[1]}</div>
              </div>
            );
          })}
        </div>
        
        {/* Legend */}
        <div className="flex gap-4 justify-center mt-4">
          <div className="flex items-center">
            <div className="w-3 h-3 bg-green-500 mr-1"></div>
            <span className="text-xs">Successful</span>
          </div>
          <div className="flex items-center">
            <div className="w-3 h-3 bg-red-500 mr-1"></div>
            <span className="text-xs">Failed</span>
          </div>
        </div>
      </div>
      
      {/* Response Time & Success Rate - Simple display */}
      <div className="p-4 bg-white rounded-lg shadow">
        <h4 className="text-sm font-medium text-gray-500 mb-4">Response Time & Success Rate</h4>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Current response time */}
          <div>
            <div className="text-center mb-2">
              <div className="text-3xl font-bold text-indigo-600">{latestData.avg_time.toFixed(2)} ms</div>
              <div className="text-sm text-gray-500">Average Response Time</div>
            </div>
            
            {/* Response time trend */}
            <div className="h-20 flex items-end space-x-1">
              {chartData.map((item, index) => {
                const maxTime = Math.max(...chartData.map(d => d.avg_time));
                const heightPercent = (item.avg_time / maxTime) * 100;
                
                return (
                  <div 
                    key={`time-${index}`} 
                    className="flex-1 bg-indigo-500" 
                    style={{ height: `${heightPercent}%` }}
                  ></div>
                );
              })}
            </div>
          </div>
          
          {/* Current success rate */}
          <div>
            <div className="text-center mb-2">
              <div className="text-3xl font-bold text-green-600">{latestData.success_rate.toFixed(2)}%</div>
              <div className="text-sm text-gray-500">Success Rate</div>
            </div>
            
            {/* Success rate trend */}
            <div className="h-20 flex items-end space-x-1">
              {chartData.map((item, index) => {
                // Scale from 80% to 100% for better visualization
                const heightPercent = ((item.success_rate - 80) / 20) * 100;
                
                return (
                  <div 
                    key={`rate-${index}`} 
                    className="flex-1 bg-green-500" 
                    style={{ height: `${Math.max(0, heightPercent)}%` }}
                  ></div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ApiMetricsChart;