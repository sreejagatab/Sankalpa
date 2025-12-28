# Sankalpa System Reference

## Core Purpose

Sankalpa is a **production-ready, multi-agent AI platform** for autonomous software development. It is NOT just a chat system - it's an AI Operating System that can autonomously build, test, deploy, and maintain complete software applications.

## Quick Reference

| Component | Location | Description |
|-----------|----------|-------------|
| Backend API | `backend/simple_main.py` | FastAPI server on port 9000 |
| Frontend | `frontend/` | Next.js 14 app on port 9001 |
| Agents | `agents/` | 35+ specialized AI agents |
| Memory | `memory/` | Session-based persistent memory |
| Core | `core/` | Config, security, caching, monitoring |

## Key Commands

```bash
# Start full system
python run_sankalpa.py

# Start backend only
python -m uvicorn backend.simple_main:app --host 0.0.0.0 --port 9000

# Start frontend only
cd frontend && npm run dev

# Docker deployment
docker-compose up -d
```

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/status` | GET | Health check |
| `/api/agents` | GET | List all agents |
| `/api/agents/execute` | POST | Execute agent |
| `/api/chains` | GET | List chain templates |
| `/api/chains/execute` | POST | Execute chain |
| `/api/memory/save` | POST | Save to memory |
| `/api/memory/load` | POST | Load from memory |

## Agent Categories (35+ Agents)

| Category | Count | Examples |
|----------|-------|----------|
| Builder | 11 | project_architect, frontend_builder, backend_builder |
| Testing | 4 | test_suite, security_scanner, critic |
| Deployment | 3 | deploy_executor, ci_generator |
| Marketing | 4 | readme_writer, seo_optimizer |
| Enhanced | 6 | self_replicator, finetuner, copilot |
| Meta | 2 | multi_agent_memory_manager |
| Orchestration | 3 | planner_agent, execution_manager |
| Custom | 5+ | hello_world, custom_calculator |

## Key Features

- **Autonomous AI Development**: Build complete applications from prompts
- **35+ Specialized Agents**: Builder, testing, deployment, marketing agents
- **Visual Workflow Composer**: Drag-and-drop agent chain builder
- **Persistent Memory**: Session-based context with transactions
- **Self-Replicating Agents**: Agents that create new agents
- **LLM Fine-Tuning**: Automated fine-tuning pipeline
- **Multi-Tenancy**: Enterprise organization support
- **Marketplace**: Share and monetize agents

## Architecture Overview

```
Client Layer (Web, CLI, VS Code)
         │
    API Gateway (FastAPI + JWT + RBAC)
         │
    Core Services (Config, Security, Cache, Monitor)
         │
    Agent Layer (35+ Agents + Chain Manager + Memory)
         │
    Data Layer (PostgreSQL, Redis, File System)
```

## Integration Protocols

| Protocol | Purpose | Implementation |
|----------|---------|----------------|
| LangChain | Agent chaining | ChainManager |
| MCP | Model Context | Agent orchestration |
| CrewAI | Multi-agent | Role-based agents |
| AutoGen | Task planning | PlannerAgent |
| ReAct | Reasoning | Copilot, Critic |
| PromptFlow | Visual workflows | Composer UI |
| GPT Engineer | Code generation | Builder agents |

## File Structure

```
sankalpa/
├── agents/           # 35+ AI agents
│   ├── builder/      # Code generation
│   ├── testing/      # Test creation
│   ├── deployment/   # CI/CD
│   ├── marketing/    # Documentation
│   └── enhanced/     # Self-replication, fine-tuning
├── backend/          # FastAPI server
│   ├── routers/      # API endpoints
│   └── db/           # Database models
├── core/             # Core services
├── memory/           # Memory system
├── frontend/         # Next.js UI
│   ├── pages/        # App pages
│   └── components/   # React components
├── marketplace/      # Marketplace module
├── tenants/          # Multi-tenancy
├── tests/            # Test suites
└── docs/             # Documentation
```

## Environment Variables

```bash
# Required
SANKALPA_JWT_SECRET=your-secret-key

# Optional
API_PORT=9000
POSTGRES_URL=postgresql://...
REDIS_URL=redis://...
OPENAI_API_KEY=...
```

## Development Notes

- All agents inherit from `BaseAgent` in `agents/base.py`
- Chain execution passes output of one agent as input to next
- Memory sessions are isolated by session_id
- Use `@cached` decorator for expensive operations
- Rate limiting is per-IP address
