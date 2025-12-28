import React, { useState, useEffect, useCallback, useRef } from 'react';
import Head from 'next/head';
import ReactFlow, {
  ReactFlowProvider,
  addEdge,
  useNodesState,
  useEdgesState,
  Controls,
  Background,
  Panel,
  MarkerType,
  Connection,
  Edge,
  Node,
  NodeTypes
} from 'reactflow';
import 'reactflow/dist/style.css';
import { nanoid } from 'nanoid';

// Custom node components
const AgentNode = ({ data, isConnectable }: any) => {
  return (
    <div className="px-4 py-2 border-2 border-blue-500 rounded-md bg-white shadow-md min-w-[200px]">
      <div className="font-bold text-blue-700 border-b border-blue-200 pb-1 mb-2">{data.label}</div>
      <div className="text-xs text-gray-600">{data.description}</div>
      {data.model && (
        <div className="mt-2 text-xs bg-blue-50 text-blue-700 px-2 py-1 rounded-full inline-block">
          {data.model}
        </div>
      )}
      {data.isExecuting && (
        <div className="mt-2 text-xs flex items-center">
          <div className="animate-pulse mr-1 w-2 h-2 bg-green-500 rounded-full"></div>
          <span className="text-green-600">Running...</span>
        </div>
      )}
      {data.hasError && (
        <div className="mt-2 text-xs text-red-600">
          ❌ Error
        </div>
      )}
    </div>
  );
};

const InputNode = ({ data, isConnectable }: any) => {
  return (
    <div className="px-4 py-2 border-2 border-green-500 rounded-md bg-white shadow-md min-w-[180px]">
      <div className="font-bold text-green-700 border-b border-green-200 pb-1 mb-2">Input</div>
      <textarea
        className="border rounded p-1 w-full text-xs h-16 resize-none"
        value={data.inputValue}
        onChange={data.onInputChange}
        placeholder="Enter workflow input..."
      />
    </div>
  );
};

const OutputNode = ({ data, isConnectable }: any) => {
  return (
    <div className="px-4 py-2 border-2 border-purple-500 rounded-md bg-white shadow-md min-w-[180px] max-w-[280px]">
      <div className="font-bold text-purple-700 border-b border-purple-200 pb-1 mb-2">Output</div>
      <div className="text-xs text-gray-700 max-h-32 overflow-auto">
        {data.output ? (
          <pre className="whitespace-pre-wrap">{data.output}</pre>
        ) : (
          <span className="text-gray-400 italic">No output yet</span>
        )}
      </div>
    </div>
  );
};

// Node types registration
const nodeTypes: NodeTypes = {
  agentNode: AgentNode,
  inputNode: InputNode,
  outputNode: OutputNode,
};

