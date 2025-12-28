# Sankalpa - AI-Powered Development Automation

Sankalpa is a multi-agent AI platform that can autonomously build, test, and deploy projects. This repository contains the fixed and improved version of Sankalpa.

## System Overview

Sankalpa is a comprehensive AI-powered development automation platform that uses a multi-agent architecture to accelerate and enhance software development workflows. Key features include:

- **Agent Generation**: Create new specialized agents dynamically
- **Chain Execution**: Run sequences of agents in a workflow
- **Memory Management**: Persistent storage of agent inputs and outputs
- **API Interface**: RESTful API for interacting with agents

## Getting Started

### Prerequisites

- Python 3.10 or later
- Node.js 18 or later

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sankalpa.git
cd sankalpa
```

2. Set up the Python environment:
```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Running Sankalpa

### Quick Start

The easiest way to start Sankalpa is to use the provided start script:

```bash
./start_sankalpa.sh
```

This will start:
- The API server on port 8080
- The frontend server on port 3003 (if working)

To stop Sankalpa, use:

```bash
./stop_sankalpa.sh
```

### Running Components Individually

#### API Server Only

```bash
source venv/bin/activate
python minimal_api_server.py
```

#### Interactive CLI

```bash
source venv/bin/activate
python simple_run.py
```

#### Comprehensive Tests

```bash
source venv/bin/activate
python comprehensive_test.py
```

## Working with Agents

### Available Agents

The system comes with several built-in agents:
- `self_replicator`: Creates new agents dynamically
- `project_architect`: Generates project structures
- Various other specialized agents for different tasks

You can list all available agents by accessing the endpoint:
```
GET http://localhost:8080/api/agents
```

### Creating New Agents

You can create new agents using the self-replicator agent through the API:

```
POST http://localhost:8080/api/create-agent
{
    "name": "my_agent",
    "description": "Description of the agent",
    "category": "utility",
    "logic": "Your agent implementation code here",
    "inputs": [
        {"name": "input1", "type": "string"}
    ],
    "outputs": [
        {"name": "output1", "type": "string"}
    ]
}
```

### Executing Agents

You can execute any agent through the API:

```
POST http://localhost:8080/api/agents/execute/{agent_name}
{
    // Agent-specific input parameters
}
```

## Troubleshooting

If you encounter issues:

1. Check the API server status:
```bash
curl http://localhost:8080/api/status
```

2. Run the system check script:
```bash
python check_all.py
```

3. Check log files:
```bash
cat api_server.log
cat frontend_server.log
```

4. Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

## API Endpoints

- `GET /api/status`: Check server status
- `GET /api/agents`: List all available agents
- `GET /api/memory`: View memory contents
- `POST /api/create-agent`: Create a new agent
- `POST /api/agents/execute/{agent_name}`: Execute an agent

## License

This project is licensed under the MIT License - see the LICENSE file for details.