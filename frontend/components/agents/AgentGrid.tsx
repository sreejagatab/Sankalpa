import React from 'react';
import AgentCard, { Agent } from './AgentCard';

interface AgentGridProps {
  agents: Agent[];
  onExecute?: (agent: Agent) => void;
}

const AgentGrid: React.FC<AgentGridProps> = ({ agents, onExecute }) => {
  return (
    <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
      {agents.map((agent) => (
        <AgentCard 
          key={agent.id} 
          agent={agent} 
          onExecute={onExecute}
        />
      ))}
    </div>
  );
};

export default AgentGrid;