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
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://docker.com)
[![GitHub Stars](https://img.shields.io/github/stars/sreejagatab/Sankalpa?style=social)](https://github.com/sreejagatab/Sankalpa)
[![GitHub Forks](https://img.shields.io/github/forks/sreejagatab/Sankalpa?style=social)](https://github.com/sreejagatab/Sankalpa/fork)
[![GitHub Issues](https://img.shields.io/github/issues/sreejagatab/Sankalpa)](https://github.com/sreejagatab/Sankalpa/issues)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

[Features](#-key-features) | [Quick Start](#-quick-start) | [Demo](#-screenshots--demo) | [Architecture](#-architecture) | [Agents](#-agent-ecosystem) | [API](#-api-reference) | [Examples](#-real-world-examples) | [FAQ](#-faq) | [Docs](#-documentation)

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

## Screenshots & Demo

### Visual Workflow Composer

```
┌─────────────────────────────────────────────────────────────────────────┐
│  SANKALPA WORKFLOW COMPOSER                                    [─][□][×]│
├─────────────────────────────────────────────────────────────────────────┤
│ ┌─────────────┐                                                         │
│ │ AGENTS      │    ┌──────────┐      ┌──────────┐      ┌──────────┐   │
│ ├─────────────┤    │ Project  │─────▶│ Frontend │─────▶│  Deploy  │   │
│ │ ○ Architect │    │ Architect│      │ Builder  │      │ Executor │   │
│ │ ○ Frontend  │    └──────────┘      └──────────┘      └──────────┘   │
│ │ ○ Backend   │          │                                    │        │
│ │ ○ Database  │          │           ┌──────────┐             │        │
│ │ ○ Auth      │          └──────────▶│ Backend  │─────────────┘        │
│ │ ○ Deploy    │                      │ Builder  │                      │
│ │ ○ Test      │                      └──────────┘                      │
│ └─────────────┘                                                         │
│                                                                         │
│ [▶ Run Chain]  [💾 Save]  [📤 Export]                    Agents: 4     │
└─────────────────────────────────────────────────────────────────────────┘
```

### Agent Playground

```
┌─────────────────────────────────────────────────────────────────────────┐
│  AGENT PLAYGROUND                                              [─][□][×]│
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Select Agent: [project_architect     ▼]                               │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ INPUT                                                            │   │
│  ├─────────────────────────────────────────────────────────────────┤   │
│  │ {                                                                │   │
│  │   "app_name": "MyBlog",                                         │   │
│  │   "type": "web",                                                │   │
│  │   "features": ["auth", "posts", "comments"]                     │   │
│  │ }                                                                │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  [▶ Execute Agent]                                                      │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ OUTPUT                                              ✓ Success    │   │
│  ├─────────────────────────────────────────────────────────────────┤   │
│  │ {                                                                │   │
│  │   "project_structure": { ... },                                 │   │
│  │   "modules": ["auth", "blog", "api"],                           │   │
│  │   "execution_time": 0.023                                       │   │
│  │ }                                                                │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Dashboard

```
┌─────────────────────────────────────────────────────────────────────────┐
│  SANKALPA DASHBOARD                                            [─][□][×]│
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │  35+        │  │  156        │  │  12         │  │  99.9%      │   │
│  │  Agents     │  │  Executions │  │  Chains     │  │  Uptime     │   │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘   │
│                                                                         │
│  RECENT EXECUTIONS                          AGENT USAGE                 │
│  ┌────────────────────────────────┐        ┌────────────────────────┐  │
│  │ ● project_architect  0.02s ✓  │        │ ████████████ frontend  │  │
│  │ ● frontend_builder   0.15s ✓  │        │ ██████████   backend   │  │
│  │ ● backend_builder    0.12s ✓  │        │ ████████     architect │  │
│  │ ● test_suite         0.08s ✓  │        │ ██████       deploy    │  │
│  │ ● deploy_executor    1.23s ✓  │        │ ████         test      │  │
│  └────────────────────────────────┘        └────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

> **Note**: For actual screenshots, run Sankalpa locally and visit `http://localhost:9001`

---

## Real-World Examples

### Example 1: Build a Complete Blog Platform

```bash
# Using the API
curl -X POST http://localhost:9000/api/chains/execute \
  -H "Content-Type: application/json" \
  -d '{
    "chain_name": "blog_builder",
    "agents": ["project_architect", "db_schema", "backend_builder", "frontend_builder", "auth_builder", "deploy_executor"],
    "input_data": {
      "app_name": "TechBlog",
      "features": ["authentication", "markdown_editor", "comments", "dark_mode", "SEO"],
      "database": "postgresql",
      "deploy_target": "vercel"
    }
  }'
```

**Output**: Complete blog with:
- User authentication (JWT)
- Markdown post editor
- Comment system
- Dark/light mode toggle
- SEO-optimized pages
- Deployed to Vercel

### Example 2: Generate a REST API

```bash
curl -X POST http://localhost:9000/api/chains/execute \
  -H "Content-Type: application/json" \
  -d '{
    "chain_name": "api_generator",
    "agents": ["db_schema", "backend_builder", "api_builder", "test_suite"],
    "input_data": {
      "resource": "products",
      "fields": ["id", "name", "description", "price", "category", "stock"],
      "operations": ["CRUD", "search", "filter", "paginate"]
    }
  }'
```

**Output**:
- Database models and migrations
- RESTful API endpoints
- Input validation
- Unit tests
- OpenAPI documentation

### Example 3: Create a SaaS Dashboard

```bash
curl -X POST http://localhost:9000/api/chains/execute \
  -H "Content-Type: application/json" \
  -d '{
    "chain_name": "saas_builder",
    "agents": ["project_architect", "auth_builder", "frontend_builder", "stripe_payment", "email_system"],
    "input_data": {
      "app_name": "AnalyticsDash",
      "features": ["user_auth", "subscription_tiers", "usage_analytics", "email_notifications"],
      "payment_provider": "stripe",
      "email_provider": "sendgrid"
    }
  }'
```

**Output**:
- Multi-tenant authentication
- Stripe subscription integration
- Usage tracking dashboard
- Email notification system
- Admin panel

### Example 4: Build a Mobile-Ready PWA

```bash
curl -X POST http://localhost:9000/api/agents/execute \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "frontend_builder",
    "input_data": {
      "type": "pwa",
      "features": ["offline_support", "push_notifications", "installable"],
      "responsive": true,
      "theme": "modern_minimal"
    }
  }'
```

### Example 5: Generate Marketing Materials

```bash
curl -X POST http://localhost:9000/api/chains/execute \
  -H "Content-Type: application/json" \
  -d '{
    "chain_name": "marketing_suite",
    "agents": ["readme_writer", "seo_optimizer", "product_hunt_copywriter", "pitch_deck_generator"],
    "input_data": {
      "product_name": "MyAwesomeApp",
      "tagline": "The future of productivity",
      "target_audience": "developers",
      "key_features": ["AI-powered", "Real-time collaboration", "Cloud-native"]
    }
  }'
```

**Output**:
- Professional README.md
- SEO meta tags and keywords
- Product Hunt launch copy
- 10-slide pitch deck outline

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
git clone https://github.com/sreejagatab/Sankalpa.git
cd Sankalpa

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
| **API Docs** | http://localhost:9000/api/docs | Swagger UI |
| **API Status** | http://localhost:9000/api/status | Health check |

### Verify Installation

```bash
# Check API status
curl http://localhost:9000/api/status
# Expected: {"status": "Sankalpa API Server is running!", "version": "1.0.0"}

# List available agents
curl http://localhost:9000/api/agents
# Expected: {"agents": [...]}

# Execute a test agent
curl -X POST http://localhost:9000/api/agents/execute \
  -H "Content-Type: application/json" \
  -d '{"agent_name": "hello_world", "input_data": {"name": "Sankalpa"}}'
# Expected: {"result": {"greeting": "Hello, Sankalpa!"}, ...}
```

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

For complete API documentation, see [docs/API.md](docs/API.md).

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

## Security

### Authentication & Authorization

| Feature | Implementation |
|---------|----------------|
| **JWT Tokens** | HS256 algorithm, configurable expiry |
| **Password Hashing** | bcrypt with salt |
| **Role-Based Access** | Admin, User, Guest roles |
| **Rate Limiting** | 100 requests/minute per IP |
| **CORS Protection** | Configurable allowed origins |

### Security Best Practices

1. **Environment Variables**: Never commit `.env` files
2. **JWT Secret**: Use a strong, random secret (32+ characters)
3. **HTTPS**: Always use HTTPS in production
4. **Input Validation**: All inputs are validated before processing
5. **SQL Injection**: Parameterized queries via SQLAlchemy
6. **XSS Protection**: React's built-in escaping + CSP headers

### Security Configuration

```bash
# .env security settings
SANKALPA_JWT_SECRET=your-very-long-random-secret-key-here
SANKALPA_JWT_ALGORITHM=HS256
SANKALPA_JWT_EXPIRE_MINUTES=30
SANKALPA_ALLOWED_ORIGINS=https://yourdomain.com
SANKALPA_RATE_LIMIT=100
```

### Reporting Vulnerabilities

Found a security issue? Please email security@sankalpa.dev (do not open public issues for security vulnerabilities).

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

## Troubleshooting

### Common Issues

#### Backend won't start

```bash
# Check if port 9000 is in use
netstat -ano | findstr :9000  # Windows
lsof -i :9000                  # Linux/Mac

# Kill the process using the port
taskkill /PID <pid> /F         # Windows
kill -9 <pid>                  # Linux/Mac
```

#### Frontend build fails

```bash
# Clear node_modules and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
```

#### Agent not found error

```bash
# Verify agent exists in catalog
cat catalog/agent_catalog.json | grep "agent_name"

# Check agent file exists
ls agents/custom/
```

#### Memory/session issues

```bash
# Clear all sessions
rm -rf memory/sessions/*.json

# Restart the backend
python -m uvicorn backend.simple_main:app --reload
```

#### Database connection failed

```bash
# Check PostgreSQL is running
pg_isready -h localhost -p 5432

# Verify connection string in .env
echo $POSTGRES_HOST
```

#### CORS errors in browser

```bash
# Add your frontend URL to allowed origins in .env
SANKALPA_ALLOWED_ORIGINS=http://localhost:9001,http://localhost:3000
```

### Debug Mode

Enable verbose logging:

```bash
# Set in .env
SANKALPA_DEBUG=true
SANKALPA_LOG_LEVEL=DEBUG

# Or run with debug flag
python -m uvicorn backend.simple_main:app --reload --log-level debug
```

### Getting Help

1. Check the [FAQ](#-faq) below
2. Search [GitHub Issues](https://github.com/sreejagatab/Sankalpa/issues)
3. Open a new issue with:
   - Error message
   - Steps to reproduce
   - Environment info (OS, Python version, Node version)

---

## FAQ

### General Questions

<details>
<summary><b>What is Sankalpa?</b></summary>

Sankalpa is a multi-agent AI platform that autonomously builds, tests, and deploys complete software applications. Give it a prompt, and it orchestrates 35+ specialized AI agents to create your application.
</details>

<details>
<summary><b>Is Sankalpa free to use?</b></summary>

Yes, Sankalpa is open-source under the MIT license. You can use it freely for personal and commercial projects.
</details>

<details>
<summary><b>Do I need an OpenAI API key?</b></summary>

The base agents work without an OpenAI key (they generate templates and scaffolds). For AI-powered code generation and intelligent suggestions, you'll need an OpenAI API key or another LLM provider.
</details>

<details>
<summary><b>What languages/frameworks does Sankalpa support?</b></summary>

Currently:
- **Frontend**: Next.js, React, TailwindCSS
- **Backend**: FastAPI (Python), Express (Node.js coming soon)
- **Database**: PostgreSQL, SQLite
- **Deployment**: Vercel, AWS, GCP, Azure
</details>

### Technical Questions

<details>
<summary><b>How do I create a custom agent?</b></summary>

1. Create a Python file in `agents/custom/`:
```python
from agents.base import BaseAgent

class MyAgent(BaseAgent):
    def __init__(self):
        super().__init__("my_agent")
        self.description = "My custom agent"

    def run(self, input_data):
        return {"result": "success"}
```

2. Register in `catalog/agent_catalog.json`
3. Restart the backend

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed instructions.
</details>

<details>
<summary><b>How does memory persistence work?</b></summary>

Sankalpa uses a session-based memory system:
- Each session has a unique ID
- Data is stored as JSON files in `memory/sessions/`
- Agents can save/load context across executions
- Sessions can be resumed or cleared

```python
# Save to memory
memory.save("key", {"data": "value"})

# Load from memory
data = memory.load("key")
```
</details>

<details>
<summary><b>Can agents run in parallel?</b></summary>

Yes! The Chain Manager supports:
- **Sequential**: Agents run one after another
- **Parallel**: Independent agents run simultaneously
- **Conditional**: Agents run based on previous results

```json
{
  "execution_mode": "parallel",
  "agents": ["frontend_builder", "backend_builder"]
}
```
</details>

<details>
<summary><b>How do I add authentication to my app?</b></summary>

Use the `auth_builder` agent:
```bash
curl -X POST http://localhost:9000/api/agents/execute \
  -H "Content-Type: application/json" \
  -d '{"agent_name": "auth_builder", "input_data": {"type": "jwt", "features": ["login", "signup", "password_reset"]}}'
```
</details>

<details>
<summary><b>What's the difference between agents and chains?</b></summary>

- **Agent**: A single specialized AI that performs one task
- **Chain**: A workflow that connects multiple agents to complete complex tasks

Think of agents as workers and chains as assembly lines.
</details>

### Deployment Questions

<details>
<summary><b>How do I deploy to production?</b></summary>

1. Set production environment variables
2. Build the frontend: `cd frontend && npm run build`
3. Use Docker Compose or your preferred hosting

See [docs/production-deployment.md](docs/production-deployment.md) for detailed steps.
</details>

<details>
<summary><b>Can I use Sankalpa with my own LLM?</b></summary>

Yes, you can configure custom LLM endpoints in the agent configuration. Support for:
- OpenAI API-compatible endpoints
- Local models (Ollama, LM Studio)
- Azure OpenAI
- Anthropic Claude
</details>

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
- [ ] Kubernetes Helm charts
- [ ] GraphQL API
- [ ] Plugin system

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

## Documentation

| Document | Description |
|----------|-------------|
| [README.md](README.md) | This file - project overview |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contribution guidelines |
| [CLAUDE.md](CLAUDE.md) | AI assistant quick reference |
| [docs/API.md](docs/API.md) | Complete API documentation |
| [docs/system_architecture.md](docs/system_architecture.md) | Architecture deep-dive |
| [docs/production-deployment.md](docs/production-deployment.md) | Deployment guide |

---

## Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/sreejagatab/Sankalpa/issues)
- **Discussions**: [GitHub Discussions](https://github.com/sreejagatab/Sankalpa/discussions)

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

[Get Started](#-quick-start) | [Documentation](docs/) | [Contributing](CONTRIBUTING.md) | [Report Bug](https://github.com/sreejagatab/Sankalpa/issues)

---

Made with love by the Sankalpa Team

</div>