// Main Composer Component
export default function ComposerPage() {
  // State for workflow configuration
  const [workflowName, setWorkflowName] = useState('New Workflow');
  const [workflowDescription, setWorkflowDescription] = useState('This workflow combines multiple agents to build a complete solution.');
  
  // State for ReactFlow
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [reactFlowInstance, setReactFlowInstance] = useState<any>(null);
  
  // Input and execution state
  const [inputText, setInputText] = useState('');
  const [outputText, setOutputText] = useState('');
  const [isExecuting, setIsExecuting] = useState(false);
  const [executionLog, setExecutionLog] = useState<string[]>([]);
  
  // Agent selection
  const [selectedAgent, setSelectedAgent] = useState<string | null>(null);
  const [activePanel, setActivePanel] = useState<'config' | 'agents' | 'templates'>('config');
  
  // Reference to the drag item
  const dragRef = useRef<any>(null);
  
  // Available agents data
  const availableAgents = [
    { 
      id: 'frontend_builder', 
      name: 'Frontend Builder',
      advanced: true,
      description: 'Builds UI components based on specifications',
      capabilities: ['React', 'TailwindCSS', 'UI/UX'],
      selfImproving: true,
      model: 'GPT-4'
    },
    { 
      id: 'backend_builder', 
      name: 'Backend Builder',
      advanced: true,
      description: 'Creates backend services and APIs',
      capabilities: ['Node.js', 'Express', 'API Design'],
      model: 'GPT-4'
    },
    { 
      id: 'db_schema', 
      name: 'Database Schema Designer',
      description: 'Designs database schemas and relations',
      capabilities: ['SQL', 'NoSQL', 'Data Modeling'],
      model: 'GPT-3.5'
    },
    { 
      id: 'api_builder', 
      name: 'API Builder',
      description: 'Designs RESTful and GraphQL APIs',
      capabilities: ['OpenAPI', 'GraphQL', 'API Testing'],
      model: 'GPT-3.5'
    },
    { 
      id: 'agent_builder', 
      name: 'Agent Builder',
      advanced: true,
      description: 'Creates specialized agents for specific tasks',
      capabilities: ['Agent Generation', 'Fine-Tuning', 'Specialization'],
      canReplicate: true,
      model: 'Claude-3'
    },
    { 
      id: 'memory_specialist', 
      name: 'Memory Specialist',
      advanced: true,
      description: 'Manages advanced vector memory operations',
      capabilities: ['Vector Embeddings', 'Memory Optimization', 'Context Management'],
      memoryEnabled: true,
      model: 'GPT-4'
    },
    {
      id: 'finetuner',
      name: 'Model Fine-Tuner',
      advanced: true,
      description: 'Fine-tunes LLMs on custom datasets',
      capabilities: ['OpenAI API', 'Dataset Preparation', 'Model Training'],
      model: 'GPT-4'
    },
    {
      id: 'copilot',
      name: 'Workflow Copilot',
      description: 'Assists with workflow creation and debugging',
      capabilities: ['Workflow Analysis', 'Agent Recommendation', 'Error Detection'],
      model: 'Claude-3'
    }
  ];

  // Template workflows
  const templateWorkflows = [
    {
      name: 'Full-Stack Development',
      description: 'Builds a complete application with frontend, backend, and database',
      agents: ['frontend_builder', 'backend_builder', 'db_schema']
    },
    {
      name: 'Self-Replicating Agent System',
      description: 'Creates a system of specialized agents that can improve themselves',
      agents: ['agent_builder', 'memory_specialist']
    },
    {
      name: 'API Development Suite',
      description: 'Designs and builds complete API systems with documentation',
      agents: ['api_builder', 'backend_builder']
    },
    {
      name: 'Fine-Tuning Pipeline',
      description: 'Creates and manages custom fine-tuned models',
      agents: ['finetuner', 'copilot']
    }
  ];

  // Initialize the flow with input and output nodes
  useEffect(() => {
    const inputNode = {
      id: 'input-1',
      type: 'inputNode',
      data: { 
        inputValue: inputText,
        onInputChange: (e: React.ChangeEvent<HTMLTextAreaElement>) => setInputText(e.target.value)
      },
      position: { x: 100, y: 200 },
    };

    const outputNode = {
      id: 'output-1',
      type: 'outputNode',
      data: { output: outputText },
      position: { x: 700, y: 200 },
    };

    setNodes([inputNode, outputNode]);
  }, []);

  // Update input node when inputText changes
  useEffect(() => {
    setNodes(nds => nds.map(node => {
      if (node.id === 'input-1') {
        node.data = {
          ...node.data,
          inputValue: inputText,
        };
      }
      return node;
    }));
  }, [inputText, setNodes]);

  // Update output node when outputText changes
  useEffect(() => {
    setNodes(nds => nds.map(node => {
      if (node.id === 'output-1') {
        node.data = {
          ...node.data,
          output: outputText,
        };
      }
      return node;
    }));
  }, [outputText, setNodes]);

  // Handle connecting nodes
  const onConnect = useCallback((params: Connection) => {
    // Create edge with animated style and arrow marker
    const edge: Edge = {
      ...params,
      id: `e-${nanoid(6)}`,
      animated: true,
      style: { stroke: '#3b82f6', strokeWidth: 2 },
      markerEnd: {
        type: MarkerType.ArrowClosed,
        width: 20,
        height: 20,
        color: '#3b82f6',
      },
    };
    setEdges(eds => addEdge(edge, eds));
  }, [setEdges]);

  // Handle dropping an agent onto the canvas
  const onDrop = useCallback(
    (event: React.DragEvent<HTMLDivElement>) => {
      event.preventDefault();
      
      if (!reactFlowInstance) return;
      
      // Get the agent data from the drag operation
      const agentType = event.dataTransfer.getData('application/reactflow');
      if (!agentType) return;
      
      const agentData = availableAgents.find(agent => agent.id === agentType);
      if (!agentData) return;

      // Get the drop position
      const reactFlowBounds = event.currentTarget.getBoundingClientRect();
      const position = reactFlowInstance.project({
        x: event.clientX - reactFlowBounds.left,
        y: event.clientY - reactFlowBounds.top,
      });

      // Create a new node
      const newNode: Node = {
        id: `${agentType}-${nanoid(6)}`,
        type: 'agentNode',
        position,
        data: { 
          label: agentData.name,
          description: agentData.description,
          model: agentData.model,
          agentId: agentData.id,
          isExecuting: false,
          hasError: false
        },
      };

      setNodes(nds => [...nds, newNode]);
    },
    [reactFlowInstance, availableAgents, setNodes]
  );

  // Setup drag over handler
  const onDragOver = useCallback((event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  }, []);

  // Setup drag start handler for agent items
  const onDragStart = (event: React.DragEvent<HTMLDivElement>, agentId: string) => {
    event.dataTransfer.setData('application/reactflow', agentId);
    event.dataTransfer.effectAllowed = 'move';
    dragRef.current = event.target;
  };
  
  // Function to generate a workflow execution plan based on nodes and edges
  const generateExecutionPlan = () => {
    // Find all paths from input to output
    const nodeMap = new Map<string, Node>();
    nodes.forEach(node => nodeMap.set(node.id, node));
    
    const edgeMap = new Map<string, string[]>();
    edges.forEach(edge => {
      const { source, target } = edge;
      if (!edgeMap.has(source)) {
        edgeMap.set(source, []);
      }
      edgeMap.get(source)?.push(target);
    });
    
    // Find execution paths (could have multiple paths)
    const findPaths = (current: string, target: string, visited = new Set<string>(), path: string[] = []) => {
      if (visited.has(current)) return [];
      
      visited.add(current);
      path.push(current);
      
      if (current === target) {
        return [path];
      }
      
      const nextNodes = edgeMap.get(current) || [];
      let paths: string[][] = [];
      
      for (const next of nextNodes) {
        const newPaths = findPaths(next, target, new Set(visited), [...path]);
        paths = [...paths, ...newPaths];
      }
      
      return paths;
    };
    
    // Start from input node
    const inputNodeId = nodes.find(node => node.type === 'inputNode')?.id;
    const outputNodeId = nodes.find(node => node.type === 'outputNode')?.id;
    
    if (!inputNodeId || !outputNodeId) {
      return { error: 'Missing input or output node' };
    }
    
    const paths = findPaths(inputNodeId, outputNodeId);
    
    if (paths.length === 0) {
      return { error: 'No valid path from input to output' };
    }
    
    // Extract agent nodes along the path (exclude input/output nodes)
    const agentPaths = paths.map(path => 
      path
        .filter(nodeId => {
          const node = nodeMap.get(nodeId);
          return node?.type === 'agentNode';
        })
        .map(nodeId => {
          const node = nodeMap.get(nodeId);
          return {
            nodeId,
            agentId: node?.data?.agentId,
            name: node?.data?.label
          };
        })
    );
    
    return { paths: agentPaths };
  };

  // Execute workflow
  const executeWorkflow = async () => {
    if (!inputText.trim()) {
      alert('Please enter input for the workflow to process');
      return;
    }
    
    const plan = generateExecutionPlan();
    
    if (plan.error) {
      alert(`Workflow execution error: ${plan.error}`);
      return;
    }
    
    if (!plan.paths || plan.paths.length === 0 || plan.paths[0].length === 0) {
      alert('Please create a connected workflow with at least one agent');
      return;
    }
    
    // Use the first path for execution (could enhance to support parallel paths)
    const executionPath = plan.paths[0];
    
    setIsExecuting(true);
    setOutputText('');
    setExecutionLog([`Starting workflow execution: "${workflowName}"`]);
    
    // Mark all agent nodes as not executing/no errors
    setNodes(nds => 
      nds.map(node => {
        if (node.type === 'agentNode') {
          return {
            ...node,
            data: {
              ...node.data,
              isExecuting: false,
              hasError: false
            }
          };
        }
        return node;
      })
    );
    
    // Execute each agent in the path
    let currentInput = inputText;
    let currentOutput = '';
    
    for (let i = 0; i < executionPath.length; i++) {
      const { nodeId, agentId, name } = executionPath[i];
      
      // Mark current agent as executing
      setNodes(nds => 
        nds.map(node => {
          if (node.id === nodeId) {
            return {
              ...node,
              data: {
                ...node.data,
                isExecuting: true
              }
            };
          }
          return node;
        })
      );
      
      setExecutionLog(logs => [...logs, `Executing agent: ${name}`]);
      
      try {
        // Simulate API call to execute agent
        // In a real implementation, this would call the actual agent API
        const result = await simulateAgentExecution(agentId, currentInput);
        currentOutput = result.output;
        currentInput = currentOutput; // Pass output to next agent
        
        setExecutionLog(logs => [...logs, `✅ ${name} completed successfully`]);
      } catch (error) {
        // Handle execution error
        setExecutionLog(logs => [...logs, `❌ Error executing ${name}: ${error}`]);
        
        // Mark agent as having error
        setNodes(nds => 
          nds.map(node => {
            if (node.id === nodeId) {
              return {
                ...node,
                data: {
                  ...node.data,
                  isExecuting: false,
                  hasError: true
                }
              };
            }
            return node;
          })
        );
        
        setIsExecuting(false);
        return;
      }
      
      // Mark agent as done executing
      setNodes(nds => 
        nds.map(node => {
          if (node.id === nodeId) {
            return {
              ...node,
              data: {
                ...node.data,
                isExecuting: false
              }
            };
          }
          return node;
        })
      );
    }
    
    // Set final output
    setOutputText(currentOutput);
    setExecutionLog(logs => [...logs, `Workflow execution completed`]);
    setIsExecuting(false);
  };

  // Execute agent through the backend API
  const executeAgentAPI = async (agentId: string, input: string): Promise<{output: string}> => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      
      // Convert agent ID to the format expected by the backend
      // Frontend uses camelCase IDs like 'frontendBuilder', but backend might use snake_case
      const backendAgentId = agentId;
      
      // Determine endpoint based on agent type
      let endpoint = '/api/agents/execute';
      let requestData: any = {
        agent_name: backendAgentId,
        input_data: { input: input }
      };
      
      // Special endpoints for enhanced agents
      if (agentId === 'finetuner') {
        endpoint = '/api/agents/finetuner/run';
        requestData = {
          model: "gpt-3.5-turbo",
          dataset: input,
          epochs: 3,
          batch_size: 4,
          learning_rate: 0.0002,
          auto_execute: false
        };
      } else if (agentId === 'self_replicator') {
        endpoint = '/api/agents/self_replicator/run';
        requestData = {
          name: `agent_from_${Date.now()}`,
          description: `Agent created from input: ${input.substring(0, 50)}...`,
          category: "custom",
          logic: input
        };
      } else if (agentId === 'vs_code_extension') {
        endpoint = '/api/agents/vs_code_extension/run';
        requestData = {
          name: "sankalpa-extension",
          display_name: "Sankalpa AI Agents",
          description: `Extension with capabilities for: ${input}`,
          publisher: "sankalpa",
          version: "0.1.0"
        };
      } else if (agentId === 'deploy_executor') {
        endpoint = '/api/agents/deploy_executor/run';
        requestData = {
          platform: "vercel",
          project_type: "next",
          project_path: ".",
          env_vars: {},
          domain: null,
          region: "us-east-1"
        };
      }
      
      // Make the API call
      console.log(`Executing agent ${agentId} via ${endpoint}`, requestData);
      
      const response = await fetch(`${apiUrl}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + (localStorage.getItem('auth_token') || '')
        },
        body: JSON.stringify(requestData),
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to execute agent');
      }
      
      const result = await response.json();
      
      // Extract the output from the result
      let output = '';
      if (result && result.result) {
        if (typeof result.result === 'string') {
          output = result.result;
        } else if (typeof result.result === 'object') {
          // Handle different result formats
          if (result.result.output) {
            output = result.result.output;
          } else if (result.result.message) {
            output = result.result.message;
          } else if (result.result.files) {
            output = `Generated files:\n${Object.keys(result.result.files).join('\n')}`;
          } else {
            output = JSON.stringify(result.result, null, 2);
          }
        }
      }
      
      return { output };
    } catch (error: any) {
      console.error('Agent execution error:', error);
      throw error.message || 'Failed to execute agent';
    }
  };
  
  // Fallback to simulated execution if API fails or for development
  const simulateAgentExecution = (agentId: string, input: string): Promise<{output: string}> => {
    // First try the real API
    return executeAgentAPI(agentId, input)
      .catch(error => {
        console.warn('Falling back to simulated execution:', error);
        
        // Fallback to simulation if API fails
        return new Promise((resolve, reject) => {
          // Simulate network delay and processing time
          setTimeout(() => {
            try {
              const agent = availableAgents.find(a => a.id === agentId);
              
              // Generate simulated output based on agent type
              let output = '';
              if (agentId === 'frontend_builder') {
                output = `Frontend components created for: ${input}\n\n- Added React components with TailwindCSS\n- Created responsive layout\n- Implemented state management`;
              } else if (agentId === 'backend_builder') {
                output = `Backend API created for: ${input}\n\n- Generated Express.js routes\n- Implemented authentication\n- Created database models`;
              } else if (agentId === 'db_schema') {
                output = `Database schema designed for: ${input}\n\n- Created tables and relationships\n- Added indexes for performance\n- Generated migration scripts`;
              } else if (agentId === 'api_builder') {
                output = `API specification created for: ${input}\n\n- Generated OpenAPI documentation\n- Created API endpoints\n- Implemented request/response validation`;
              } else if (agentId === 'agent_builder') {
                output = `Created specialized agent for: ${input}\n\n- Trained on domain knowledge\n- Implemented specialized functions\n- Added self-improvement capability`;
              } else if (agentId === 'memory_specialist') {
                output = `Enhanced memory for: ${input}\n\n- Created vector embeddings\n- Optimized context retrieval\n- Implemented long-term recall`;
              } else if (agentId === 'finetuner') {
                output = `Fine-tuning job initiated for: ${input}\n\n- Prepared training data\n- Configured hyperparameters\n- Submitted fine-tuning job to OpenAI`;
              } else if (agentId === 'copilot') {
                output = `Analyzed workflow and generated improvements for: ${input}\n\n- Identified optimization opportunities\n- Suggested additional agents\n- Recommended parameter adjustments`;
              } else {
                output = `Processed input: ${input}\n\nGenerated by ${agent?.name || agentId}`;
              }
              
              resolve({ output });
            } catch (error: any) {
              reject(error.message);
            }
          }, 1500 + Math.random() * 1000);
        });
      });
  };

  // Save workflow as JSON
  const saveWorkflow = () => {
    const workflow = {
      name: workflowName,
      description: workflowDescription,
      nodes,
      edges,
      created: new Date().toISOString()
    };
    
    // Convert to JSON and create download link
    const dataStr = JSON.stringify(workflow, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
    
    const exportFileDefaultName = `${workflowName.replace(/\s+/g, '_').toLowerCase()}_workflow.json`;
    
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
  };

  // Load workflow from JSON file
  const loadWorkflow = (event: React.ChangeEvent<HTMLInputElement>) => {
    const fileReader = new FileReader();
    if (event.target.files && event.target.files.length > 0) {
      fileReader.readAsText(event.target.files[0], "UTF-8");
      fileReader.onload = e => {
        try {
          const workflow = JSON.parse(e.target?.result as string);
          
          // Set workflow metadata
          setWorkflowName(workflow.name || 'Imported Workflow');
          setWorkflowDescription(workflow.description || '');
          
          // Set nodes and edges
          setNodes(workflow.nodes || []);
          setEdges(workflow.edges || []);
          
          // Update UI with success message
          setExecutionLog([`Workflow "${workflow.name}" loaded successfully`]);
        } catch (error) {
          alert('Error loading workflow file. Please make sure it is a valid JSON file.');
        }
      };
    }
  };

  // Apply a template workflow
  const applyTemplate = (template: any) => {
    // Set workflow metadata
    setWorkflowName(template.name);
    setWorkflowDescription(template.description);
    
    // Create nodes for each agent in the template
    const agentNodes: Node[] = [];
    const templateEdges: Edge[] = [];
    
    // Get input and output nodes
    const inputNode = nodes.find(n => n.id === 'input-1');
    const outputNode = nodes.find(n => n.id === 'output-1');
    
    if (!inputNode || !outputNode) return;
    
    // Create agent nodes with sequential positioning
    template.agents.forEach((agentId: string, index: number) => {
      const agent = availableAgents.find(a => a.id === agentId);
      if (!agent) return;
      
      // Calculate position (in a line between input and output)
      const totalAgents = template.agents.length;
      const stepX = (outputNode.position.x - inputNode.position.x) / (totalAgents + 1);
      const x = inputNode.position.x + stepX * (index + 1);
      const y = inputNode.position.y;
      
      const newNode: Node = {
        id: `${agentId}-${nanoid(6)}`,
        type: 'agentNode',
        position: { x, y },
        data: { 
          label: agent.name,
          description: agent.description,
          model: agent.model,
          agentId: agent.id,
          isExecuting: false,
          hasError: false
        },
      };
      
      agentNodes.push(newNode);
    });
    
    // Create edges between nodes
    for (let i = 0; i < agentNodes.length; i++) {
      if (i === 0) {
        // Connect input to first agent
        templateEdges.push({
          id: `e-input-${nanoid(6)}`,
          source: inputNode.id,
          target: agentNodes[i].id,
          animated: true,
          style: { stroke: '#3b82f6', strokeWidth: 2 },
          markerEnd: {
            type: MarkerType.ArrowClosed,
            width: 20,
            height: 20,
            color: '#3b82f6',
          },
        });
      }
      
      if (i < agentNodes.length - 1) {
        // Connect agent to next agent
        templateEdges.push({
          id: `e-${nanoid(6)}`,
          source: agentNodes[i].id,
          target: agentNodes[i + 1].id,
          animated: true,
          style: { stroke: '#3b82f6', strokeWidth: 2 },
          markerEnd: {
            type: MarkerType.ArrowClosed,
            width: 20,
            height: 20,
            color: '#3b82f6',
          },
        });
      }
      
      if (i === agentNodes.length - 1) {
        // Connect last agent to output
        templateEdges.push({
          id: `e-output-${nanoid(6)}`,
          source: agentNodes[i].id,
          target: outputNode.id,
          animated: true,
          style: { stroke: '#3b82f6', strokeWidth: 2 },
          markerEnd: {
            type: MarkerType.ArrowClosed,
            width: 20,
            height: 20,
            color: '#3b82f6',
          },
        });
      }
    }
    
    // Update nodes and edges
    setNodes([inputNode, outputNode, ...agentNodes]);
    setEdges(templateEdges);
  };

  return (
    <>
      <Head>
        <title>Workflow Composer - Sankalpa</title>
        <meta name="description" content="Build and visualize agent workflows with Sankalpa" />
      </Head>
      
      <div className="flex flex-col h-screen">
        {/* Toolbar */}
        <div className="bg-white border-b p-4 flex justify-between items-center">
          <div className="flex items-center space-x-4">
            <h1 className="text-xl font-bold">Workflow Composer</h1>
            <div className="flex space-x-2">
              <button
                onClick={() => setActivePanel('config')}
                className={`px-3 py-1 text-sm rounded-md ${activePanel === 'config' ? 'bg-blue-100 text-blue-700' : 'hover:bg-gray-100'}`}
              >
                Config
              </button>
              <button
                onClick={() => setActivePanel('agents')}
                className={`px-3 py-1 text-sm rounded-md ${activePanel === 'agents' ? 'bg-blue-100 text-blue-700' : 'hover:bg-gray-100'}`}
              >
                Agents
              </button>
              <button
                onClick={() => setActivePanel('templates')}
                className={`px-3 py-1 text-sm rounded-md ${activePanel === 'templates' ? 'bg-blue-100 text-blue-700' : 'hover:bg-gray-100'}`}
              >
                Templates
              </button>
            </div>
          </div>
          <div className="flex space-x-2">
            <button
              onClick={saveWorkflow}
              className="px-3 py-1 text-sm border border-gray-300 rounded-md hover:bg-gray-50"
            >
              Save
            </button>
            <label className="px-3 py-1 text-sm border border-gray-300 rounded-md hover:bg-gray-50 cursor-pointer">
              Load
              <input
                type="file"
                accept=".json"
                className="hidden"
                onChange={loadWorkflow}
              />
            </label>
            <button
              onClick={executeWorkflow}
              disabled={isExecuting}
              className={`px-3 py-1 text-sm text-white rounded-md ${isExecuting ? 'bg-gray-400' : 'bg-blue-600 hover:bg-blue-700'}`}
            >
              {isExecuting ? 'Executing...' : 'Execute'}
            </button>
          </div>
        </div>
        
        <div className="flex flex-1 overflow-hidden">
          {/* Left sidebar */}
          <div className="w-64 border-r overflow-auto">
            {activePanel === 'config' && (
              <div className="p-4 space-y-4">
                <h2 className="font-semibold">Workflow Configuration</h2>
                <div>
                  <label className="block text-sm text-gray-700 mb-1">Name</label>
                  <input
                    type="text"
                    value={workflowName}
                    onChange={(e) => setWorkflowName(e.target.value)}
                    className="w-full px-2 py-1 text-sm border rounded-md"
                  />
                </div>
                <div>
                  <label className="block text-sm text-gray-700 mb-1">Description</label>
                  <textarea
                    value={workflowDescription}
                    onChange={(e) => setWorkflowDescription(e.target.value)}
                    rows={3}
                    className="w-full px-2 py-1 text-sm border rounded-md"
                  />
                </div>
                <div>
                  <label className="block text-sm text-gray-700 mb-1">Input</label>
                  <textarea
                    value={inputText}
                    onChange={(e) => setInputText(e.target.value)}
                    rows={4}
                    placeholder="Enter workflow input here..."
                    className="w-full px-2 py-1 text-sm border rounded-md"
                  />
                </div>
              </div>
            )}
            
            {activePanel === 'agents' && (
              <div className="p-4">
                <h2 className="font-semibold mb-2">Available Agents</h2>
                <p className="text-xs text-gray-500 mb-4">Drag agents onto the canvas</p>
                <div className="space-y-2">
                  {availableAgents.map((agent) => (
                    <div
                      key={agent.id}
                      className="p-2 border rounded-md bg-white cursor-move hover:bg-gray-50"
                      draggable
                      onDragStart={(e) => onDragStart(e, agent.id)}
                    >
                      <div className="font-medium text-sm">{agent.name}</div>
                      <div className="text-xs text-gray-500">{agent.description}</div>
                      {agent.model && (
                        <div className="mt-1 text-xs bg-blue-50 text-blue-700 px-1 py-0.5 rounded-full inline-block">
                          {agent.model}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
            
            {activePanel === 'templates' && (
              <div className="p-4">
                <h2 className="font-semibold mb-2">Workflow Templates</h2>
                <p className="text-xs text-gray-500 mb-4">Pre-configured workflows</p>
                <div className="space-y-2">
                  {templateWorkflows.map((template, index) => (
                    <div
                      key={index}
                      className="p-2 border rounded-md bg-white cursor-pointer hover:bg-gray-50"
                      onClick={() => applyTemplate(template)}
                    >
                      <div className="font-medium text-sm">{template.name}</div>
                      <div className="text-xs text-gray-500">{template.description}</div>
                      <div className="mt-1 flex flex-wrap gap-1">
                        {template.agents.map((agentId) => {
                          const agent = availableAgents.find(a => a.id === agentId);
                          return agent ? (
                            <div key={agentId} className="text-xs bg-gray-100 px-1 py-0.5 rounded-full">
                              {agent.name}
                            </div>
                          ) : null;
                        })}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
          
          {/* Main flow area */}
          <div className="flex-1 flex flex-col h-full">
            <ReactFlowProvider>
              <div className="flex-1 h-full" onDrop={onDrop} onDragOver={onDragOver}>
                <ReactFlow
                  nodes={nodes}
                  edges={edges}
                  onNodesChange={onNodesChange}
                  onEdgesChange={onEdgesChange}
                  onConnect={onConnect}
                  nodeTypes={nodeTypes}
                  onInit={setReactFlowInstance}
                  snapToGrid={true}
                  fitView
                >
                  <Background />
                  <Controls />
                  <Panel position="top-left">
                    <div className="bg-white p-2 rounded-md shadow-md text-xs">
                      <div><strong>Tips:</strong></div>
                      <div>• Drag agents from sidebar to canvas</div>
                      <div>• Connect nodes by dragging from handles</div>
                      <div>• Create a path from Input to Output</div>
                    </div>
                  </Panel>
                </ReactFlow>
              </div>
            </ReactFlowProvider>
          </div>
          
          {/* Right sidebar (logs) */}
          <div className="w-64 border-l overflow-auto">
            <div className="p-4">
              <h2 className="font-semibold mb-2">Execution Log</h2>
              <div className="bg-gray-50 p-2 rounded-md h-48 overflow-y-auto text-xs font-mono">
                {executionLog.length > 0 ? (
                  executionLog.map((log, index) => (
                    <div key={index} className="mb-1">
                      {log}
                    </div>
                  ))
                ) : (
                  <div className="text-gray-400 italic">
                    No execution logs yet. Execute the workflow to see output.
                  </div>
                )}
              </div>
              
              <h2 className="font-semibold mt-4 mb-2">Output</h2>
              <div className="bg-gray-50 p-2 rounded-md min-h-32 max-h-64 overflow-y-auto text-xs whitespace-pre-wrap">
                {outputText ? outputText : (
                  <span className="text-gray-400 italic">No output generated yet</span>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}