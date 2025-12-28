"""
Tests for frontend pages

These tests use Jest and React Testing Library to test React pages.
They should be run with the frontend testing framework.
"""

# This is a Python file that contains Jest test specifications
# It will be executed by the frontend testing framework

"""
// Import necessary testing libraries
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { rest } from 'msw';
import { setupServer } from 'msw/node';

// Import pages to test
import HomePage from '../../frontend/pages/index';
import AgentsPage from '../../frontend/pages/agents/index';
import AgentDetailPage from '../../frontend/pages/agents/[id]';
import PlaygroundPage from '../../frontend/pages/playground';
import MemoryPage from '../../frontend/pages/memory';
import ChatPage from '../../frontend/pages/chat';

// Mock the Next.js router
jest.mock('next/router', () => ({
  useRouter: () => ({
    push: jest.fn(),
    pathname: '/',
    query: {},
  }),
}));

// Set up mock API server
const server = setupServer(
  // Mock API endpoints
  rest.get('/api/agents', (req, res, ctx) => {
    return res(ctx.json({
      agents: [
        { id: 'agent1', name: 'Agent 1', description: 'First test agent' },
        { id: 'agent2', name: 'Agent 2', description: 'Second test agent' },
      ]
    }));
  }),
  
  rest.get('/api/agents/:id', (req, res, ctx) => {
    const { id } = req.params;
    return res(ctx.json({
      id,
      name: `Agent ${id}`,
      description: `Description for agent ${id}`,
      capabilities: ['test', 'mock'],
    }));
  }),
  
  rest.get('/api/memory', (req, res, ctx) => {
    return res(ctx.json({
      keys: ['key1', 'key2', 'key3'],
    }));
  }),
  
  rest.get('/api/memory/:key', (req, res, ctx) => {
    const { key } = req.params;
    return res(ctx.json({
      [key]: `Value for ${key}`,
    }));
  }),
  
  rest.post('/api/agents/execute/:id', (req, res, ctx) => {
    const { id } = req.params;
    return res(ctx.json({
      result: `Result from agent ${id}`,
    }));
  }),
);

// Enable API mocking before tests
beforeAll(() => server.listen());
// Reset any request handlers that we may add during the tests
afterEach(() => server.resetHandlers());
// Disable API mocking after the tests are done
afterAll(() => server.close());

// Home page tests
describe('Home Page', () => {
  test('renders welcome message', () => {
    render(<HomePage />);
    
    expect(screen.getByText(/welcome to sankalpa/i)).toBeInTheDocument();
  });

  test('renders navigation links', () => {
    render(<HomePage />);
    
    expect(screen.getByText('Playground')).toBeInTheDocument();
    expect(screen.getByText('Agents')).toBeInTheDocument();
    expect(screen.getByText('Memory')).toBeInTheDocument();
  });
});

// Agents page tests
describe('Agents Page', () => {
  test('renders list of agents', async () => {
    render(<AgentsPage />);
    
    // Wait for the agents to load
    await waitFor(() => {
      expect(screen.getByText('Agent 1')).toBeInTheDocument();
      expect(screen.getByText('Agent 2')).toBeInTheDocument();
    });
  });

  test('navigates to agent detail page when agent is clicked', async () => {
    const mockRouter = {
      push: jest.fn(),
      pathname: '/agents',
      query: {},
    };
    
    // Override the router mock for this test
    require('next/router').useRouter.mockReturnValue(mockRouter);
    
    render(<AgentsPage />);
    
    // Wait for the agents to load
    await waitFor(() => {
      expect(screen.getByText('Agent 1')).toBeInTheDocument();
    });
    
    // Click on an agent
    fireEvent.click(screen.getByText('Agent 1'));
    
    // Check that router.push was called with the correct path
    expect(mockRouter.push).toHaveBeenCalledWith('/agents/agent1');
  });
});

// Agent detail page tests
describe('Agent Detail Page', () => {
  test('renders agent details', async () => {
    // Set up the router mock to include the agent ID
    const mockRouter = {
      push: jest.fn(),
      pathname: '/agents/[id]',
      query: { id: 'agent1' },
    };
    
    require('next/router').useRouter.mockReturnValue(mockRouter);
    
    render(<AgentDetailPage />);
    
    // Wait for the agent details to load
    await waitFor(() => {
      expect(screen.getByText('Agent agent1')).toBeInTheDocument();
      expect(screen.getByText('Description for agent agent1')).toBeInTheDocument();
    });
  });

  test('executes agent when run button is clicked', async () => {
    // Set up the router mock to include the agent ID
    const mockRouter = {
      push: jest.fn(),
      pathname: '/agents/[id]',
      query: { id: 'agent1' },
    };
    
    require('next/router').useRouter.mockReturnValue(mockRouter);
    
    render(<AgentDetailPage />);
    
    // Wait for the agent details to load
    await waitFor(() => {
      expect(screen.getByText('Agent agent1')).toBeInTheDocument();
    });
    
    // Enter input
    fireEvent.change(screen.getByLabelText('Input'), {
      target: { value: 'Test input' },
    });
    
    // Click run button
    fireEvent.click(screen.getByText('Run Agent'));
    
    // Wait for the result
    await waitFor(() => {
      expect(screen.getByText('Result from agent agent1')).toBeInTheDocument();
    });
  });
});

// Playground page tests
describe('Playground Page', () => {
  test('renders playground interface', () => {
    render(<PlaygroundPage />);
    
    expect(screen.getByText('Sankalpa Playground')).toBeInTheDocument();
    expect(screen.getByLabelText('Input')).toBeInTheDocument();
    expect(screen.getByText('Run')).toBeInTheDocument();
  });

  test('displays results when run button is clicked', async () => {
    render(<PlaygroundPage />);
    
    // Enter input
    fireEvent.change(screen.getByLabelText('Input'), {
      target: { value: 'Test playground input' },
    });
    
    // Select an agent
    fireEvent.change(screen.getByLabelText('Agent'), {
      target: { value: 'agent1' },
    });
    
    // Click run button
    fireEvent.click(screen.getByText('Run'));
    
    // Wait for the result
    await waitFor(() => {
      expect(screen.getByText('Result from agent agent1')).toBeInTheDocument();
    });
  });
});

// Memory page tests
describe('Memory Page', () => {
  test('renders memory interface', async () => {
    render(<MemoryPage />);
    
    expect(screen.getByText('Memory Manager')).toBeInTheDocument();
    
    // Wait for memory keys to load
    await waitFor(() => {
      expect(screen.getByText('key1')).toBeInTheDocument();
      expect(screen.getByText('key2')).toBeInTheDocument();
      expect(screen.getByText('key3')).toBeInTheDocument();
    });
  });

  test('displays memory value when key is clicked', async () => {
    render(<MemoryPage />);
    
    // Wait for memory keys to load
    await waitFor(() => {
      expect(screen.getByText('key1')).toBeInTheDocument();
    });
    
    // Click on a key
    fireEvent.click(screen.getByText('key1'));
    
    // Wait for the value to load
    await waitFor(() => {
      expect(screen.getByText('Value for key1')).toBeInTheDocument();
    });
  });
});

// Chat page tests
describe('Chat Page', () => {
  test('renders chat interface', () => {
    render(<ChatPage />);
    
    expect(screen.getByText('Chat')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Type your message...')).toBeInTheDocument();
    expect(screen.getByText('Send')).toBeInTheDocument();
  });

  test('sends message when send button is clicked', () => {
    // Mock the WebSocket
    const mockSend = jest.fn();
    global.WebSocket = jest.fn(() => ({
      send: mockSend,
      addEventListener: jest.fn(),
      removeEventListener: jest.fn(),
    }));
    
    render(<ChatPage />);
    
    // Type a message
    fireEvent.change(screen.getByPlaceholderText('Type your message...'), {
      target: { value: 'Hello, agent!' },
    });
    
    // Click send button
    fireEvent.click(screen.getByText('Send'));
    
    // Check that the message was sent
    expect(mockSend).toHaveBeenCalledWith(expect.stringContaining('Hello, agent!'));
  });
});
"""
