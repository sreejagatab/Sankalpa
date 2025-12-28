import React, { useState, useEffect, useRef } from 'react';
import { Agent } from './AgentCard';
import { useWebSocket } from '../collaboration/WebSocketProvider';

interface AgentChatProps {
  agents: Agent[];
  onAgentSelect?: (agent: Agent) => void;
}

interface ChatMessage {
  id: string;
  sender: string;
  senderType: 'user' | 'agent' | 'system';
  content: string;
  timestamp: Date;
  agentId?: string;
}

const AgentChat: React.FC<AgentChatProps> = ({ agents, onAgentSelect }) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [selectedAgent, setSelectedAgent] = useState<Agent | null>(null);
  const [isAgentResponding, setIsAgentResponding] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  const { connected, sendMessage, messages: wsMessages, joinRoom } = useWebSocket();

  // Scroll to bottom of messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Add system welcome message on mount
  useEffect(() => {
    if (messages.length === 0) {
      setMessages([
        {
          id: 'welcome',
          sender: 'System',
          senderType: 'system',
          content: 'Welcome to Sankalpa Agent Chat! Select an agent to get started or type a message to use the default assistant.',
          timestamp: new Date()
        }
      ]);
    }
  }, []);

  // Process incoming WebSocket messages if available
  useEffect(() => {
    if (wsMessages && wsMessages.length > 0) {
      const formattedMessages = wsMessages.map(msg => {
        // Transform WebSocket messages to our chat format
        return {
          id: msg.id || `ws-${Date.now()}`,
          sender: msg.sender || 'Agent',
          senderType: msg.sender_type || 'agent',
          content: msg.content,
          timestamp: new Date(msg.timestamp || Date.now()),
          agentId: msg.agent_id
        };
      });
      
      setMessages(prev => [...prev, ...formattedMessages]);
    }
  }, [wsMessages]);

  // Join agent chat room on mount
  useEffect(() => {
    if (connected && joinRoom) {
      joinRoom('agent-chat');
    }
  }, [connected, joinRoom]);

  const handleAgentSelect = (agent: Agent) => {
    setSelectedAgent(agent);
    
    if (onAgentSelect) {
      onAgentSelect(agent);
    }
    
    // Add system message about agent selection
    const systemMessage: ChatMessage = {
      id: `system-${Date.now()}`,
      sender: 'System',
      senderType: 'system',
      content: `You've selected ${agent.name}. How can I help you with ${agent.category} tasks?`,
      timestamp: new Date()
    };
    
    setMessages(prev => [...prev, systemMessage]);
  };

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;
    
    // Store the message for later use
    const messageText = inputMessage.trim();
    setInputMessage('');
    
    // Add user message
    const userMessage: ChatMessage = {
      id: `user-${Date.now()}`,
      sender: 'You',
      senderType: 'user',
      content: messageText,
      timestamp: new Date()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setIsAgentResponding(true);
    
    // If using real WebSocket, send message
    if (connected && sendMessage) {
      sendMessage({
        content: messageText,
        agent_id: selectedAgent?.id,
        room_id: 'agent-chat'
      });
      
      // Wait for response via WebSocket - handle in the useEffect for wsMessages
    } else {
      // Try to call the real API first
      try {
        const agentId = selectedAgent?.id || 'default';
        const response = await fetch('/api/agents/execute', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            agent_name: agentId,
            input_data: { input: messageText }
          })
        });
        
        if (response.ok) {
          const result = await response.json();
          console.log('API response:', result);
          
          // Extract the result
          let responseText = '';
          if (result && result.result) {
            if (typeof result.result === 'string') {
              responseText = result.result;
            } else if (typeof result.result === 'object') {
              // Format the JSON response nicely
              responseText = `Result:\n\`\`\`json\n${JSON.stringify(result.result, null, 2)}\n\`\`\``;
            }
          } else {
            // If we get an unexpected response format
            responseText = `Received response from ${agentId} agent.\n\n\`\`\`json\n${JSON.stringify(result, null, 2)}\n\`\`\``;
          }
          
          // Add agent message
          const agentName = selectedAgent ? selectedAgent.name : 'Assistant';
          const agentMessage: ChatMessage = {
            id: `agent-${Date.now()}`,
            sender: agentName,
            senderType: 'agent',
            content: responseText,
            timestamp: new Date(),
            agentId: selectedAgent?.id
          };
          
          setMessages(prev => [...prev, agentMessage]);
          setIsAgentResponding(false);
          return;
        }
      } catch (error) {
        console.warn('API call failed, falling back to mock responses:', error);
        // Fall through to mock responses if API fails
      }
      
      // Fallback to mock responses
      setTimeout(() => {
        const agentName = selectedAgent ? selectedAgent.name : 'Assistant';
        const agentMessage: ChatMessage = {
          id: `agent-${Date.now()}`,
          sender: agentName,
          senderType: 'agent',
          content: generateMockResponse(messageText, selectedAgent),
          timestamp: new Date(),
          agentId: selectedAgent?.id
        };
        
        setMessages(prev => [...prev, agentMessage]);
        setIsAgentResponding(false);
      }, 1500);
    }
  };

  const generateMockResponse = (message: string, agent: Agent | null): string => {
    if (!agent) {
      return `I'm the default assistant. I can help you with general questions or direct you to a specialized agent. What would you like to know?`;
    }
    
    switch(agent.category) {
      case 'builder':
        return `As a ${agent.name}, I can help you build and structure your code. Based on your message "${message}", I'd suggest starting with a component architecture diagram. What specific part would you like me to help with first?`;
      case 'testing':
        return `I'm specialized in testing. For your request "${message}", I recommend setting up unit tests using Jest or Cypress for UI components. Would you like me to generate some test cases?`;
      case 'deployment':
        return `I can assist with deploying your application. Regarding "${message}", we should first set up a CI/CD pipeline. Are you using GitHub Actions, GitLab CI, or another platform?`;
      case 'enhanced':
        return `As an enhanced agent, I can provide deeper analysis. For "${message}", I'd recommend exploring these options: 1) Optimize for performance, 2) Add type safety, 3) Improve code readability. Which would you like to focus on?`;
      default:
        return `I'm ${agent.name}. I'll help you with "${message}" from a ${agent.category} perspective. Let's break this down into actionable steps. First, can you tell me more about your specific goals?`;
    }
  };
  
  const renderMessage = (message: ChatMessage) => {
    const isUserMessage = message.senderType === 'user';
    const isSystemMessage = message.senderType === 'system';
    
    if (isSystemMessage) {
      return (
        <div key={message.id} className="flex justify-center my-2">
          <div className="bg-gray-100 px-4 py-2 rounded-lg max-w-md text-sm text-gray-600">
            {message.content}
          </div>
        </div>
      );
    }
    
    return (
      <div key={message.id} className={`flex ${isUserMessage ? 'justify-end' : 'justify-start'} mb-4`}>
        <div className="flex flex-col max-w-md">
          <div className={`flex items-center ${isUserMessage ? 'justify-end' : 'justify-start'} mb-1`}>
            <span className="text-xs text-gray-500 mr-2">
              {message.timestamp.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
            </span>
            <span className="font-medium text-sm">{message.sender}</span>
          </div>
          <div className={`px-4 py-3 rounded-lg ${isUserMessage ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-800'}`}>
            {message.content}
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="flex flex-col h-full">
      <div className="bg-white shadow-sm border-b p-4">
        <h2 className="text-lg font-medium text-gray-900">Agent Chat</h2>
        <p className="text-sm text-gray-500">Chat with our intelligent agents</p>
      </div>
      
      <div className="flex-grow flex overflow-hidden">
        {/* Agent Selector Sidebar */}
        <div className="w-72 border-r bg-gray-50 overflow-y-auto">
          <div className="p-4">
            <h3 className="text-sm font-medium text-gray-700 mb-3">Available Agents</h3>
            <div className="space-y-2">
              {agents.map(agent => (
                <button
                  key={agent.id}
                  onClick={() => handleAgentSelect(agent)}
                  className={`w-full flex items-center p-2 rounded-lg text-left transition-colors ${selectedAgent?.id === agent.id ? 'bg-blue-100 text-blue-800' : 'hover:bg-gray-100'}`}
                >
                  <div className="flex-shrink-0 h-10 w-10 rounded-full bg-gray-200 flex items-center justify-center text-gray-500">
                    {agent.avatar ? (
                      <img src={agent.avatar} alt={agent.name} className="h-10 w-10 rounded-full" />
                    ) : (
                      agent.name.charAt(0).toUpperCase()
                    )}
                  </div>
                  <div className="ml-3">
                    <p className="text-sm font-medium">{agent.name}</p>
                    <p className="text-xs text-gray-500 truncate">{agent.category}</p>
                  </div>
                </button>
              ))}
            </div>
          </div>
        </div>
        
        {/* Chat Area */}
        <div className="flex-grow flex flex-col bg-white">
          {/* Messages */}
          <div className="flex-grow p-4 overflow-y-auto">
            <div className="space-y-4">
              {messages.map(message => renderMessage(message))}
              {isAgentResponding && (
                <div className="flex justify-start mb-4">
                  <div className="bg-gray-200 text-gray-800 px-4 py-3 rounded-lg flex items-center space-x-2">
                    <div className="h-2 w-2 bg-gray-500 rounded-full animate-bounce"></div>
                    <div className="h-2 w-2 bg-gray-500 rounded-full animate-bounce delay-75"></div>
                    <div className="h-2 w-2 bg-gray-500 rounded-full animate-bounce delay-150"></div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          </div>
          
          {/* Message Input */}
          <div className="border-t p-4">
            <div className="flex items-center">
              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                className="flex-grow rounded-lg border border-gray-300 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Type your message..."
              />
              <button
                onClick={handleSendMessage}
                disabled={!inputMessage.trim()}
                className="ml-2 px-4 py-2 bg-blue-600 text-white rounded-lg disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Send
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AgentChat;