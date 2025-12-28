# Sankalpa System Architecture

## Overview

Sankalpa is a **multi-tier, event-driven architecture** designed for autonomous software development through AI agents. The system follows principles of modularity, scalability, and extensibility.

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                CLIENT LAYER                                      │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│    ┌────────────┐    ┌────────────┐    ┌────────────┐    ┌────────────┐       │
│    │   Web UI   │    │    CLI     │    │  VS Code   │    │  Electron  │       │
│    │ (Next.js)  │    │  (Python)  │    │ Extension  │    │ Desktop App│       │
│    └─────┬──────┘    └─────┬──────┘    └─────┬──────┘    └─────┬──────┘       │
│          │                 │                 │                 │               │
│          └─────────────────┴─────────────────┴─────────────────┘               │
│                                    │                                           │
│                              HTTP/WebSocket                                    │
│                                    │                                           │
└────────────────────────────────────┼───────────────────────────────────────────┘
                                     │
┌────────────────────────────────────┼───────────────────────────────────────────┐
│                                API GATEWAY                                      │
├────────────────────────────────────┼───────────────────────────────────────────┤
│                                    ▼                                           │
│    ┌─────────────────────────────────────────────────────────────────────┐    │
│    │                         FastAPI Server                               │    │
│    │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐           │    │
│    │  │   CORS   │  │   Auth   │  │  Rate    │  │ Metrics  │           │    │
│    │  │Middleware│  │Middleware│  │ Limiter  │  │Middleware│           │    │
│    │  └──────────┘  └──────────┘  └──────────┘  └──────────┘           │    │
│    └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                           │
│    ┌───────────────────────────────┼───────────────────────────────────────┐  │
│    │                          API ROUTERS                                   │  │
│    │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐             │  │
│    │  │ /agents  │  │ /chains  │  │ /memory  │  │  /users  │             │  │
│    │  └──────────┘  └──────────┘  └──────────┘  └──────────┘             │  │
│    │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐             │  │
│    │  │/market   │  │/tenants  │  │  /nlp    │  │/webhooks │             │  │
│    │  └──────────┘  └──────────┘  └──────────┘  └──────────┘             │  │
│    └───────────────────────────────────────────────────────────────────────┘  │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
                                     │
┌────────────────────────────────────┼───────────────────────────────────────────┐
│                              CORE SERVICES                                      │
├────────────────────────────────────┼───────────────────────────────────────────┤
│                                    ▼                                           │
│    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │
│    │   Config    │    │  Security   │    │   Caching   │    │ Monitoring  │  │
│    │  Manager    │    │   Module    │    │   Layer     │    │   System    │  │
│    │  ─────────  │    │  ─────────  │    │  ─────────  │    │  ─────────  │  │
│    │ • Singleton │    │ • JWT Auth  │    │ • In-memory │    │ • Metrics   │  │
│    │ • Env vars  │    │ • RBAC      │    │ • Redis     │    │ • Health    │  │
│    │ • Sections  │    │ • Rate limit│    │ • TTL cache │    │ • Logging   │  │
│    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘  │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
                                     │
┌────────────────────────────────────┼───────────────────────────────────────────┐
│                               AGENT LAYER                                       │
├────────────────────────────────────┼───────────────────────────────────────────┤
│                                    ▼                                           │
│    ┌─────────────────────────────────────────────────────────────────────────┐│
│    │                          AGENT LOADER                                    ││
│    │  • Dynamic import from catalog                                          ││
│    │  • Class instantiation with memory injection                            ││
│    │  • Agent registry management                                            ││
│    └─────────────────────────────────────────────────────────────────────────┘│
│                                    │                                           │
│    ┌────────────────┬──────────────┼──────────────┬────────────────┐          │
│    ▼                ▼              ▼              ▼                ▼          │
│ ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│ │ Builder  │  │ Testing  │  │ Deploy   │  │Marketing │  │ Enhanced │        │
│ │ Agents   │  │ Agents   │  │ Agents   │  │ Agents   │  │ Agents   │        │
│ │ (11)     │  │ (4)      │  │ (3)      │  │ (4)      │  │ (6)      │        │
│ └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │
│                                    │                                           │
│    ┌─────────────────────────────────────────────────────────────────────────┐│
│    │                         CHAIN MANAGER                                    ││
│    │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                  ││
│    │  │  Sequential  │  │   Parallel   │  │ Conditional  │                  ││
│    │  │  Execution   │  │  Execution   │  │  Branching   │                  ││
│    │  └──────────────┘  └──────────────┘  └──────────────┘                  ││
│    └─────────────────────────────────────────────────────────────────────────┘│
│                                    │                                           │
│    ┌─────────────────────────────────────────────────────────────────────────┐│
│    │                        MEMORY MANAGER                                    ││
│    │  • Session-based storage     • Transaction support                       ││
│    │  • Backup and restore        • Cross-agent context sharing               ││
│    └─────────────────────────────────────────────────────────────────────────┘│
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
                                     │
