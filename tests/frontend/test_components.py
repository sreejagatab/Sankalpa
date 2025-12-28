"""
Tests for frontend components

These tests use Jest and React Testing Library to test React components.
They should be run with the frontend testing framework.
"""

# This is a Python file that contains Jest test specifications
# It will be executed by the frontend testing framework

"""
// Import necessary testing libraries
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';

// Import components to test
import { AgentCard } from '../../frontend/components/AgentCard';
import { ChatMessage } from '../../frontend/components/ChatMessage';
import { MemoryViewer } from '../../frontend/components/MemoryViewer';
import { Sidebar } from '../../frontend/components/Sidebar';
import { WebSocketProvider } from '../../frontend/components/WebSocketProvider';

// Mock the Next.js router
jest.mock('next/router', () => ({
  useRouter: () => ({
    push: jest.fn(),
    pathname: '/',
    query: {},
  }),
}));

// AgentCard component tests
describe('AgentCard Component', () => {
  const mockAgent = {
    id: 'test-agent',
    name: 'Test Agent',
    description: 'A test agent',
    capabilities: ['test', 'mock'],
    status: 'active',
  };

  test('renders agent information correctly', () => {
    render(<AgentCard agent={mockAgent} />);
    
    expect(screen.getByText('Test Agent')).toBeInTheDocument();
    expect(screen.getByText('A test agent')).toBeInTheDocument();
    expect(screen.getByText('test')).toBeInTheDocument();
    expect(screen.getByText('mock')).toBeInTheDocument();
  });

  test('executes agent when run button is clicked', async () => {
    const onRunMock = jest.fn();
    render(<AgentCard agent={mockAgent} onRun={onRunMock} />);
    
    fireEvent.click(screen.getByText('Run'));
    
    expect(onRunMock).toHaveBeenCalledWith('test-agent');
  });
});

// ChatMessage component tests
describe('ChatMessage Component', () => {
  test('renders user message correctly', () => {
    const userMessage = {
      id: '1',
      sender: 'user',
      content: 'Hello, world!',
      timestamp: new Date().toISOString(),
    };
    
    render(<ChatMessage message={userMessage} />);
    
    expect(screen.getByText('Hello, world!')).toBeInTheDocument();
    expect(screen.getByTestId('user-avatar')).toBeInTheDocument();
  });

  test('renders agent message correctly', () => {
    const agentMessage = {
      id: '2',
      sender: 'agent',
      content: 'Hello, human!',
      timestamp: new Date().toISOString(),
      agentName: 'Test Agent',
    };
    
    render(<ChatMessage message={agentMessage} />);
    
    expect(screen.getByText('Hello, human!')).toBeInTheDocument();
    expect(screen.getByText('Test Agent')).toBeInTheDocument();
    expect(screen.getByTestId('agent-avatar')).toBeInTheDocument();
  });
});

// MemoryViewer component tests
describe('MemoryViewer Component', () => {
  const mockMemoryData = {
    'key1': 'value1',
    'key2': { nested: 'value2' },
    'key3': ['item1', 'item2'],
  };

  test('renders memory data correctly', () => {
    render(<MemoryViewer data={mockMemoryData} />);
    
    expect(screen.getByText('key1')).toBeInTheDocument();
    expect(screen.getByText('key2')).toBeInTheDocument();
    expect(screen.getByText('key3')).toBeInTheDocument();
    expect(screen.getByText('value1')).toBeInTheDocument();
  });

  test('expands nested objects when clicked', () => {
    render(<MemoryViewer data={mockMemoryData} />);
    
    fireEvent.click(screen.getByText('key2'));
    
    expect(screen.getByText('nested')).toBeInTheDocument();
    expect(screen.getByText('value2')).toBeInTheDocument();
  });
});

// Sidebar component tests
describe('Sidebar Component', () => {
  const mockNavItems = [
    { name: 'Home', path: '/' },
    { name: 'Agents', path: '/agents' },
    { name: 'Memory', path: '/memory' },
  ];

  test('renders navigation items correctly', () => {
    render(<Sidebar navItems={mockNavItems} />);
    
    expect(screen.getByText('Home')).toBeInTheDocument();
    expect(screen.getByText('Agents')).toBeInTheDocument();
    expect(screen.getByText('Memory')).toBeInTheDocument();
  });

  test('highlights active item based on current path', () => {
    render(<Sidebar navItems={mockNavItems} activePath="/agents" />);
    
    const activeItem = screen.getByText('Agents').closest('li');
    expect(activeItem).toHaveClass('active');
  });
});

// WebSocketProvider component tests
describe('WebSocketProvider Component', () => {
  // Mock WebSocket
  const mockWebSocket = {
    send: jest.fn(),
    close: jest.fn(),
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
  };
  
  // Mock window.WebSocket
  global.WebSocket = jest.fn(() => mockWebSocket);

  test('provides WebSocket context to children', () => {
    const TestConsumer = () => {
      const { connected, sendMessage } = React.useContext(WebSocketContext);
      return (
        <div>
          <span data-testid="connection-status">{connected ? 'Connected' : 'Disconnected'}</span>
          <button onClick={() => sendMessage('test')}>Send</button>
        </div>
      );
    };

    render(
      <WebSocketProvider url="ws://localhost:8000/ws">
        <TestConsumer />
      </WebSocketProvider>
    );
    
    // Initially disconnected
    expect(screen.getByTestId('connection-status')).toHaveTextContent('Disconnected');
    
    // Simulate connection
    const connectHandler = mockWebSocket.addEventListener.mock.calls.find(call => call[0] === 'open')[1];
    connectHandler();
    
    // Now connected
    expect(screen.getByTestId('connection-status')).toHaveTextContent('Connected');
    
    // Test sending a message
    fireEvent.click(screen.getByText('Send'));
    expect(mockWebSocket.send).toHaveBeenCalledWith('test');
  });
});
"""
