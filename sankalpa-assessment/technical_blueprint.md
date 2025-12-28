# Sankalpa Technical Implementation Blueprint

This document provides specific technical recommendations for implementing the enhancements outlined in the improvement plan.

## Backend Architecture

### FastAPI Application Structure

```
/backend
  /routers
    /api
      v1.py         # API version 1 router
      v2.py         # API version 2 router
    agents.py       # Agent operations
    auth.py         # Authentication endpoints
    memory.py       # Memory operations
  /core
    config.py       # App configuration
    dependencies.py # Dependency injection
    logging.py      # Logging configuration
    security.py     # Security utilities
  /db
    base.py         # Database setup
    models.py       # SQLAlchemy models
    repositories/   # Data access layer
    migrations/     # Alembic migrations
  /services
    agent_service.py    # Agent business logic
    memory_service.py   # Memory business logic
    auth_service.py     # Auth business logic
  main.py           # FastAPI application
  Dockerfile        # Container definition
```

### Code Example: Enhanced Main Application

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from backend.core.config import settings
from backend.routers import api, agents, auth, memory
from backend.core.logging import setup_logging
from backend.db.base import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup logging
    setup_logging()
    
    # Initialize the database
    await init_db()
    
    yield
    # Cleanup resources

app = FastAPI(
    title="Sankalpa API",
    description="API for AI-powered software development automation",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api.router)
app.include_router(agents.router)
app.include_router(auth.router)
app.include_router(memory.router)

@app.get("/")
async def root():
    return {"message": "Sankalpa API is running", "version": "1.0.0"}
```

## Agent System

### Enhanced Base Agent

```python
from abc import ABC, abstractmethod
import logging
from typing import Dict, Any, Optional
from pydantic import BaseModel, ValidationError
import time
import traceback

class AgentInput(BaseModel):
    prompt: str
    context: Optional[Dict[str, Any]] = {}

class AgentOutput(BaseModel):
    message: str
    files: Optional[Dict[str, str]] = {}
    data: Optional[Dict[str, Any]] = {}
    error: Optional[str] = None