┌────────────────────────────────────┼───────────────────────────────────────────┐
│                               DATA LAYER                                        │
├────────────────────────────────────┼───────────────────────────────────────────┤
│                                    ▼                                           │
│    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐          │
│    │   PostgreSQL    │    │     Redis       │    │  File System    │          │
│    │   ───────────   │    │   ───────────   │    │   ───────────   │          │
│    │  • Users        │    │  • Sessions     │    │  • Agent files  │          │
│    │  • Roles        │    │  • Cache        │    │  • Memory JSON  │          │
│    │  • API Keys     │    │  • Rate limits  │    │  • Logs         │          │
│    │  • Chains       │    │  • Pub/Sub      │    │  • Workflows    │          │
│    │  • Marketplace  │    │                 │    │  • Templates    │          │
│    └─────────────────┘    └─────────────────┘    └─────────────────┘          │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Component Details

### 1. Client Layer

Multiple interfaces for interacting with Sankalpa:

| Interface | Technology | Purpose |
|-----------|------------|---------|
| **Web UI** | Next.js 14, React 18 | Visual workflow composer, dashboard |
| **CLI** | Python (argparse) | Command-line agent execution |
| **VS Code Extension** | TypeScript | IDE integration |
| **Electron App** | Electron, Node.js | Desktop application |

#### Web UI Pages

| Page | Route | Description |
|------|-------|-------------|
| Homepage | `/` | Feature overview and navigation |
| Composer | `/composer` | Visual workflow builder (React Flow) |
| Playground | `/playground` | Interactive agent testing |
| Dashboard | `/dashboard` | System metrics and monitoring |
| Agents | `/agents` | Agent catalog and execution |
| Memory | `/memory` | Memory browser and management |
| Marketplace | `/marketplace` | Agent and workflow marketplace |
| Chat | `/chat` | AI chat interface |

---

### 2. API Gateway (FastAPI)

#### Middleware Stack

```
Request → CORS → Auth → Rate Limit → Metrics → Handler → Response
```

| Middleware | Purpose | Configuration |
|------------|---------|---------------|
| **CORS** | Cross-origin requests | Configurable origins |
| **Auth** | JWT token validation | HS256 algorithm |
| **Rate Limit** | Request throttling | Per-IP limits |
| **Metrics** | Performance tracking | Duration, counts |

#### API Endpoints

| Route | Methods | Description |
|-------|---------|-------------|
| `/api/status` | GET | Health check and version |
| `/api/agents` | GET | List all agents |
| `/api/agents/execute` | POST | Execute single agent |
| `/api/agents/enhanced` | GET | Enhanced agent list |
| `/api/chains` | GET | List chain templates |
| `/api/chains/execute` | POST | Execute agent chain |
| `/api/memory/save` | POST | Save to memory |
| `/api/memory/load` | POST | Load from memory |
| `/api/memory/all` | GET | Get all memory |
| `/api/memory/sessions` | GET | List sessions |
| `/api/users/login` | POST | User authentication |
| `/api/marketplace` | GET, POST | Marketplace operations |

---

### 3. Core Services

#### Configuration Manager (`core/config.py`)

Singleton pattern for centralized configuration:

```python
class Configuration:
    app: AppConfig          # Application settings
    api: ApiConfig          # API configuration
    security: SecurityConfig # Security settings
    memory: MemoryConfig    # Memory settings
    agents: AgentsConfig    # Agent configuration
    logging: LoggingConfig  # Logging settings
```

#### Security Module (`core/security.py` - 308 lines)

| Feature | Implementation |
|---------|----------------|
| JWT Authentication | Access + refresh tokens |
| Password Hashing | bcrypt with salt |
| RBAC | Role-based access control |
| Rate Limiting | Sliding window algorithm |
| Security Headers | XSS, CSRF, Content-Type |

#### Caching Layer (`core/caching.py` - 297 lines)

