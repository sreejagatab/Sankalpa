# Sankalpa

<div align="center">

```
███████╗ █████╗ ███╗   ██╗██╗  ██╗ █████╗ ██╗     ██████╗  █████╗
██╔════╝██╔══██╗████╗  ██║██║ ██╔╝██╔══██╗██║     ██╔══██╗██╔══██╗
███████╗███████║██╔██╗ ██║█████╔╝ ███████║██║     ██████╔╝███████║
╚════██║██╔══██║██║╚██╗██║██╔═██╗ ██╔══██║██║     ██╔═══╝ ██╔══██║
███████║██║  ██║██║ ╚████║██║  ██╗██║  ██║███████╗██║     ██║  ██║
╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝  ╚═╝
```

**The Ultimate Multi-Agent AI Platform for Autonomous Software Development**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Node.js](https://img.shields.io/badge/Node.js-18+-green.svg)](https://nodejs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.103+-teal.svg)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-14+-black.svg)](https://nextjs.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[Features](#-features) | [Quick Start](#-quick-start) | [Architecture](#-architecture) | [Agents](#-agent-ecosystem) | [API](#-api-reference) | [Documentation](#-documentation)

</div>

---

## What is Sankalpa?

**Sankalpa** (Sanskrit: "intention" or "will") is a production-ready, enterprise-grade **multi-agent AI platform** that autonomously builds, tests, deploys, and maintains complete software applications. It's not just a chatbot or code assistant - it's an **AI Operating System for Software Development**.

### The Vision

```
User Prompt → Planner Agent → Builder Agents → Test Agents → Deploy Agent → Live Application
```

Give Sankalpa a prompt like *"Build me a blog with authentication, markdown editor, and dark mode"* and watch it:

1. **Plan** the architecture and module structure
2. **Generate** frontend (Next.js), backend (FastAPI), and database schemas
3. **Create** authentication with JWT tokens
4. **Build** UI components with Tailwind CSS
5. **Write** unit and integration tests
6. **Deploy** to Vercel/AWS/GCP
7. **Generate** documentation and marketing materials

---

## Key Features

### Core Capabilities

| Feature | Description |
|---------|-------------|
| **35+ Specialized AI Agents** | Builder, testing, deployment, marketing, and meta agents |
| **Visual Workflow Composer** | Drag-and-drop agent chain builder with React Flow |
| **Persistent Memory System** | Session-based context with transaction support |
| **Chain Execution Engine** | Sequential, parallel, and conditional agent workflows |
| **Self-Replicating Agents** | Agents that create new agents from text prompts |
| **LLM Fine-Tuning** | Automated fine-tuning pipeline for custom models |
| **Multi-Tenancy** | Enterprise-ready with organization support |
| **Marketplace** | Share and monetize agents and workflows |

### What Makes Sankalpa Unique?

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         SANKALPA CAPABILITIES                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                  │
│  │   Planning   │  │   Building   │  │   Testing    │                  │
│  │   ────────   │  │   ────────   │  │   ────────   │                  │
│  │ • Task plan  │  │ • Frontend   │  │ • Unit tests │                  │
│  │ • Arch design│  │ • Backend    │  │ • E2E tests  │                  │
│  │ • Workflow   │  │ • Database   │  │ • Security   │                  │
│  └──────────────┘  └──────────────┘  └──────────────┘                  │
│                                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                  │
│  │  Deploying   │  │  Marketing   │  │   Enhanced   │                  │
│  │  ──────────  │  │  ──────────  │  │  ──────────  │                  │
│  │ • CI/CD      │  │ • README     │  │ • Self-rep   │                  │
│  │ • Cloud      │  │ • SEO        │  │ • Fine-tune  │                  │
│  │ • Domain     │  │ • Pitch deck │  │ • Copilot    │                  │
│  └──────────────┘  └──────────────┘  └──────────────┘                  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Quick Start

### Prerequisites

- **Python 3.10+**
- **Node.js 18+**
- **PostgreSQL 14+** (optional, for production)
- **Redis 7+** (optional, for caching)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/sankalpa.git
cd sankalpa

# Backend setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend setup
cd frontend
npm install
cd ..

# Configure environment
cp .env.example .env
# Edit .env with your settings
```

### Run Sankalpa

**Option 1: Full System Launcher**
```bash
python run_sankalpa.py
```

**Option 2: Run Services Separately**
```bash
# Terminal 1: Backend API (port 9000)
python -m uvicorn backend.simple_main:app --host 0.0.0.0 --port 9000

# Terminal 2: Frontend (port 9001)
cd frontend && npm run dev
```

**Option 3: Docker Compose**
```bash
docker-compose up -d
```

### Access Points

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:9001 | Web UI |
| **Workflow Composer** | http://localhost:9001/composer | Visual chain builder |
| **Playground** | http://localhost:9001/playground | Agent testing |
| **Backend API** | http://localhost:9000 | REST API |
| **API Status** | http://localhost:9000/api/status | Health check |

---

## Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              SANKALPA PLATFORM                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         PRESENTATION LAYER                           │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │   │
│  │  │  Composer    │  │  Playground  │  │  Dashboard   │              │   │
│  │  │  (ReactFlow) │  │  (Testing)   │  │  (Metrics)   │              │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │   │
│  │                       Next.js 14 + TailwindCSS                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                           API LAYER                                  │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐           │   │
│  │  │ /agents  │  │ /chains  │  │ /memory  │  │ /users   │           │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘           │   │
│  │                     FastAPI + JWT + RBAC                            │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        CORE SERVICES                                 │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐           │   │
│  │  │ Security │  │ Caching  │  │Monitoring│  │ Logging  │           │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         AGENT LAYER (35+ Agents)                     │   │
│  │  ┌────────────────────────────────────────────────────────────────┐ │   │
│  │  │ Builder(11) │ Testing(4) │ Deploy(3) │ Marketing(4) │ Meta(2) │ │   │
│  │  └────────────────────────────────────────────────────────────────┘ │   │
│  │  ┌────────────────────────────────────────────────────────────────┐ │   │
│  │  │ Enhanced(6): SelfReplicator, Finetuner, Copilot, VSCode, etc.  │ │   │
│  │  └────────────────────────────────────────────────────────────────┘ │   │
│  │                    Chain Manager + Memory System                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                          DATA LAYER                                  │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │   │
│  │  │  PostgreSQL  │  │    Redis     │  │ File System  │              │   │
│  │  │  (Users,     │  │  (Caching,   │  │  (Sessions,  │              │   │
│  │  │   Chains)    │  │   Sessions)  │  │   Agents)    │              │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  INTEGRATIONS: GitHub │ Marketplace │ Multi-Tenancy │ NLP │ Fine-Tuning    │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Directory Structure

```
sankalpa/
├── agents/                     # 35+ AI Agents
│   ├── base.py                # BaseAgent abstract class
│   ├── enhanced_base.py       # Enhanced agent with logging
│   ├── loader.py              # Dynamic agent loading
│   ├── chain_manager.py       # Agent chain orchestration
│   ├── builder/               # 11 builder agents
│   │   ├── project_architect_agent.py
│   │   ├── frontend_builder_agent.py
│   │   ├── backend_builder_agent.py
│   │   ├── api_builder_agent.py
│   │   ├── db_schema_agent.py
│   │   ├── auth_builder_agent.py
│   │   └── ...
│   ├── testing/               # 4 testing agents
│   ├── deployment/            # 3 deployment agents
│   ├── marketing/             # 4 marketing agents
│   ├── enhanced/              # 6 enhanced agents
│   ├── meta/                  # 2 meta agents
│   ├── orchestration/         # 3 orchestration agents
│   └── custom/                # User-created agents
├── backend/                    # FastAPI Backend
│   ├── simple_main.py         # API server
│   ├── routers/               # API endpoints
│   │   ├── agents.py
│   │   ├── chains.py
│   │   ├── memory.py
│   │   └── users.py
│   ├── db/                    # Database layer
│   └── websockets/            # Real-time communication
├── core/                       # Core Services
│   ├── config.py              # Configuration management
│   ├── security.py            # JWT, RBAC, rate limiting
│   ├── caching.py             # Redis/in-memory caching
│   ├── monitoring.py          # Metrics and health checks
│   └── logging.py             # Structured logging
├── memory/                     # Memory Management
│   ├── memory_manager.py      # Basic memory
│   └── enhanced_memory_manager.py  # Transaction support
├── frontend/                   # Next.js Web Application
│   ├── pages/                 # 14+ pages
│   │   ├── index.tsx          # Homepage
│   │   ├── composer.tsx       # Visual workflow composer
│   │   ├── playground.tsx     # Agent testing
│   │   ├── dashboard/         # System dashboard
│   │   └── ...
│   ├── components/            # 20+ React components
│   └── lib/api-client.ts      # API client
├── marketplace/                # Agent marketplace
├── tenants/                    # Multi-tenancy
├── integrations/               # External integrations
│   └── github/                # GitHub API client
├── cli/                        # Command-line interface
├── tests/                      # Test suites
├── docs/                       # Documentation
├── docker-compose.yml          # Container orchestration
├── requirements.txt            # Python dependencies
└── run_sankalpa.py            # Full system launcher
```

---

## Agent Ecosystem

### Agent Categories

Sankalpa includes **35+ specialized agents** organized into 9 categories:

#### Builder Agents (11)

| Agent | Description | Key Outputs |
|-------|-------------|-------------|
| `project_architect` | Creates project structure and module plan | Folder structure, architecture |
| `frontend_builder` | Generates Next.js/React UI | Pages, components, styles |
| `backend_builder` | Creates FastAPI backend scaffold | Routes, models, middleware |
| `api_builder` | Generates REST API endpoints | OpenAPI spec, handlers |
| `db_schema` | Designs database schemas | Pydantic models, migrations |
| `auth_builder` | JWT authentication system | Login, signup, tokens |
| `ui_generator` | UI layout with Tailwind | Forms, inputs, layouts |
| `markdown_editor` | Markdown editor with preview | Editor component |
| `email_system` | SMTP email integration | Email templates, sender |
| `stripe_payment` | Payment system integration | Checkout, webhooks |
| `role_auth` | Role-based access control | Permissions, middleware |

#### Testing Agents (4)

| Agent | Description |
|-------|-------------|
| `test_suite` | Unit test generation |
| `integration_test` | Integration test creation |
| `security_scanner` | Security vulnerability scanning |
| `critic` | Code quality review |

#### Deployment Agents (3)

| Agent | Description |
|-------|-------------|
| `deploy_executor` | Deploy to Vercel/AWS/GCP/Azure |
| `ci_generator` | GitHub Actions CI/CD workflows |
| `domain_linker` | Custom domain configuration |

#### Marketing Agents (4)

| Agent | Description |
|-------|-------------|
| `readme_writer` | README.md generation |
| `seo_optimizer` | SEO meta tags and keywords |
| `product_hunt_copywriter` | Launch copy for Product Hunt |
| `pitch_deck_generator` | 10-slide pitch deck outline |

#### Enhanced Agents (6)

| Agent | Description |
|-------|-------------|
| `copilot` | Interactive AI assistant |
| `self_replicator` | Creates new agents from prompts |
| `finetuner` | LLM fine-tuning automation |
| `plugin_loader` | Third-party plugin integration |
| `vs_code_extension` | VS Code extension generation |
| `cli_runner` | CLI command execution |

#### Meta Agents (2)

| Agent | Description |
|-------|-------------|
| `multi_agent_memory_manager` | Cross-agent memory coordination |
| `version_tracker` | Version control and tracking |

#### Orchestration Agents (3)

| Agent | Description |
|-------|-------------|
| `planner_agent` | Task planning and workflow design |
| `execution_manager` | Agent execution orchestration |
| `session_replayer` | Session replay and debugging |

### Agent Execution Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        AGENT EXECUTION PIPELINE                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐          │
│  │  INPUT  │────▶│  AGENT  │────▶│  CHAIN  │────▶│ OUTPUT  │          │
│  │  DATA   │     │  LOADER │     │ MANAGER │     │ RESULT  │          │
│  └─────────┘     └─────────┘     └─────────┘     └─────────┘          │
│       │              │               │               │                 │
│       ▼              ▼               ▼               ▼                 │
│  ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐          │
│  │VALIDATE │     │ DYNAMIC │     │SEQUENTIAL│    │  STORE  │          │
│  │  INPUT  │     │  IMPORT │     │ PARALLEL │    │ MEMORY  │          │
│  │  SCHEMA │     │  CLASS  │     │CONDITIONAL│   │  LOGS   │          │
│  └─────────┘     └─────────┘     └─────────┘     └─────────┘          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## API Reference

### Base URL

```
http://localhost:9000/api
```

### Authentication

```bash
# Get JWT token
POST /api/users/login
Content-Type: application/json
{
  "username": "user@example.com",
  "password": "password"
}

# Use token in requests
Authorization: Bearer <token>
```

### Endpoints

#### Status

```bash
GET /api/status
# Response: {"status": "Sankalpa API Server is running!", "version": "1.0.0"}
```

#### Agents

```bash
# List all agents
GET /api/agents
# Response: {"agents": [{name, description, category, model, inputs, outputs}, ...]}

# List enhanced agents
GET /api/agents/enhanced
# Response: [{id, name, description, category, model}, ...]

# Execute an agent
POST /api/agents/execute
Content-Type: application/json
{
  "agent_name": "hello_world",
  "input_data": {"name": "User"}
}
# Response: {"agent_name": "hello_world", "execution_id": "exec_123", "result": {...}, "execution_time": 0.001}
```

#### Chains

```bash
# List chain templates
GET /api/chains
# Response: {"chains": [{name, description, agents}, ...]}

# Execute a chain
POST /api/chains/execute
Content-Type: application/json
{
  "chain_name": "builder_chain",
  "agents": ["project_architect", "frontend_builder", "backend_builder"],
  "input_data": {"app_name": "MyApp"},
  "session_id": "optional_session_id"
}
# Response: {"chain_name": "...", "status": "completed", "results": [...], "final_output": {...}}
```

#### Memory

```bash
# Save to memory
POST /api/memory/save
Content-Type: application/json
{
  "key": "my_key",
  "value": {"data": "value"},
  "session_id": "optional_session"
}

# Load from memory
POST /api/memory/load
Content-Type: application/json
{
  "key": "my_key",
  "session_id": "optional_session"
}

# Get all memory
GET /api/memory/all?session_id=optional

# List sessions
GET /api/memory/sessions
```

---

## Visual Workflow Composer

The **Workflow Composer** is a drag-and-drop interface for building agent chains visually.

### Features

- **Drag-and-drop nodes** - Add agents by dragging from the palette
- **Visual connections** - Connect agents with edges to define flow
- **Real-time execution** - Run chains and see progress live
- **Template workflows** - Load pre-built workflow templates
- **Export/Import** - Save and share workflow JSON files

### Accessing the Composer

```
http://localhost:9001/composer
```

### Workflow JSON Format

```json
{
  "name": "full_stack_builder",
  "description": "Build a complete full-stack application",
  "nodes": [
    {"id": "1", "type": "agent", "data": {"agent": "project_architect"}},
    {"id": "2", "type": "agent", "data": {"agent": "frontend_builder"}},
    {"id": "3", "type": "agent", "data": {"agent": "backend_builder"}}
  ],
  "edges": [
    {"source": "1", "target": "2"},
    {"source": "1", "target": "3"}
  ]
}
```

---

## Protocols & Integrations

Sankalpa integrates multiple AI agent protocols:

| Protocol | Purpose | Implementation |
|----------|---------|----------------|
| **LangChain** | Agent chaining, memory | ChainManager, MemoryManager |
| **MCP** | Model Context Protocol | Agent orchestration |
| **CrewAI** | Multi-agent collaboration | Role-based agents |
| **AutoGen** | Task planning | PlannerAgent |
| **ReAct** | Reasoning + tool use | Copilot, Critic agents |
| **PromptFlow** | Visual workflows | Composer UI |
| **GPT Engineer** | Project generation | Builder agents |
| **BabyAGI** | Task planning | Planning system |

---

## Configuration

### Environment Variables

Create a `.env` file from `.env.example`:

```bash
# Application
SANKALPA_ENV=development
SANKALPA_DEBUG=true
SANKALPA_LOG_LEVEL=INFO

# API Server
API_HOST=0.0.0.0
API_PORT=9000

# Frontend
FRONTEND_URL=http://localhost:9001

# Security
SANKALPA_JWT_SECRET=your-secret-key-here
SANKALPA_JWT_ALGORITHM=HS256
SANKALPA_JWT_EXPIRE_MINUTES=30

# Database (optional for production)
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=sankalpa
POSTGRES_HOST=localhost

# Redis (optional for caching)
REDIS_URL=redis://localhost:6379/0

# External APIs (optional)
OPENAI_API_KEY=your-openai-key
GITHUB_TOKEN=your-github-token
```

---

## Deployment

### Docker Deployment

```bash
# Build and run all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production Deployment

Sankalpa supports deployment to:

- **Vercel** - Frontend (Next.js)
- **AWS** - Elastic Beanstalk, ECS, Lambda
- **GCP** - App Engine, Cloud Run
- **Azure** - App Service, Container Apps

See [Production Deployment Guide](docs/production-deployment.md) for detailed instructions.

---

## Testing

```bash
# Run all backend tests
pytest

# Run with coverage
pytest --cov=sankalpa tests/

# Run frontend tests
cd frontend && npm test

# Run specific test category
pytest tests/unit/
pytest tests/integration/
pytest tests/e2e/
```

---

## CLI Usage

```bash
# Run the CLI
python cli/cli.py

# Execute a single agent
python cli/cli.py run-agent hello_world --input '{"name": "User"}'

# Execute a workflow
python cli/flow_runner.py composer_flows/example_blog_chain.json
```

---

## Development

### Adding a New Agent

1. Create agent file in appropriate category folder:

```python
# agents/custom/my_agent.py
from agents.base import BaseAgent
from typing import Dict, Any

class MyCustomAgent(BaseAgent):
    def __init__(self, name="my_agent", memory=None):
        super().__init__(name, memory)
        self.category = "custom"
        self.description = "My custom agent description"

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        # Your agent logic here
        return {"result": "success", "data": input_data}
```

2. Register in `catalog/agent_catalog.json`:

```json
{
  "my_agent": {
    "description": "My custom agent",
    "category": "custom",
    "module": "agents.custom.my_agent",
    "class": "MyCustomAgent"
  }
}
```

3. Test your agent:

```bash
curl -X POST http://localhost:9000/api/agents/execute \
  -H "Content-Type: application/json" \
  -d '{"agent_name": "my_agent", "input_data": {"test": true}}'
```

---

## Roadmap

### Current Version (v1.0)

- [x] 35+ specialized agents
- [x] Visual workflow composer
- [x] Memory system with sessions
- [x] Chain execution engine
- [x] REST API with authentication
- [x] Next.js frontend
- [x] Docker deployment

### Upcoming Features

- [ ] Real-time WebSocket collaboration
- [ ] Vector memory with embeddings
- [ ] Advanced LLM fine-tuning UI
- [ ] Agent marketplace
- [ ] VS Code extension
- [ ] Mobile application
- [ ] Enterprise SSO

---

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run tests: `pytest && cd frontend && npm test`
5. Commit: `git commit -m 'Add amazing feature'`
6. Push: `git push origin feature/amazing-feature`
7. Open a Pull Request

---

## Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/yourusername/sankalpa/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/sankalpa/discussions)

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

Sankalpa builds upon concepts from:

- [LangChain](https://langchain.com) - Agent framework
- [CrewAI](https://crewai.com) - Multi-agent collaboration
- [AutoGen](https://microsoft.github.io/autogen/) - Agent conversations
- [GPT Engineer](https://github.com/gpt-engineer-org/gpt-engineer) - Code generation
- [React Flow](https://reactflow.dev) - Visual workflow builder

---

<div align="center">

**Built with intention. Powered by AI.**

[Get Started](#-quick-start) | [Documentation](docs/) | [Contributing](CONTRIBUTING.md)

</div>