class BaseAgent(ABC):
    def __init__(self, name: str, memory=None):
        self.name = name
        self.memory = memory or {}
        self.logger = logging.getLogger(f"agent.{name}")
        self.start_time = None

    def _validate_input(self, input_data: Dict[str, Any]) -> AgentInput:
        try:
            return AgentInput(**input_data)
        except ValidationError as e:
            self.logger.error(f"Invalid input: {e}")
            raise ValueError(f"Invalid input: {e}")

    def _validate_output(self, output_data: Dict[str, Any]) -> AgentOutput:
        try:
            return AgentOutput(**output_data)
        except ValidationError as e:
            self.logger.error(f"Invalid output: {e}")
            return AgentOutput(
                message="Agent produced invalid output",
                error=str(e)
            )

    def _start_timing(self):
        self.start_time = time.time()

    def _end_timing(self):
        if self.start_time:
            duration = time.time() - self.start_time
            self.logger.info(f"Agent {self.name} execution time: {duration:.2f}s")
            return duration
        return None

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        self._start_timing()
        self.logger.info(f"Running agent: {self.name}")
        
        try:
            # Validate input
            validated_input = self._validate_input(input_data)
            
            # Execute agent logic
            result = self._execute(validated_input.dict())
            
            # Validate output
            validated_output = self._validate_output(result)
            
            # Log completion
            self.logger.info(f"Agent {self.name} completed successfully")
            
            return validated_output.dict()
        
        except Exception as e:
            self.logger.error(f"Error in agent {self.name}: {str(e)}")
            self.logger.debug(traceback.format_exc())
            return {
                "message": f"Error in agent {self.name}",
                "error": str(e)
            }
        finally:
            self._end_timing()

    @abstractmethod
    def _execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Implement agent logic here"""
        pass
```

## Memory System

### Database Models

```python
from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class Agent(Base):
    __tablename__ = "agents"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text)
    module_path = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class AgentRun(Base):
    __tablename__ = "agent_runs"
    
    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id"))
    input_data = Column(JSON)
    output_data = Column(JSON)
    status = Column(String)  # success, error, timeout
    duration_ms = Column(Integer)
    error_message = Column(Text, nullable=True)
    session_id = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    agent = relationship("Agent", back_populates="runs")

Agent.runs = relationship("AgentRun", back_populates="agent")

class Session(Base):
    __tablename__ = "sessions"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=True)
    metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    runs = relationship("AgentRun", primaryjoin="Session.id == AgentRun.session_id")
```

### Memory Manager

```python
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, Optional, List
import uuid
from datetime import datetime
from backend.db.models import Session, AgentRun, Agent
from backend.db.repositories.agent_repository import AgentRepository
from backend.db.repositories.agent_run_repository import AgentRunRepository
from backend.db.repositories.session_repository import SessionRepository

class MemoryManager:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.agent_repo = AgentRepository(db_session)
        self.run_repo = AgentRunRepository(db_session)
        self.session_repo = SessionRepository(db_session)
        self.current_session_id = None

    async def create_session(self, name: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Create a new session and return its ID"""
        session_id = str(uuid.uuid4())
        session = Session(
            id=session_id,
            name=name,
            metadata=metadata or {},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        await self.session_repo.create(session)
        self.current_session_id = session_id
        return session_id

    async def save(self, agent_name: str, input_data: Dict[str, Any], output_data: Dict[str, Any], 
                  status: str, duration_ms: int, error_message: Optional[str] = None) -> None:
        """Save an agent run to the database"""
        if not self.current_session_id:
            await self.create_session("auto_created")
            
        agent = await self.agent_repo.get_by_name(agent_name)
        
        if not agent:
            # If agent doesn't exist in DB, create a placeholder
            agent_id = await self.agent_repo.create_placeholder(agent_name)
        else:
            agent_id = agent.id
            
        run = AgentRun(
            agent_id=agent_id,
            input_data=input_data,
            output_data=output_data,
            status=status,
            duration_ms=duration_ms,
            error_message=error_message,
            session_id=self.current_session_id,
            created_at=datetime.utcnow()
        )
        
        await self.run_repo.create(run)

    async def load(self, agent_name: str, session_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Load all runs for a specific agent, optionally filtered by session"""
        sid = session_id or self.current_session_id
        if not sid:
            return []
            
        runs = await self.run_repo.get_by_agent_name_and_session(agent_name, sid)
        return [run.output_data for run in runs]

    async def get_session_summary(self, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Get a summary of all runs in a session"""
        sid = session_id or self.current_session_id
        if not sid:
            return {}
            
        session = await self.session_repo.get_by_id(sid)
        if not session:
            return {}
            
        runs = await self.run_repo.get_by_session_id(sid)
        
        agents = {}
        for run in runs:
            agent_name = run.agent.name
            if agent_name not in agents:
                agents[agent_name] = []
            agents[agent_name].append({
                "id": run.id,
                "status": run.status,
                "duration_ms": run.duration_ms,
                "created_at": run.created_at.isoformat(),
                "output_summary": {k: v for k, v in run.output_data.items() if k != "files"}
            })
            
        return {
            "session_id": session.id,
            "name": session.name,
            "created_at": session.created_at.isoformat(),
            "updated_at": session.updated_at.isoformat(),
            "metadata": session.metadata,
            "agents": agents
        }
```

## Chain Manager Enhancements

```python
from typing import List, Dict, Any, Optional, Callable
import asyncio
import logging
from backend.services.agent_service import AgentService
from backend.services.memory_service import MemoryService

class ChainManager:
    def __init__(self, agent_service: AgentService, memory_service: MemoryService):
        self.agent_service = agent_service
        self.memory_service = memory_service
        self.logger = logging.getLogger("chain_manager")

    async def run(self, chain_config: Dict[str, Any], input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run a chain of agents based on the provided configuration"""
        session_id = await self.memory_service.create_session(
            name=chain_config.get("name", "unnamed_chain"),
            metadata={
                "chain_config": chain_config,
                "initial_input": input_data
            }
        )
        
        self.logger.info(f"Starting chain execution with session {session_id}")
        
        # Extract chain type and agents
        chain_type = chain_config.get("type", "sequential")
        agents = chain_config.get("agents", [])
        
        if not agents:
            return {"error": "No agents specified in chain"}
        
        # Execute the chain based on type
        if chain_type == "sequential":
            return await self._run_sequential(agents, input_data)
        elif chain_type == "parallel":
            return await self._run_parallel(agents, input_data)
        elif chain_type == "conditional":
            return await self._run_conditional(agents, chain_config.get("conditions", {}), input_data)
        else:
            return {"error": f"Unsupported chain type: {chain_type}"}

    async def _run_sequential(self, agents: List[str], input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run agents sequentially, passing output from one to the next"""
        self.logger.info(f"Running sequential chain with {len(agents)} agents")
        
        result = input_data
        for agent_name in agents:
            self.logger.debug(f"Running agent {agent_name} in sequential chain")
            try:
                result = await self.agent_service.run_agent(agent_name, result)
            except Exception as e:
                self.logger.error(f"Error in agent {agent_name}: {str(e)}")
                return {
                    "error": f"Chain failed at agent {agent_name}: {str(e)}",
                    "partial_result": result
                }
                
        return {
            "message": "Chain executed successfully",
            "result": result
        }

    async def _run_parallel(self, agents: List[str], input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run agents in parallel, then combine their outputs"""
        self.logger.info(f"Running parallel chain with {len(agents)} agents")
        
        tasks = []
        for agent_name in agents:
            self.logger.debug(f"Scheduling agent {agent_name} in parallel chain")
            tasks.append(self.agent_service.run_agent(agent_name, input_data))
            
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        combined_result = {"message": "Parallel chain executed", "results": {}}
        errors = []
        
        for i, result in enumerate(results):
            agent_name = agents[i]
            if isinstance(result, Exception):
                self.logger.error(f"Error in parallel agent {agent_name}: {str(result)}")
                errors.append(f"{agent_name}: {str(result)}")
                combined_result["results"][agent_name] = {"error": str(result)}
            else:
                combined_result["results"][agent_name] = result
                
        if errors:
            combined_result["errors"] = errors
            
        return combined_result

    async def _run_conditional(self, agents: List[str], conditions: Dict[str, Any], 
                              input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run agents conditionally based on conditions"""
        self.logger.info(f"Running conditional chain with {len(agents)} agents")
        
        # Initialize with first agent
        current_agent = agents[0] if agents else None
        result = input_data
        executed_agents = []
        
        while current_agent and current_agent not in executed_agents:
            self.logger.debug(f"Running agent {current_agent} in conditional chain")
            try:
                result = await self.agent_service.run_agent(current_agent, result)
                executed_agents.append(current_agent)
                
                # Determine next agent based on conditions
                next_agent = None
                for condition_key, target_agent in conditions.get(current_agent, {}).items():
                    condition_met = self._evaluate_condition(condition_key, result)
                    if condition_met:
                        next_agent = target_agent
                        break
                        
                current_agent = next_agent
                
            except Exception as e:
                self.logger.error(f"Error in agent {current_agent}: {str(e)}")
                return {
                    "error": f"Chain failed at agent {current_agent}: {str(e)}",
                    "partial_result": result,
                    "executed_agents": executed_agents
                }
                
        return {
            "message": "Conditional chain executed successfully",
            "result": result,
            "executed_agents": executed_agents
        }

    def _evaluate_condition(self, condition: str, data: Dict[str, Any]) -> bool:
        """Evaluate a condition against result data"""
        try:
            # Simple conditions: "key:value" or "key"
            if ":" in condition:
                key, value = condition.split(":", 1)
                return str(data.get(key)) == value
            else:
                # Check if key exists and has a truthy value
                return bool(data.get(condition))
        except Exception as e:
            self.logger.error(f"Error evaluating condition {condition}: {str(e)}")
            return False
```

## Frontend Improvements

### Enhanced Composer Page

```tsx
import React, { useCallback, useState, useEffect } from 'react';
import ReactFlow, {
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
  Node,
  Edge,
  Connection,
  NodeTypes,
  Panel,
  Handle,
  Position
} from 'reactflow';
import 'reactflow/dist/style.css';
import axios from 'axios';
import { Spinner, Alert, Button, Box, Heading, Text, Select, FormControl, FormLabel, Input } from '@chakra-ui/react';

// Custom node component
const AgentNode = ({ data, isConnectable }) => {
  return (
    <div className="agent-node p-4 rounded-lg border-2 border-blue-500 bg-white shadow-lg min-w-[200px]">
      <Handle type="target" position={Position.Top} isConnectable={isConnectable} />
      <div className="font-bold text-lg">{data.label}</div>
      {data.description && <div className="text-sm text-gray-600">{data.description}</div>}
      <div className="flex mt-2">
        {data.status && (
          <span className={`px-2 py-1 rounded text-xs ${
            data.status === 'completed' ? 'bg-green-100 text-green-800' : 
            data.status === 'running' ? 'bg-blue-100 text-blue-800' :
            data.status === 'error' ? 'bg-red-100 text-red-800' : 
            'bg-gray-100 text-gray-800'
          }`}>
            {data.status}
          </span>
        )}
      </div>
      <Handle type="source" position={Position.Bottom} isConnectable={isConnectable} />
    </div>
  );
};

const nodeTypes: NodeTypes = {
  agent: AgentNode,
};

// Initial nodes with better styling
const initialNodes: Node[] = [
  {
    id: '1',
    type: 'agent',
    data: { label: 'Planner Agent', description: 'Creates execution plan' },
    position: { x: 250, y: 0 },
  },
];

export default function Composer() {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [output, setOutput] = useState<string>('');
  const [isRunning, setIsRunning] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [availableAgents, setAvailableAgents] = useState<any[]>([]);
  const [selectedAgent, setSelectedAgent] = useState<string>('');
  const [chainName, setChainName] = useState<string>('My Agent Chain');
  const [prompt, setPrompt] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(true);

  // Fetch available agents on component mount
  useEffect(() => {
    const fetchAgents = async () => {
      try {
        const response = await axios.get('/api/agents');
        setAvailableAgents(response.data);
        setIsLoading(false);
      } catch (err) {
        setError('Failed to load available agents');
        setIsLoading(false);
      }
    };
    
    fetchAgents();
  }, []);

  const onConnect = useCallback(
    (params: Edge | Connection) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  const addAgentNode = () => {
    if (!selectedAgent) return;
    
    const agent = availableAgents.find(a => a.name === selectedAgent);
    if (!agent) return;
    
    const id = (nodes.length + 1).toString();
    const newNode: Node = {
      id,
      type: 'agent',
      data: { 
        label: agent.name,
        description: agent.description,
        status: 'pending'
      },
      position: { 
        x: Math.random() * 300 + 100, 
        y: nodes.length * 100 + 100 
      },
    };
    
    setNodes((nds) => [...nds, newNode]);
  };

  const extractAgentChain = () => {
    // Convert the visual flow to a chain configuration
    const chainAgents = nodes.map(node => node.data.label);
    
    // Create chain structure by following edges
    const chainConfig = {
      name: chainName,
      type: 'sequential', // Default to sequential
      agents: chainAgents,
      edges: edges.map(edge => ({
        source: edge.source,
        target: edge.target
      }))
    };
    
    return chainConfig;
  };

  const runChain = async () => {
    try {
      setIsRunning(true);
      setError(null);
      
      // Update nodes to show running status
      setNodes((nds) => 
        nds.map(node => ({
          ...node,
          data: { ...node.data, status: 'pending' }
        }))
      );
      
      const chainConfig = extractAgentChain();
      
      // Start chain execution
      const res = await axios.post('/api/run-chain', {
        chain: chainConfig,
        input: { prompt }
      });
      
      // Update output and node statuses
      setOutput(JSON.stringify(res.data, null, 2));
      
      // Mark agents as completed
      setNodes((nds) => 
        nds.map(node => ({
          ...node,
          data: { ...node.data, status: 'completed' }
        }))
      );
      
    } catch (err) {
      setError('Chain execution failed: ' + (err.response?.data?.error || err.message));
      
      // Mark nodes as error
      setNodes((nds) => 
        nds.map(node => ({
          ...node,
          data: { 
            ...node.data, 
            status: node.data.status === 'running' ? 'error' : node.data.status 
          }
        }))
      );
    } finally {
      setIsRunning(false);
    }
  };

  const saveChain = async () => {
    try {
      const chainConfig = extractAgentChain();
      
      await axios.post('/api/save-chain', {
        name: chainName,
        config: chainConfig
      });
      
      alert('Chain saved successfully!');
    } catch (err) {
      setError('Failed to save chain: ' + (err.response?.data?.error || err.message));
    }
  };

  if (isLoading) {
    return <div className="flex items-center justify-center h-screen"><Spinner /></div>;
  }

  return (
    <div className="h-screen flex flex-col">
      {/* Header with controls */}
      <div className="bg-gray-100 p-4 border-b flex flex-wrap items-center gap-4">
        <FormControl className="flex-1 min-w-[250px]">
          <FormLabel>Chain Name</FormLabel>
          <Input 
            value={chainName}
            onChange={(e) => setChainName(e.target.value)}
            placeholder="My Agent Chain"
          />
        </FormControl>
        
        <FormControl className="flex-1 min-w-[250px]">
          <FormLabel>Add Agent</FormLabel>
          <div className="flex gap-2">
            <Select 
              value={selectedAgent}
              onChange={(e) => setSelectedAgent(e.target.value)}
              placeholder="Select agent"
            >
              {availableAgents.map(agent => (
                <option key={agent.name} value={agent.name}>
                  {agent.name}
                </option>
              ))}
            </Select>
            <Button onClick={addAgentNode} colorScheme="blue">Add</Button>
          </div>
        </FormControl>
        
        <FormControl className="flex-1 min-w-[250px]">
          <FormLabel>Input Prompt</FormLabel>
          <Input 
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Enter prompt for the chain..."
          />
        </FormControl>
        
        <div className="flex gap-2 mt-auto">
          <Button onClick={saveChain} colorScheme="green" leftIcon={<span>💾</span>}>
            Save Chain
          </Button>
          <Button 
            onClick={runChain} 
            colorScheme="purple" 
            leftIcon={<span>▶️</span>}
            isLoading={isRunning}
            loadingText="Running"
          >
            Run Chain
          </Button>
        </div>
      </div>
      
      {/* Error alert */}
      {error && (
        <Alert status="error" variant="solid" className="m-4">
          {error}
        </Alert>
      )}
      
      {/* Flow editor */}
      <div className="flex-1">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          nodeTypes={nodeTypes}
          fitView
        >
          <Controls />
          <MiniMap />
          <Background variant="dots" gap={12} size={1} />
          
          <Panel position="bottom-center" className="bg-white p-4 rounded-t-lg shadow-lg border">
            <Heading size="sm">Chain Layout</Heading>
            <Text fontSize="sm" className="text-gray-600">
              Drag to connect agents. Double-click background to add a node.
            </Text>
          </Panel>
        </ReactFlow>
      </div>
      
      {/* Output panel */}
      {output && (
        <div className="bg-gray-100 p-4 border-t h-1/3 overflow-auto">
          <Heading size="md" className="mb-2">Output</Heading>
          <pre className="bg-gray-800 text-gray-100 p-4 rounded overflow-auto">
            {output}
          </pre>
        </div>
      )}
    </div>
  );
}
```

## CLI Enhancements

```python
import typer
import json
import os
from typing import List, Optional
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from agents.loader import load_agent
from memory.memory_manager import MemoryManager
from agents.chain_manager import ChainManager
from cli.config_manager import ConfigManager

app = typer.Typer(help="Sankalpa CLI - AI-powered software development automation")
console = Console()
config = ConfigManager()

@app.command()
def run_agent(
    name: str = typer.Argument(..., help="Name of the agent to run"),
    prompt: str = typer.Option("", "--prompt", "-p", help="Input prompt for the agent"),
    input_file: Optional[Path] = typer.Option(None, "--input", "-i", help="JSON file with input data"),
    output_file: Optional[Path] = typer.Option(None, "--output", "-o", help="Save output to JSON file"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show verbose output")
):
    """
    Run a single agent with the provided input
    """
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]Loading agent {name}..."),
            transient=True,
        ) as progress:
            progress.add_task("load", name=name)
            agent = load_agent(name)
            
        if not agent:
            console.print(f"[bold red]Error:[/] Agent '{name}' not found")
            raise typer.Exit(code=1)
            
        # Prepare input data
        input_data = {"prompt": prompt}
        
        if input_file:
            try:
                with open(input_file) as f:
                    file_data = json.load(f)
                    input_data.update(file_data)
            except Exception as e:
                console.print(f"[bold red]Error loading input file:[/] {str(e)}")
                raise typer.Exit(code=1)
                
        # Run the agent
        with Progress(
            SpinnerColumn(),
            TextColumn(f"[bold green]Running {name}..."),
            transient=not verbose,
        ) as progress:
            task = progress.add_task("run")
            result = agent.run(input_data)
            progress.update(task, completed=100)
            
        # Display result
        console.print(Panel.fit(
            f"[bold]Agent:[/] {name}\n\n{json.dumps(result, indent=2)}",
            title="Result",
            border_style="green"
        ))
        
        # Save output if requested
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2)
            console.print(f"Output saved to [bold]{output_file}[/]")
            
    except Exception as e:
        console.print(f"[bold red]Error running agent:[/] {str(e)}")
        if verbose:
            console.print_exception()
        raise typer.Exit(code=1)

@app.command()
def run_chain(
    chain_file: Path = typer.Argument(..., help="JSON file containing the chain configuration"),
    prompt: str = typer.Option("", "--prompt", "-p", help="Input prompt for the chain"),
    input_file: Optional[Path] = typer.Option(None, "--input", "-i", help="JSON file with input data"),
    output_file: Optional[Path] = typer.Option(None, "--output", "-o", help="Save output to JSON file"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show verbose output")
):
    """
    Run a chain of agents from a JSON configuration file
    """
    try:
        # Load chain configuration
        try:
            with open(chain_file) as f:
                chain_config = json.load(f)
        except Exception as e:
            console.print(f"[bold red]Error loading chain file:[/] {str(e)}")
            raise typer.Exit(code=1)
            
        # Initialize memory and chain manager
        memory = MemoryManager()
        agents = []
        
        # Get agent names from chain
        if isinstance(chain_config, list):
            # Simple list format
            agent_names = [
                node["label"].lower().replace("agent ", "").strip()
                for node in chain_config
                if "Agent" in node["label"]
            ]
        else:
            # New structured format
            agent_names = chain_config.get("agents", [])
            
        # Load agents
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]Loading agents..."),
            transient=not verbose,
        ) as progress:
            for name in agent_names:
                task = progress.add_task(f"load-{name}")
                agent = load_agent(name)
                if agent:
                    agents.append(agent)
                    progress.update(task, completed=100)
                else:
                    console.print(f"[bold yellow]Warning:[/] Agent '{name}' not found, skipping")
                    
        if not agents:
            console.print("[bold red]Error:[/] No valid agents found in chain")
            raise typer.Exit(code=1)
            
        # Prepare input data
        input_data = {"prompt": prompt}
        
        if input_file:
            try:
                with open(input_file) as f:
                    file_data = json.load(f)
                    input_data.update(file_data)
            except Exception as e:
                console.print(f"[bold red]Error loading input file:[/] {str(e)}")
                raise typer.Exit(code=1)
                
        # Run the chain
        chain = ChainManager(agents, memory)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold green]Running chain..."),
            transient=not verbose,
        ) as progress:
            task = progress.add_task("run-chain")
            result = chain.run(input_data)
            progress.update(task, completed=100)
            
        # Display result
        console.print(Panel.fit(
            json.dumps(result, indent=2),
            title="Chain Result",
            border_style="green"
        ))
        
        # Save output if requested
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2)
            console.print(f"Output saved to [bold]{output_file}[/]")
            
    except Exception as e:
        console.print(f"[bold red]Error running chain:[/] {str(e)}")
        if verbose:
            console.print_exception()
        raise typer.Exit(code=1)