Multi-level caching strategy:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  In-Memory  │ ──▶ │    Redis    │ ──▶ │  Database   │
│   (L1)      │     │    (L2)     │     │    (L3)     │
│   ~1ms      │     │   ~5ms      │     │   ~50ms     │
└─────────────┘     └─────────────┘     └─────────────┘
```

#### Monitoring System (`core/monitoring.py` - 300 lines)

- System metrics (CPU, memory, disk)
- Request latency tracking
- Agent execution metrics
- Health check endpoints

---

### 4. Agent Layer

#### Agent Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      AGENT ECOSYSTEM                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    BASE AGENT                            │   │
│  │  • name: str                                             │   │
│  │  • description: str                                      │   │
│  │  • category: str                                         │   │
│  │  • memory: MemoryManager                                 │   │
│  │  • run(input_data) -> dict  [ABSTRACT]                  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│              ┌───────────────┼───────────────┐                 │
│              ▼               ▼               ▼                 │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐      │
│  │   BUILDER     │  │   TESTING     │  │   DEPLOY      │      │
│  │   AGENTS      │  │   AGENTS      │  │   AGENTS      │      │
│  │   (11)        │  │   (4)         │  │   (3)         │      │
│  └───────────────┘  └───────────────┘  └───────────────┘      │
│                                                                 │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐      │
│  │  MARKETING    │  │   ENHANCED    │  │    META       │      │
│  │   AGENTS      │  │   AGENTS      │  │   AGENTS      │      │
│  │   (4)         │  │   (6)         │  │   (2)         │      │
│  └───────────────┘  └───────────────┘  └───────────────┘      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### Agent Categories (35+ Total)

| Category | Count | Key Agents |
|----------|-------|------------|
| **Builder** | 11 | project_architect, frontend_builder, backend_builder, api_builder, db_schema, auth_builder, ui_generator |
| **Testing** | 4 | test_suite, integration_test, security_scanner, critic |
| **Deployment** | 3 | deploy_executor, ci_generator, domain_linker |
| **Marketing** | 4 | readme_writer, seo_optimizer, product_hunt_copywriter, pitch_deck_generator |
| **Enhanced** | 6 | copilot, self_replicator, finetuner, plugin_loader, vs_code_extension, cli_runner |
| **Meta** | 2 | multi_agent_memory_manager, version_tracker |
| **Orchestration** | 3 | planner_agent, execution_manager, session_replayer |
| **Custom** | 5+ | hello_world, custom_calculator, text_translator, date_formatter, code_summarizer |

#### Agent Loader (`agents/loader.py`)

Dynamic agent loading system:

```python
def load_agent(agent_name: str) -> BaseAgent:
    1. Look up agent in catalog (agent_catalog.json)
    2. Import module dynamically (importlib)
    3. Get agent class from module
    4. Instantiate with memory manager
    5. Return agent instance
```

#### Chain Manager

Orchestrates agent execution in various patterns:

| Pattern | Description | Use Case |
|---------|-------------|----------|
| **Sequential** | Agents run one after another, output → input | Build pipelines |
| **Parallel** | Agents run concurrently | Independent tasks |
| **Conditional** | Branch based on results | Decision flows |

---

### 5. Memory System

#### Memory Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      MEMORY SYSTEM                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              ENHANCED MEMORY MANAGER                      │  │
│  │                                                           │  │
│  │  save(key, value, session_id)  →  Store data             │  │
│  │  load(key, session_id)         →  Retrieve data          │  │
│  │  get_all(session_id)           →  All session data       │  │
│  │  list_sessions()               →  Available sessions     │  │
│  │  backup(session_id)            →  Create backup          │  │
│  │  restore(backup_id)            →  Restore from backup    │  │
│  │                                                           │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                  │
│              ┌───────────────┼───────────────┐                 │
│              ▼               ▼               ▼                 │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐      │
│  │  JSON Files   │  │    Redis      │  │  PostgreSQL   │      │
│  │  (Default)    │  │  (Sessions)   │  │  (Metadata)   │      │
│  └───────────────┘  └───────────────┘  └───────────────┘      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### Memory Features

| Feature | Description |
|---------|-------------|
| **Sessions** | Isolated memory per session |
| **Transactions** | Atomic operations |
| **Backups** | Point-in-time recovery |
| **Cross-agent** | Shared context between agents |

---

### 6. Data Layer

#### PostgreSQL Schema

```sql
-- Core Tables
users (id, username, email, password_hash, created_at)
roles (id, name, description)
permissions (id, name, resource, action)
user_roles (user_id, role_id)
role_permissions (role_id, permission_id)
api_keys (id, user_id, key_hash, name, expires_at)

-- Domain Tables
chains (id, name, description, agents, created_by)
memory_sessions (id, user_id, created_at, metadata)

-- Marketplace
marketplace_items (id, name, type, author_id, downloads, rating)
reviews (id, item_id, user_id, rating, comment)
```

#### Redis Keys

```
session:<session_id>     → Session data
cache:<key>              → Cached responses
ratelimit:<ip>           → Rate limit counters
pubsub:agents            → Agent events
pubsub:chains            → Chain events
```

#### File System Structure

```
/memory/sessions/         → Session JSON files
/agents/                  → Agent source code
/logs/                    → Application logs
/composer_flows/          → Workflow templates
/catalog/                 → Agent catalog
/projects/                → Generated projects
```

---

## Data Flow Diagrams

### Agent Execution Flow

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Client  │───▶│   API    │───▶│  Agent   │───▶│  Agent   │
│  Request │    │  Router  │    │  Loader  │    │ Instance │
└──────────┘    └──────────┘    └──────────┘    └────┬─────┘
                                                     │
                    ┌────────────────────────────────┘
                    │
                    ▼
┌──────────┐    ┌──────────┐    ┌──────────┐
│  Memory  │◀───│  Agent   │───▶│  Result  │
│  Manager │    │   Run    │    │ Response │
└──────────┘    └──────────┘    └──────────┘
```

### Chain Execution Flow

```
┌──────────┐    ┌──────────┐    ┌─────────────────────────────────┐
│  Input   │───▶│  Chain   │───▶│           AGENT LOOP            │
│  Data    │    │  Manager │    │                                 │
└──────────┘    └──────────┘    │  ┌───────┐      ┌───────┐      │
                                │  │Agent 1│─────▶│Agent 2│─────▶│
                                │  └───┬───┘      └───┬───┘      │
                                │      │              │          │
                                │      ▼              ▼          │
                                │  ┌────────────────────────┐    │
                                │  │    Memory Storage      │    │
                                │  └────────────────────────┘    │
                                └────────────────┬────────────────┘
                                                 │
                                                 ▼
                                          ┌──────────┐
                                          │  Final   │
                                          │  Output  │
                                          └──────────┘
```

---

## Security Architecture

### Authentication Flow

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Login   │───▶│ Validate │───▶│ Generate │───▶│  Return  │
│ Request  │    │ Password │    │   JWT    │    │  Tokens  │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
                                                      │
┌──────────┐    ┌──────────┐    ┌──────────┐          │
│ Protected│◀───│  Check   │◀───│  Decode  │◀─────────┘
│ Resource │    │  Roles   │    │   JWT    │
└──────────┘    └──────────┘    └──────────┘
```

### Authorization Model

```
User ──▶ Roles ──▶ Permissions ──▶ Resources

Example:
admin     ──▶  [admin]      ──▶  [*:*]           ──▶  All resources
developer ──▶  [developer]  ──▶  [agents:execute] ──▶  Agent execution
viewer    ──▶  [viewer]     ──▶  [agents:read]   ──▶  Read-only
```

---

## Deployment Architecture

### Docker Compose

```yaml
version: '3.8'
services:
  backend:
    image: sankalpa-backend
    ports: ["9000:9000"]
    environment:
      - DATABASE_URL=postgresql://...
      - REDIS_URL=redis://redis:6379
    depends_on: [postgres, redis]

  frontend:
    image: sankalpa-frontend
    ports: ["9001:3000"]
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:9000
    depends_on: [backend]

  postgres:
    image: postgres:14
    ports: ["5432:5432"]
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]
```

### Production Deployment

```
┌─────────────────────────────────────────────────────────────────┐
│                           CDN                                    │
│                     (CloudFront/Fastly)                          │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────┼─────────────────────────────────────┐
│                     Load Balancer                                  │
│                     (ALB/nginx)                                    │
└─────────────────────────────────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
    ┌──────────┐        ┌──────────┐        ┌──────────┐
    │ Backend  │        │ Backend  │        │ Backend  │
    │ Instance │        │ Instance │        │ Instance │
    └──────────┘        └──────────┘        └──────────┘
          │                   │                   │
          └───────────────────┼───────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
    ┌──────────┐        ┌──────────┐        ┌──────────┐
    │PostgreSQL│        │  Redis   │        │   S3     │
    │  (RDS)   │        │(ElastiC.)│        │ Storage  │
    └──────────┘        └──────────┘        └──────────┘
```

---

## Scalability

### Horizontal Scaling

| Component | Strategy |
|-----------|----------|
| API | Stateless, load balanced |
| Sessions | Redis for shared state |
| Database | Read replicas, connection pooling |
| Files | S3/object storage |

### Performance Targets

| Metric | Target |
|--------|--------|
| API latency (p99) | < 200ms |
| Agent execution | < 5s average |
| Chain execution | < 30s average |
| Memory operations | < 50ms |

---

## Technology Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js 14, React 18, TailwindCSS, React Flow |
| Backend | FastAPI 0.103, Python 3.10+, Uvicorn |
| Database | PostgreSQL 14, SQLAlchemy 2.0 |
| Cache | Redis 7 |
| Auth | JWT (python-jose), bcrypt |
| Container | Docker, Docker Compose |
| CI/CD | GitHub Actions |
| Testing | pytest, Jest |