@app.command()
def list_agents(
    category: Optional[str] = typer.Option(None, "--category", "-c", help="Filter agents by category")
):
    """
    List all available agents in the catalog
    """
    try:
        catalog_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "catalog", "agent_catalog.json")
        
        with open(catalog_path) as f:
            catalog = json.load(f)
            
        # Filter by category if specified
        if category:
            filtered_catalog = {k: v for k, v in catalog.items() if category.lower() in v.get("module", "").lower()}
        else:
            filtered_catalog = catalog
            
        if not filtered_catalog:
            console.print(f"[yellow]No agents found{' in category ' + category if category else ''}[/]")
            return
            
        # Group by module category
        categories = {}
        for name, info in filtered_catalog.items():
            module = info.get("module", "")
            cat = module.split(".")[0] if "." in module else "other"
            if cat not in categories:
                categories[cat] = []
            categories[cat].append((name, info))
            
        # Display agents by category
        for cat, agents in categories.items():
            console.print(f"[bold blue]{cat.upper()}[/]")
            for name, info in sorted(agents):
                console.print(f"  [green]{name}[/] - {info.get('description', 'No description')}")
            console.print()
            
    except Exception as e:
        console.print(f"[bold red]Error listing agents:[/] {str(e)}")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
```

## Agent Catalog JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Agent Catalog",
  "type": "object",
  "additionalProperties": {
    "type": "object",
    "required": ["description", "module"],
    "properties": {
      "description": {
        "type": "string",
        "description": "Human-readable description of the agent's purpose"
      },
      "module": {
        "type": "string",
        "description": "Python module path for the agent implementation"
      },
      "parameters": {
        "type": "object",
        "description": "Optional parameters schema for the agent",
        "additionalProperties": true
      },
      "outputs": {
        "type": "object",
        "description": "Schema of expected agent outputs",
        "additionalProperties": true
      },
      "category": {
        "type": "string",
        "description": "Category for grouping agents"
      },
      "dependencies": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "Other agents this agent depends on"
      },
      "examples": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "input": {
              "type": "object"
            },
            "output": {
              "type": "object"
            },
            "description": {
              "type": "string"
            }
          }
        },
        "description": "Example usage scenarios"
      }
    }
  }
}
```

## Docker Configuration

### Dockerfile for Backend

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p memory/sessions projects

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  backend:
    build: 
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/sankalpa
      - ENVIRONMENT=production
      - SECRET_KEY=${SECRET_KEY}
      - CORS_ORIGINS=http://localhost:3000,https://${DOMAIN}
    volumes:
      - ./projects:/app/projects
      - ./memory:/app/memory
    depends_on:
      - db
    restart: always

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
    depends_on:
      - backend
    restart: always

  db:
    image: postgres:13
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=sankalpa
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: always

  redis:
    image: redis:6
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: always

volumes:
  postgres_data:
  redis_data:
```