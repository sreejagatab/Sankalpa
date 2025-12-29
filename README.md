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
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](./CONTRIBUTING.md)
[![Agents](https://img.shields.io/badge/Agents-35+-purple.svg)](#agent-ecosystem)
[![OpenAI](https://img.shields.io/badge/OpenAI-Integrated-412991.svg)](#llm-integration)

**[Features](#-key-features)** | **[Quick Start](#-quick-start)** | **[Architecture](#-system-architecture)** | **[Agents](#-agent-ecosystem)** | **[API](./docs/API.md)** | **[Deployment](./docs/deployment-guide.md)**

</div>

---
<img width="1536" height="1024" alt="20251229_1644_Sankalpa AI Platform_simple_compose_01kdnfxh8ke2gr114mn57p8k0g" src="https://github.com/user-attachments/assets/6e77ebc7-4719-4797-b2ec-9b7f5e024515" />
---

## Table of Contents

<details>
<summary><b>Click to expand full Table of Contents</b></summary>

### Overview
- [What is Sankalpa?](#-what-is-sankalpa)
- [Key Features](#-key-features)
- [What Makes Sankalpa Unique](#what-makes-sankalpa-unique)
- [Version 2.0 Features](#new-in-version-20)

### Getting Started
- [Quick Start](#-quick-start)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running Sankalpa](#run-sankalpa)
- [Access Points](#access-points)
- [Verify Installation](#verify-installation)

### Architecture
- [System Architecture](#-system-architecture)
- [High-Level Overview](#high-level-architecture-diagram)
- [Component Architecture](#component-architecture)
- [Data Flow Diagrams](#-data-flow-diagrams)
- [Request Lifecycle](#request-lifecycle)
- [Agent Execution Pipeline](#agent-execution-pipeline)
- [Chain Execution Flow](#chain-execution-flow)
- [Memory System Flow](#memory-system-flow)
- [Directory Structure](#directory-structure)

### Agent Ecosystem
- [Agent Ecosystem Overview](#-agent-ecosystem)
- [Agent Categories](#agent-categories-overview)
- [Builder Agents (11)](#-builder-agents-11)
- [Testing Agents (4)](#-testing-agents-4)
- [Deployment Agents (3)](#-deployment-agents-3)
- [Marketing Agents (4)](#-marketing-agents-4)
- [Enhanced Agents (6)](#-enhanced-agents-6)
- [Meta Agents (2)](#-meta-agents-2)
- [Orchestration Agents (3)](#-orchestration-agents-3)
- [Custom Agents](#-custom-agents)
- [Creating Custom Agents](#creating-a-custom-agent)

### Core Components
- [Backend API](#-backend-api)
- [Frontend Application](#-frontend-application)
- [Memory System](#-memory-system)
- [Chain Manager](#-chain-manager)
- [LLM Integration](#-llm-integration)
- [Plugin System](#-plugin-system)

### API Reference
- [API Overview](#-api-reference)
- [Authentication](#authentication)
- [Agents API](#agents-api)
- [Chains API](#chains-api)
- [Memory API](#memory-api)
- [GraphQL API](#graphql-api)
- [WebSocket API](#websocket-api)
- [SSO API](#sso-api)
- [Fine-tuning API](#fine-tuning-api)

### Visual Interfaces
- [Workflow Composer](#-visual-workflow-composer)
- [Agent Playground](#agent-playground)
- [Dashboard](#dashboard)
- [Marketplace](#marketplace)
- [Fine-tuning UI](#fine-tuning-ui)

### Test Results & Benchmarks
- [LLM Integration Test Results](#-llm-integration-test-results)
- [Performance Benchmarks](#performance-benchmarks)
- [Test Coverage](#test-coverage)

### Real-World Examples
- [Example 1: Complete Blog Platform](#example-1-build-a-complete-blog-platform)
- [Example 2: REST API Generation](#example-2-generate-a-rest-api)
- [Example 3: SaaS Dashboard](#example-3-create-a-saas-dashboard)
- [Example 4: Mobile-Ready PWA](#example-4-build-a-mobile-ready-pwa)
- [Example 5: Marketing Materials](#example-5-generate-marketing-materials)

### Security
- [Security Overview](#-security)
- [Authentication & Authorization](#authentication--authorization)
- [Security Best Practices](#security-best-practices)
- [Enterprise SSO](#enterprise-sso)

### Configuration
- [Environment Variables](#-configuration)
- [Security Configuration](#security-configuration)
- [Database Configuration](#database-configuration)
- [LLM Configuration](#llm-configuration)

### Deployment
- [Docker Deployment](#-deployment)
- [Kubernetes (Helm)](#kubernetes-deployment-helm)
- [Cloud Deployment](#cloud-deployment)
- [Production Checklist](#production-checklist)

### Integrations & Protocols
- [Supported Protocols](#-protocols--integrations)
- [External Integrations](#external-integrations)

### Troubleshooting
- [Common Issues](#-troubleshooting)
- [Debug Mode](#debug-mode)
- [Getting Help](#getting-help)

### FAQ
- [General Questions](#general-questions)
- [Technical Questions](#technical-questions)
- [Deployment Questions](#deployment-questions)

### Development
- [Contributing](#-contributing)
- [Adding New Agents](#adding-a-new-agent)
- [Development Setup](#development-setup)
- [Testing](#testing)

### Resources
- [Documentation](#-documentation)
- [Roadmap](#-roadmap)
- [Support](#-support)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)

</details>

---

## What is Sankalpa?

**Sankalpa** (Sanskrit: "intention" or "will") is a production-ready, enterprise-grade **multi-agent AI platform** that autonomously builds, tests, deploys, and maintains complete software applications. It's not just a chatbot or code assistant - it's an **AI Operating System for Software Development**.

### The Vision

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           SANKALPA: FROM PROMPT TO PRODUCTION                    │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│   "Build me a blog with auth, markdown editor, and dark mode"                   │
│                              │                                                   │
│                              ▼                                                   │
│   ┌──────────────────────────────────────────────────────────────────────────┐  │
│   │                         SANKALPA ORCHESTRATION                            │  │
│   │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐       │  │
│   │  │ Planner │─▶│ Builder │─▶│ Testing │─▶│ Deploy  │─▶│Marketing│       │  │
│   │  │  Agent  │  │ Agents  │  │ Agents  │  │ Agents  │  │ Agents  │       │  │
│   │  └─────────┘  └─────────┘  └─────────┘  └─────────┘  └─────────┘       │  │
│   └──────────────────────────────────────────────────────────────────────────┘  │
│                              │                                                   │
│                              ▼                                                   │
│   ┌──────────────────────────────────────────────────────────────────────────┐  │
│   │  OUTPUTS:                                                                 │  │
│   │  [x] Next.js Frontend    [x] FastAPI Backend    [x] PostgreSQL Schema    │  │
│   │  [x] JWT Authentication  [x] Markdown Editor    [x] Dark Mode Toggle     │  │
│   │  [x] Unit Tests          [x] E2E Tests          [x] CI/CD Pipeline       │  │
│   │  [x] Vercel Deployment   [x] README.md          [x] SEO Optimization     │  │
│   └──────────────────────────────────────────────────────────────────────────┘  │
│                              │                                                   │
│                              ▼                                                   │
│                     LIVE APPLICATION DEPLOYED                                    │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

Give Sankalpa a prompt like *"Build me a blog with authentication, markdown editor, and dark mode"* and watch it:

| Step | Agent | Action | Output |
|------|-------|--------|--------|
| 1 | `planner_agent` | Plan architecture | Module structure, tech stack |
| 2 | `project_architect` | Create project structure | Folder hierarchy, configs |
| 3 | `db_schema` | Design database | SQLAlchemy models, migrations |
| 4 | `backend_builder` | Build API server | FastAPI routes, middleware |
| 5 | `auth_builder` | Create authentication | JWT tokens, login/signup |
| 6 | `frontend_builder` | Generate UI | Next.js pages, components |
| 7 | `ui_generator` | Build components | Buttons, forms, layouts |
| 8 | `test_suite` | Write tests | Unit tests, integration tests |
| 9 | `deploy_executor` | Deploy application | Vercel/AWS/GCP deployment |
| 10 | `readme_writer` | Generate docs | Professional README |
| 11 | `seo_optimizer` | Optimize SEO | Meta tags, sitemap |

---

## Key Features

### Core Capabilities Matrix

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           SANKALPA CAPABILITIES MATRIX                           │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  AGENTS           WORKFLOWS         MEMORY           DEPLOYMENT                  │
│  ═══════          ═════════         ══════           ══════════                  │
│  [x] 35+ Agents   [x] Visual UI     [x] Sessions     [x] Docker                  │
│  [x] Categories   [x] Drag-Drop     [x] Persist      [x] K8s Helm                │
│  [x] Custom       [x] Templates     [x] Vector DB    [x] AWS/GCP                 │
│  [x] Self-Rep     [x] Export        [x] Transactions [x] Vercel                  │
│                                                                                  │
│  API              SECURITY          ENTERPRISE       INTEGRATIONS                │
│  ═══              ════════          ══════════       ════════════                │
│  [x] REST         [x] JWT Auth      [x] Multi-Tenant [x] OpenAI                  │
│  [x] GraphQL      [x] RBAC          [x] SSO (SAML)   [x] GitHub                  │
│  [x] WebSocket    [x] Rate Limit    [x] Org Support  [x] Stripe                  │
│  [x] OpenAPI      [x] CORS          [x] Audit Logs   [x] SendGrid                │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Feature Comparison Table

| Feature | Description | Status |
|---------|-------------|--------|
| **35+ Specialized AI Agents** | Builder, testing, deployment, marketing, and meta agents | ✅ Complete |
| **Visual Workflow Composer** | Drag-and-drop agent chain builder with React Flow | ✅ Complete |
| **Persistent Memory System** | Session-based context with transaction support | ✅ Complete |
| **Chain Execution Engine** | Sequential, parallel, and conditional agent workflows | ✅ Complete |
| **Self-Replicating Agents** | Agents that create new agents from text prompts | ✅ Complete |
| **LLM Fine-Tuning** | Automated fine-tuning pipeline with visual UI | ✅ Complete |
| **Multi-Tenancy** | Enterprise-ready with organization support | ✅ Complete |
| **Marketplace** | Share, publish, install agents and workflows | ✅ Complete |
| **OpenAI Integration** | GPT-4o-mini powered code generation | ✅ Complete |
| **Context Sharing** | Agents share context through chain execution | ✅ Complete |

### New in Version 2.0

| Feature | Description | Technology |
|---------|-------------|------------|
| **Intelligent Orchestrator** | Auto-analyzes tasks & creates optimal chains | `intelligent_orchestrator.py` |
| **Agent Contracts** | Input/Output schemas & dependency validation | Pydantic + DependencyResolver |
| **Context Optimization** | Agents only receive relevant context (~40% token savings) | `contracts.py` |
| **Real-time WebSocket** | Live collaboration with pub/sub | Redis + WebSocket |
| **Vector Memory** | Semantic search capabilities | ChromaDB/Pinecone/Weaviate |
| **GraphQL API** | Flexible queries and mutations | Strawberry + Apollo Client |
| **Plugin System** | Extensible architecture | 50+ hook points |
| **Fine-tuning UI** | Visual dataset management | React + OpenAI API |
| **VS Code Extension** | Editor integration | TypeScript Extension API |
| **Enterprise SSO** | Single sign-on support | SAML 2.0, OIDC |
| **Helm Charts** | Kubernetes deployment | AWS EKS/GCP GKE/Azure AKS |
| **Mobile PWA** | Offline-first mobile | Service Workers + IndexedDB |
| **LLM Integration** | Real AI-powered generation | OpenAI GPT-4o-mini |

### What Makes Sankalpa Unique

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         SANKALPA vs OTHER TOOLS                                  │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  Feature              │ ChatGPT │ Copilot │ GPT Engineer │ Sankalpa             │
│  ─────────────────────┼─────────┼─────────┼──────────────┼──────────────────    │
│  Multi-Agent System   │   No    │   No    │    No        │  ✅ 35+ Agents       │
│  Auto-Orchestration   │   No    │   No    │    No        │  ✅ Task → Chain     │
│  Visual Workflows     │   No    │   No    │    No        │  ✅ Drag-n-Drop      │
│  Persistent Memory    │ Limited │   No    │    No        │  ✅ Full Sessions    │
│  Self-Replication     │   No    │   No    │    No        │  ✅ Agents → Agents  │
│  Enterprise SSO       │   No    │   No    │    No        │  ✅ SAML/OIDC        │
│  Fine-tuning UI       │   No    │   No    │    No        │  ✅ Visual Manager   │
│  Marketplace          │   No    │   No    │    No        │  ✅ Share/Install    │
│  Full Stack Deploy    │   No    │   No    │  Partial     │  ✅ Complete CI/CD   │
│  Context Accumulation │   No    │   No    │    No        │  ✅ Chain Memory     │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Quick Start

### Prerequisites

| Requirement | Minimum Version | Recommended | Purpose |
|-------------|-----------------|-------------|---------|
| **Python** | 3.10+ | 3.11+ | Backend runtime |
| **Node.js** | 18+ | 20+ | Frontend runtime |
| **npm** | 9+ | 10+ | Package management |
| **PostgreSQL** | 14+ | 15+ | Production database (optional) |
| **Redis** | 7+ | 7.2+ | Caching & pub/sub (optional) |
| **Docker** | 24+ | 25+ | Container deployment (optional) |
| **OpenAI API Key** | - | - | LLM-powered generation (optional) |

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/sreejagatab/Sankalpa.git
cd Sankalpa

# 2. Backend setup
python -m venv venv

# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# 3. Frontend setup
cd frontend
npm install
cd ..

# 4. Configure environment
cp .env.example .env

# Edit .env with your settings:
# - SANKALPA_JWT_SECRET (required)
# - OPENAI_API_KEY (optional, for LLM features)
```

### Run Sankalpa

**Option 1: Full System Launcher (Recommended)**
```bash
python run_sankalpa.py
```

**Option 2: Run Services Separately**
```bash
# Terminal 1: Backend API (port 9000)
python -m uvicorn backend.simple_main:app --host 0.0.0.0 --port 9000 --reload

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
| **Dashboard** | http://localhost:9001/dashboard | System metrics |
| **Marketplace** | http://localhost:9001/marketplace | Agent marketplace |
| **Fine-tuning** | http://localhost:9001/finetuning | LLM fine-tuning UI |
| **Backend API** | http://localhost:9000 | REST API |
| **API Docs** | http://localhost:9000/api/docs | Swagger UI |
| **GraphQL** | http://localhost:9000/graphql | GraphQL Playground |
| **WebSocket** | ws://localhost:9000/ws | Real-time updates |

### Verify Installation

```bash
# 1. Check API status
curl http://localhost:9000/api/status
# Expected: {"status": "Sankalpa API Server is running!", "version": "1.0.0"}

# 2. List available agents
curl http://localhost:9000/api/agents
# Expected: {"agents": [...35+ agents...]}

# 3. Execute a test agent
curl -X POST http://localhost:9000/api/agents/execute \
  -H "Content-Type: application/json" \
  -d '{"agent_name": "hello_world", "input_data": {"name": "Sankalpa"}}'
# Expected: {"result": {"greeting": "Hello, Sankalpa!"}, ...}

# 4. Check frontend
# Open http://localhost:9001 in your browser
```

---

## System Architecture

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                 SANKALPA PLATFORM                                    │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│  ╔═══════════════════════════════════════════════════════════════════════════════╗  │
│  ║                           CLIENT LAYER                                         ║  │
│  ║  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          ║  │
│  ║  │  Web App    │  │  VS Code    │  │    CLI      │  │  Mobile     │          ║  │
│  ║  │  (Next.js)  │  │  Extension  │  │   Client    │  │   PWA       │          ║  │
│  ║  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘          ║  │
│  ╚═════════│════════════════│════════════════│════════════════│══════════════════╝  │
│            │                │                │                │                      │
│            └────────────────┴────────────────┴────────────────┘                      │
│                                      │                                               │
│                                      ▼                                               │
│  ╔═══════════════════════════════════════════════════════════════════════════════╗  │
│  ║                           API GATEWAY LAYER                                    ║  │
│  ║  ┌─────────────────────────────────────────────────────────────────────────┐  ║  │
│  ║  │                      FastAPI Application                                 │  ║  │
│  ║  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐      │  ║  │
│  ║  │  │   JWT    │ │   CORS   │ │   Rate   │ │ Security │ │  Metrics │      │  ║  │
│  ║  │  │   Auth   │ │  Filter  │ │  Limiter │ │ Headers  │ │Middleware│      │  ║  │
│  ║  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘      │  ║  │
│  ║  │                                                                          │  ║  │
│  ║  │  ┌────────────────────────────────────────────────────────────────────┐ │  ║  │
│  ║  │  │ ENDPOINTS:                                                          │ │  ║  │
│  ║  │  │ /api/agents  /api/chains  /api/memory  /api/users  /api/plugins    │ │  ║  │
│  ║  │  │ /api/finetuning  /api/sso  /api/marketplace  /graphql  /ws        │ │  ║  │
│  ║  │  └────────────────────────────────────────────────────────────────────┘ │  ║  │
│  ║  └─────────────────────────────────────────────────────────────────────────┘  ║  │
│  ╚═══════════════════════════════════════════════════════════════════════════════╝  │
│                                      │                                               │
│                                      ▼                                               │
│  ╔═══════════════════════════════════════════════════════════════════════════════╗  │
│  ║                         CORE SERVICES LAYER                                    ║  │
│  ║  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐         ║  │
│  ║  │   Config     │ │   Security   │ │   Caching    │ │  Monitoring  │         ║  │
│  ║  │   Manager    │ │   Service    │ │   Service    │ │   Service    │         ║  │
│  ║  │              │ │              │ │              │ │              │         ║  │
│  ║  │ - YAML/ENV   │ │ - JWT/RBAC   │ │ - Redis      │ │ - Metrics    │         ║  │
│  ║  │ - Hierarchy  │ │ - SSO        │ │ - In-Memory  │ │ - Health     │         ║  │
│  ║  │ - Hot Reload │ │ - Rate Limit │ │ - TTL        │ │ - Logs       │         ║  │
│  ║  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘         ║  │
│  ╚═══════════════════════════════════════════════════════════════════════════════╝  │
│                                      │                                               │
│                                      ▼                                               │
│  ╔═══════════════════════════════════════════════════════════════════════════════╗  │
│  ║                           AGENT LAYER (35+ Agents)                             ║  │
│  ║  ┌─────────────────────────────────────────────────────────────────────────┐  ║  │
│  ║  │                        AGENT CATEGORIES                                  │  ║  │
│  ║  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐           │  ║  │
│  ║  │  │ Builder │ │ Testing │ │ Deploy  │ │Marketing│ │Enhanced │           │  ║  │
│  ║  │  │   (11)  │ │   (4)   │ │   (3)   │ │   (4)   │ │   (6)   │           │  ║  │
│  ║  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘           │  ║  │
│  ║  │  ┌─────────┐ ┌─────────┐ ┌─────────┐                                    │  ║  │
│  ║  │  │  Meta   │ │  Orch   │ │ Custom  │                                    │  ║  │
│  ║  │  │   (2)   │ │   (3)   │ │   (5+)  │                                    │  ║  │
│  ║  │  └─────────┘ └─────────┘ └─────────┘                                    │  ║  │
│  ║  └─────────────────────────────────────────────────────────────────────────┘  ║  │
│  ║                                                                                ║  │
│  ║  ┌─────────────────────────────────────────────────────────────────────────┐  ║  │
│  ║  │                     ORCHESTRATION COMPONENTS                             │  ║  │
│  ║  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐       │  ║  │
│  ║  │  │   Agent Loader   │  │   Chain Manager  │  │  Memory Manager  │       │  ║  │
│  ║  │  │  (Dynamic Load)  │  │ (Seq/Par/Cond)   │  │   (Sessions)     │       │  ║  │
│  ║  │  └──────────────────┘  └──────────────────┘  └──────────────────┘       │  ║  │
│  ║  └─────────────────────────────────────────────────────────────────────────┘  ║  │
│  ╚═══════════════════════════════════════════════════════════════════════════════╝  │
│                                      │                                               │
│                                      ▼                                               │
│  ╔═══════════════════════════════════════════════════════════════════════════════╗  │
│  ║                            DATA LAYER                                          ║  │
│  ║  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐            ║  │
│  ║  │    PostgreSQL    │  │      Redis       │  │   File System    │            ║  │
│  ║  │                  │  │                  │  │                  │            ║  │
│  ║  │  - Users         │  │  - Sessions      │  │  - Agent Files   │            ║  │
│  ║  │  - Chains        │  │  - Cache         │  │  - Memory JSON   │            ║  │
│  ║  │  - Executions    │  │  - Pub/Sub       │  │  - Plugins       │            ║  │
│  ║  │  - Marketplace   │  │  - Rate Limits   │  │  - Workflows     │            ║  │
│  ║  └──────────────────┘  └──────────────────┘  └──────────────────┘            ║  │
│  ╚═══════════════════════════════════════════════════════════════════════════════╝  │
│                                      │                                               │
│                                      ▼                                               │
│  ╔═══════════════════════════════════════════════════════════════════════════════╗  │
│  ║                         EXTERNAL INTEGRATIONS                                  ║  │
│  ║  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐    ║  │
│  ║  │ OpenAI  │ │ GitHub  │ │ Stripe  │ │SendGrid │ │ Vercel  │ │ AWS/GCP │    ║  │
│  ║  │   API   │ │   API   │ │   API   │ │   API   │ │   CLI   │ │  SDKs   │    ║  │
│  ║  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘    ║  │
│  ╚═══════════════════════════════════════════════════════════════════════════════╝  │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

### Component Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                            COMPONENT INTERACTION MAP                                 │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│   FRONTEND (Next.js 14)                    BACKEND (FastAPI)                        │
│   ══════════════════════                   ═════════════════                        │
│                                                                                      │
│   ┌─────────────────────┐                  ┌─────────────────────┐                  │
│   │    Pages/Routes     │                  │    API Routers      │                  │
│   │  ┌───────────────┐  │     REST API     │  ┌───────────────┐  │                  │
│   │  │  /composer    │──┼──────────────────┼─▶│  /api/chains  │  │                  │
│   │  │  /playground  │──┼──────────────────┼─▶│  /api/agents  │  │                  │
│   │  │  /dashboard   │──┼──────────────────┼─▶│  /api/memory  │  │                  │
│   │  │  /marketplace │──┼──────────────────┼─▶│/api/marketplace│ │                  │
│   │  │  /finetuning  │──┼──────────────────┼─▶│/api/finetuning│  │                  │
│   │  └───────────────┘  │                  │  └───────────────┘  │                  │
│   └─────────────────────┘                  └──────────┬──────────┘                  │
│                                                       │                              │
│   ┌─────────────────────┐                            │                              │
│   │    React Flow       │                            ▼                              │
│   │  (Visual Composer)  │                  ┌─────────────────────┐                  │
│   │  ┌───────────────┐  │                  │    Agent Layer      │                  │
│   │  │ Agent Nodes   │  │                  │  ┌───────────────┐  │                  │
│   │  │ Edge Connect  │  │     GraphQL      │  │ Agent Loader  │  │                  │
│   │  │ Flow Control  │──┼──────────────────┼─▶│ Chain Manager │  │                  │
│   │  └───────────────┘  │                  │  │ Base Agent    │  │                  │
│   └─────────────────────┘                  │  └───────────────┘  │                  │
│                                            └──────────┬──────────┘                  │
│   ┌─────────────────────┐                            │                              │
│   │   Apollo Client     │                            ▼                              │
│   │   (GraphQL)         │                  ┌─────────────────────┐                  │
│   │  ┌───────────────┐  │    WebSocket     │   Core Services     │                  │
│   │  │ Queries       │  │                  │  ┌───────────────┐  │                  │
│   │  │ Mutations     │──┼──────────────────┼─▶│ LLM Client    │  │                  │
│   │  │ Subscriptions │  │                  │  │ Memory Mgr    │  │                  │
│   │  └───────────────┘  │                  │  │ Security      │  │                  │
│   └─────────────────────┘                  │  └───────────────┘  │                  │
│                                            └──────────┬──────────┘                  │
│   ┌─────────────────────┐                            │                              │
│   │   State Management  │                            ▼                              │
│   │  ┌───────────────┐  │                  ┌─────────────────────┐                  │
│   │  │ React Context │  │                  │   External APIs     │                  │
│   │  │ Local Storage │  │                  │  ┌───────────────┐  │                  │
│   │  │ Session Cache │  │                  │  │ OpenAI API    │  │                  │
│   │  └───────────────┘  │                  │  │ GitHub API    │  │                  │
│   └─────────────────────┘                  │  │ Cloud SDKs    │  │                  │
│                                            │  └───────────────┘  │                  │
│                                            └─────────────────────┘                  │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagrams

### Request Lifecycle

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              REQUEST LIFECYCLE FLOW                                  │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│   CLIENT REQUEST                                                                     │
│        │                                                                             │
│        ▼                                                                             │
│   ┌─────────────────┐                                                               │
│   │  1. CORS Check  │ ──▶ Verify origin against allowed_origins                     │
│   └────────┬────────┘                                                               │
│            │ ✓                                                                       │
│            ▼                                                                         │
│   ┌─────────────────┐                                                               │
│   │ 2. Rate Limiter │ ──▶ Check requests/minute per IP (default: 60/min)            │
│   └────────┬────────┘                                                               │
│            │ ✓                                                                       │
│            ▼                                                                         │
│   ┌─────────────────┐                                                               │
│   │ 3. Security     │ ──▶ Add security headers (X-Content-Type, CSP, etc.)          │
│   │    Headers      │                                                               │
│   └────────┬────────┘                                                               │
│            │                                                                         │
│            ▼                                                                         │
│   ┌─────────────────┐     ┌─────────────────┐                                       │
│   │ 4. JWT Auth     │────▶│  Decode Token   │                                       │
│   │    (if needed)  │     │  Verify Expiry  │                                       │
│   └────────┬────────┘     │  Extract User   │                                       │
│            │              └─────────────────┘                                       │
│            ▼                                                                         │
│   ┌─────────────────┐                                                               │
│   │ 5. Request      │ ──▶ Log method, URL, client IP, request_id                    │
│   │    Logging      │                                                               │
│   └────────┬────────┘                                                               │
│            │                                                                         │
│            ▼                                                                         │
│   ┌─────────────────┐                                                               │
│   │ 6. Router       │ ──▶ Match route → Execute handler                             │
│   │    Dispatch     │                                                               │
│   └────────┬────────┘                                                               │
│            │                                                                         │
│            ▼                                                                         │
│   ┌─────────────────┐                                                               │
│   │ 7. Business     │ ──▶ Agent execution / Chain execution / Memory ops            │
│   │    Logic        │                                                               │
│   └────────┬────────┘                                                               │
│            │                                                                         │
│            ▼                                                                         │
│   ┌─────────────────┐                                                               │
│   │ 8. Response     │ ──▶ Add X-Process-Time, X-Request-ID headers                  │
│   │    Processing   │                                                               │
│   └────────┬────────┘                                                               │
│            │                                                                         │
│            ▼                                                                         │
│   ┌─────────────────┐                                                               │
│   │ 9. Metrics      │ ──▶ Record request count, response time, status               │
│   │    Collection   │                                                               │
│   └────────┬────────┘                                                               │
│            │                                                                         │
│            ▼                                                                         │
│       JSON RESPONSE                                                                  │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

### Agent Execution Pipeline

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           AGENT EXECUTION PIPELINE                                   │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│   POST /api/agents/execute                                                          │
│   {                                                                                  │
│     "agent_name": "frontend_builder",                                               │
│     "input_data": {"app_name": "TaskFlow", "features": [...]}                       │
│   }                                                                                  │
│        │                                                                             │
│        ▼                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────────────┐   │
│   │ 1. AGENT LOADER                                                              │   │
│   │    ┌───────────────────────────────────────────────────────────────────┐    │   │
│   │    │  agent_name = "frontend_builder"                                   │    │   │
│   │    │                      │                                             │    │   │
│   │    │                      ▼                                             │    │   │
│   │    │  ┌─────────────────────────────────────────────────────────────┐  │    │   │
│   │    │  │ catalog/agent_catalog.json                                   │  │    │   │
│   │    │  │ {                                                            │  │    │   │
│   │    │  │   "frontend_builder": {                                      │  │    │   │
│   │    │  │     "module": "agents.builder.frontend_builder_agent",       │  │    │   │
│   │    │  │     "class": "FrontendBuilderAgent"                          │  │    │   │
│   │    │  │   }                                                          │  │    │   │
│   │    │  │ }                                                            │  │    │   │
│   │    │  └─────────────────────────────────────────────────────────────┘  │    │   │
│   │    │                      │                                             │    │   │
│   │    │                      ▼                                             │    │   │
│   │    │  importlib.import_module() → Get class → Instantiate              │    │   │
│   │    └───────────────────────────────────────────────────────────────────┘    │   │
│   └──────────────────────────────────────────────────────────────────────┬──────┘   │
│                                                                          │          │
│                                                                          ▼          │
│   ┌─────────────────────────────────────────────────────────────────────────────┐   │
│   │ 2. AGENT INITIALIZATION                                                     │   │
│   │    ┌───────────────────────────────────────────────────────────────────┐    │   │
│   │    │  agent = FrontendBuilderAgent(name="frontend_builder")             │    │   │
│   │    │                                                                    │    │   │
│   │    │  Inherits from BaseAgent:                                          │    │   │
│   │    │  - self.name = "frontend_builder"                                  │    │   │
│   │    │  - self.category = "builder"                                       │    │   │
│   │    │  - self.context = None                                             │    │   │
│   │    │  - self._llm_client = None (lazy loaded)                           │    │   │
│   │    └───────────────────────────────────────────────────────────────────┘    │   │
│   └──────────────────────────────────────────────────────────────────────┬──────┘   │
│                                                                          │          │
│                                                                          ▼          │
│   ┌─────────────────────────────────────────────────────────────────────────────┐   │
│   │ 3. CONTEXT INJECTION (if part of chain)                                     │   │
│   │    ┌───────────────────────────────────────────────────────────────────┐    │   │
│   │    │  if accumulated_context:                                           │    │   │
│   │    │      agent.set_context(accumulated_context)                        │    │   │
│   │    │                                                                    │    │   │
│   │    │  Context includes:                                                 │    │   │
│   │    │  - Previous agent outputs                                          │    │   │
│   │    │  - Generated files (models, routes)                                │    │   │
│   │    │  - Shared state (endpoints, pages)                                 │    │   │
│   │    └───────────────────────────────────────────────────────────────────┘    │   │
│   └──────────────────────────────────────────────────────────────────────┬──────┘   │
│                                                                          │          │
│                                                                          ▼          │
│   ┌─────────────────────────────────────────────────────────────────────────────┐   │
│   │ 4. AGENT EXECUTION                                                          │   │
│   │    ┌───────────────────────────────────────────────────────────────────┐    │   │
│   │    │  result = agent.run(input_data)                                    │    │   │
│   │    │                                                                    │    │   │
│   │    │  Inside run():                                                     │    │   │
│   │    │  ┌─────────────────────────────────────────────────────────────┐  │    │   │
│   │    │  │ 1. Build prompt with app_name and features                  │  │    │   │
│   │    │  │ 2. Add context from previous agents (if any)                │  │    │   │
│   │    │  │ 3. Call self.generate_files_with_llm(prompt, file_types)    │  │    │   │
│   │    │  │ 4. LLM generates code for each file                         │  │    │   │
│   │    │  │ 5. Return {"message": "...", "files": {...}}                │  │    │   │
│   │    │  └─────────────────────────────────────────────────────────────┘  │    │   │
│   │    └───────────────────────────────────────────────────────────────────┘    │   │
│   └──────────────────────────────────────────────────────────────────────┬──────┘   │
│                                                                          │          │
│                                                                          ▼          │
│   ┌─────────────────────────────────────────────────────────────────────────────┐   │
│   │ 5. LLM INTEGRATION (if enabled)                                             │   │
│   │    ┌───────────────────────────────────────────────────────────────────┐    │   │
│   │    │  core/llm_client.py:                                               │    │   │
│   │    │                                                                    │    │   │
│   │    │  ┌─────────────────────────────────────────────────────────────┐  │    │   │
│   │    │  │  OpenAI API Call:                                            │  │    │   │
│   │    │  │  - Model: gpt-4o-mini                                        │  │    │   │
│   │    │  │  - System Prompt: Agent's SYSTEM_PROMPT                      │  │    │   │
│   │    │  │  - User Prompt: Built from input_data + context              │  │    │   │
│   │    │  │  - Temperature: 0.7                                          │  │    │   │
│   │    │  │  - Max Tokens: 4096                                          │  │    │   │
│   │    │  └─────────────────────────────────────────────────────────────┘  │    │   │
│   │    │                                                                    │    │   │
│   │    │  Returns: Generated code as string                                 │    │   │
│   │    └───────────────────────────────────────────────────────────────────┘    │   │
│   └──────────────────────────────────────────────────────────────────────┬──────┘   │
│                                                                          │          │
│                                                                          ▼          │
│   ┌─────────────────────────────────────────────────────────────────────────────┐   │
│   │ 6. RESULT PACKAGING                                                         │   │
│   │    ┌───────────────────────────────────────────────────────────────────┐    │   │
│   │    │  {                                                                 │    │   │
│   │    │    "agent_name": "frontend_builder",                               │    │   │
│   │    │    "execution_id": "exec_abc123",                                  │    │   │
│   │    │    "result": {                                                     │    │   │
│   │    │      "message": "Frontend generated for TaskFlow",                 │    │   │
│   │    │      "files": {                                                    │    │   │
│   │    │        "pages/index.tsx": "...",                                   │    │   │
│   │    │        "components/Layout.tsx": "..."                              │    │   │
│   │    │      }                                                             │    │   │
│   │    │    },                                                              │    │   │
│   │    │    "execution_time": 23.45,                                        │    │   │
│   │    │    "success": true                                                 │    │   │
│   │    │  }                                                                 │    │   │
│   │    └───────────────────────────────────────────────────────────────────┘    │   │
│   └─────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

### Chain Execution Flow

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                            CHAIN EXECUTION FLOW                                      │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│   POST /api/chains/execute                                                          │
│   {                                                                                  │
│     "chain_name": "full_stack_builder",                                             │
│     "agents": ["project_architect", "db_schema", "backend_builder",                 │
│                "frontend_builder", "test_suite"],                                   │
│     "input_data": {"app_name": "TaskFlow"}                                          │
│   }                                                                                  │
│                                                                                      │
│        │                                                                             │
│        ▼                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────────────┐   │
│   │                         CHAIN MANAGER                                        │   │
│   │                                                                              │   │
│   │   accumulated_context = {                                                    │   │
│   │     "agent_outputs": {},                                                     │   │
│   │     "files": {},                                                             │   │
│   │     "models": [],                                                            │   │
│   │     "routes": [],                                                            │   │
│   │     "pages": [],                                                             │   │
│   │     "endpoints": []                                                          │   │
│   │   }                                                                          │   │
│   └──────────────────────────────────────────────────────────────────────┬──────┘   │
│                                                                          │          │
│   ┌──────────────────────────────────────────────────────────────────────┴──────┐   │
│   │                                                                              │   │
│   │  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐                  │   │
│   │  │  Agent 1    │      │  Agent 2    │      │  Agent 3    │                  │   │
│   │  │  project_   │ ───▶ │  db_schema  │ ───▶ │  backend_   │ ───▶ ...        │   │
│   │  │  architect  │      │             │      │  builder    │                  │   │
│   │  └──────┬──────┘      └──────┬──────┘      └──────┬──────┘                  │   │
│   │         │                    │                    │                          │   │
│   │         ▼                    ▼                    ▼                          │   │
│   │  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐                  │   │
│   │  │ Output:     │      │ Output:     │      │ Output:     │                  │   │
│   │  │ - structure │      │ - models    │      │ - routes    │                  │   │
│   │  │ - configs   │      │ - schemas   │      │ - endpoints │                  │   │
│   │  │ - Dockerfile│      │ - User      │      │ - services  │                  │   │
│   │  │             │      │ - Project   │      │             │                  │   │
│   │  └──────┬──────┘      └──────┬──────┘      └──────┬──────┘                  │   │
│   │         │                    │                    │                          │   │
│   │         └────────────────────┴────────────────────┘                          │   │
│   │                              │                                                │   │
│   │                              ▼                                                │   │
│   │   ┌─────────────────────────────────────────────────────────────────────┐    │   │
│   │   │                    CONTEXT ACCUMULATION                              │    │   │
│   │   │                                                                      │    │   │
│   │   │  After each agent:                                                   │    │   │
│   │   │                                                                      │    │   │
│   │   │  accumulated_context["agent_outputs"][agent_name] = result           │    │   │
│   │   │                                                                      │    │   │
│   │   │  if "files" in result:                                               │    │   │
│   │   │      accumulated_context["files"].update(result["files"])            │    │   │
│   │   │                                                                      │    │   │
│   │   │  if "models" in result:                                              │    │   │
│   │   │      accumulated_context["models"].extend(result["models"])          │    │   │
│   │   │                                                                      │    │   │
│   │   │  ... routes, pages, endpoints                                        │    │   │
│   │   │                                                                      │    │   │
│   │   │  Next agent receives: agent.set_context(accumulated_context)         │    │   │
│   │   └─────────────────────────────────────────────────────────────────────┘    │   │
│   │                                                                              │   │
│   └──────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                      │
│   FINAL OUTPUT:                                                                      │
│   ┌─────────────────────────────────────────────────────────────────────────────┐   │
│   │  {                                                                           │   │
│   │    "chain_name": "full_stack_builder",                                       │   │
│   │    "status": "completed",                                                    │   │
│   │    "total_execution_time": 384.35,                                           │   │
│   │    "agents_executed": 5,                                                     │   │
│   │    "results": [                                                              │   │
│   │      {"agent": "project_architect", "files": 27, "time": 45.2},              │   │
│   │      {"agent": "db_schema", "files": 16, "time": 32.1},                      │   │
│   │      {"agent": "backend_builder", "files": 10, "time": 28.5},                │   │
│   │      {"agent": "frontend_builder", "files": 15, "time": 35.8},               │   │
│   │      {"agent": "test_suite", "files": 1, "time": 12.3}                       │   │
│   │    ],                                                                        │   │
│   │    "total_files_generated": 69,                                              │   │
│   │    "final_context": { ... }                                                  │   │
│   │  }                                                                           │   │
│   └─────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

### Memory System Flow

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                            MEMORY SYSTEM FLOW                                        │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│   ┌─────────────────────────────────────────────────────────────────────────────┐   │
│   │                         SESSION MANAGEMENT                                   │   │
│   │                                                                              │   │
│   │   Request: { "session_id": "sess_abc123", "key": "user_prefs" }              │   │
│   │                                                                              │   │
│   │                              │                                               │   │
│   │                              ▼                                               │   │
│   │   ┌─────────────────────────────────────────────────────────────────────┐   │   │
│   │   │              MEMORY MANAGER (memory/memory_manager.py)               │   │   │
│   │   │                                                                      │   │   │
│   │   │   Session Directory: memory/sessions/                                │   │   │
│   │   │                                                                      │   │   │
│   │   │   ┌─────────────────────────────────────────────────────────────┐   │   │   │
│   │   │   │  memory/sessions/                                            │   │   │   │
│   │   │   │  ├── sess_abc123/                                            │   │   │   │
│   │   │   │  │   ├── user_prefs.json                                     │   │   │   │
│   │   │   │  │   ├── agent_outputs.json                                  │   │   │   │
│   │   │   │  │   └── workflow_state.json                                 │   │   │   │
│   │   │   │  ├── sess_def456/                                            │   │   │   │
│   │   │   │  │   └── ...                                                 │   │   │   │
│   │   │   │  └── default/                                                │   │   │   │
│   │   │   │      └── ...                                                 │   │   │   │
│   │   │   └─────────────────────────────────────────────────────────────┘   │   │   │
│   │   └─────────────────────────────────────────────────────────────────────┘   │   │
│   │                                                                              │   │
│   │   ┌─────────────────────────────────────────────────────────────────────┐   │   │
│   │   │                      OPERATIONS                                      │   │   │
│   │   │                                                                      │   │   │
│   │   │   SAVE:                                                              │   │   │
│   │   │   ┌─────────────────────────────────────────────────────────────┐   │   │   │
│   │   │   │  1. Validate session_id (create if not exists)              │   │   │   │
│   │   │   │  2. Write to temp file first (atomic)                       │   │   │   │
│   │   │   │  3. Rename temp to final (atomic)                           │   │   │   │
│   │   │   │  4. Return success                                          │   │   │   │
│   │   │   └─────────────────────────────────────────────────────────────┘   │   │   │
│   │   │                                                                      │   │   │
│   │   │   LOAD:                                                              │   │   │
│   │   │   ┌─────────────────────────────────────────────────────────────┐   │   │   │
│   │   │   │  1. Build path: sessions/{session_id}/{key}.json            │   │   │   │
│   │   │   │  2. Read file if exists                                     │   │   │   │
│   │   │   │  3. Parse JSON                                              │   │   │   │
│   │   │   │  4. Return data (or null if not found)                      │   │   │   │
│   │   │   └─────────────────────────────────────────────────────────────┘   │   │   │
│   │   │                                                                      │   │   │
│   │   │   TRANSACTION:                                                       │   │   │
│   │   │   ┌─────────────────────────────────────────────────────────────┐   │   │   │
│   │   │   │  1. Begin transaction (copy current state)                  │   │   │   │
│   │   │   │  2. Perform operations                                      │   │   │   │
│   │   │   │  3. Commit (keep changes) or Rollback (restore state)       │   │   │   │
│   │   │   └─────────────────────────────────────────────────────────────┘   │   │   │
│   │   └─────────────────────────────────────────────────────────────────────┘   │   │
│   │                                                                              │   │
│   │   ┌─────────────────────────────────────────────────────────────────────┐   │   │
│   │   │                     VECTOR MEMORY (v2.0)                             │   │   │
│   │   │                                                                      │   │   │
│   │   │   Providers:                                                         │   │   │
│   │   │   ┌───────────┐  ┌───────────┐  ┌───────────┐                       │   │   │
│   │   │   │ ChromaDB  │  │ Pinecone  │  │ Weaviate  │                       │   │   │
│   │   │   │ (Local)   │  │ (Cloud)   │  │ (Self-   │                       │   │   │
│   │   │   │           │  │           │  │  hosted)  │                       │   │   │
│   │   │   └───────────┘  └───────────┘  └───────────┘                       │   │   │
│   │   │                                                                      │   │   │
│   │   │   Flow:                                                              │   │   │
│   │   │   Text → OpenAI Embeddings → Vector → Store → Semantic Search       │   │   │
│   │   └─────────────────────────────────────────────────────────────────────┘   │   │
│   └─────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

### Directory Structure

```
sankalpa/
├── agents/                          # 35+ AI Agents
│   ├── base.py                      # BaseAgent abstract class with LLM support
│   ├── enhanced_base.py             # Enhanced agent with logging/metrics
│   ├── loader.py                    # Dynamic agent loading from catalog
│   ├── chain_manager.py             # Agent chain orchestration
│   ├── enhanced_chain_manager.py    # Chain manager with retry/callbacks
│   │
│   ├── builder/                     # 11 Builder Agents
│   │   ├── project_architect_agent.py
│   │   ├── frontend_builder_agent.py
│   │   ├── backend_builder_agent.py
│   │   ├── api_builder_agent.py
│   │   ├── db_schema_agent.py
│   │   ├── auth_builder_agent.py
│   │   ├── ui_generator_agent.py
│   │   ├── markdown_editor_agent.py
│   │   ├── email_system_agent.py
│   │   ├── stripe_payment_agent.py
│   │   └── role_auth_agent.py
│   │
│   ├── testing/                     # 4 Testing Agents
│   │   ├── test_suite_agent.py
│   │   ├── integration_test_agent.py
│   │   ├── security_scanner_agent.py
│   │   └── critic_agent.py
│   │
│   ├── deployment/                  # 3 Deployment Agents
│   │   ├── deploy_executor_agent.py
│   │   ├── ci_generator_agent.py
│   │   └── domain_linker_agent.py
│   │
│   ├── marketing/                   # 4 Marketing Agents
│   │   ├── readme_writer_agent.py
│   │   ├── seo_optimizer_agent.py
│   │   ├── product_hunt_copywriter_agent.py
│   │   └── pitch_deck_generator_agent.py
│   │
│   ├── enhanced/                    # 6 Enhanced Agents
│   │   ├── copilot_agent.py
│   │   ├── self_replicator_agent.py
│   │   ├── finetuner_agent.py
│   │   ├── plugin_loader_agent.py
│   │   ├── vs_code_extension_agent.py
│   │   └── cli_runner_agent.py
│   │
│   ├── meta/                        # 2 Meta Agents
│   │   ├── multi_agent_memory_manager.py
│   │   └── version_tracker_agent.py
│   │
│   ├── orchestration/               # 3 Orchestration Agents
│   │   ├── planner_agent.py
│   │   ├── execution_manager_agent.py
│   │   └── session_replayer_agent.py
│   │
│   └── custom/                      # 5+ Custom Agents
│       ├── hello_world_agent.py
│       ├── custom_calculator_agent.py
│       └── ...
│
├── backend/                         # FastAPI Backend
│   ├── simple_main.py               # Basic API server
│   ├── enhanced_main.py             # Full-featured server
│   │
│   ├── routers/                     # API Endpoints
│   │   ├── agents.py                # /api/agents
│   │   ├── chains.py                # /api/chains
│   │   ├── memory.py                # /api/memory
│   │   ├── users.py                 # /api/users
│   │   ├── finetuning.py            # /api/finetuning
│   │   ├── sso.py                   # /api/sso
│   │   ├── plugins.py               # /api/plugins
│   │   └── marketplace.py           # /api/marketplace
│   │
│   ├── graphql/                     # GraphQL API
│   │   ├── schema.py
│   │   ├── types/
│   │   ├── resolvers/
│   │   └── subscriptions.py
│   │
│   ├── db/                          # Database Layer
│   │   ├── database.py
│   │   └── models.py
│   │
│   ├── websockets/                  # Real-time Communication
│   │   ├── connection_manager.py
│   │   ├── redis_pubsub.py
│   │   ├── handlers.py
│   │   └── routes.py
│   │
│   └── middleware/                  # Middleware
│       └── metrics.py
│
├── core/                            # Core Services
│   ├── config.py                    # Configuration management
│   ├── security.py                  # JWT, RBAC, rate limiting
│   ├── caching.py                   # Redis/in-memory caching
│   ├── monitoring.py                # Metrics and health checks
│   ├── logging.py                   # Structured logging
│   ├── llm_client.py                # OpenAI LLM integration
│   │
│   └── sso/                         # Enterprise SSO
│       ├── base.py
│       ├── oidc.py
│       ├── saml.py
│       └── providers/
│           ├── azure_ad.py
│           ├── okta.py
│           └── google.py
│
├── memory/                          # Memory Management
│   ├── memory_manager.py            # Session-based memory
│   ├── enhanced_memory_manager.py   # Enhanced with transactions
│   │
│   ├── sessions/                    # Session storage (JSON files)
│   │
│   └── vector/                      # Vector Memory (v2.0)
│       ├── embeddings.py            # OpenAI embeddings
│       ├── chromadb_store.py
│       ├── pinecone_store.py
│       └── weaviate_store.py
│
├── plugins/                         # Plugin System
│   ├── base.py                      # Plugin base class
│   ├── registry.py                  # Plugin registry
│   ├── hooks.py                     # 50+ hook points
│   └── examples/                    # Example plugins
│
├── finetuning/                      # LLM Fine-tuning
│   ├── models.py                    # Fine-tuning job models
│   ├── service.py                   # OpenAI integration
│   └── schemas.py                   # API schemas
│
├── frontend/                        # Next.js Web Application
│   ├── pages/                       # App Pages
│   │   ├── index.tsx                # Homepage
│   │   ├── composer.tsx             # Visual workflow composer
│   │   ├── playground.tsx           # Agent testing
│   │   ├── dashboard/               # System dashboard
│   │   ├── marketplace/             # Agent marketplace
│   │   ├── finetuning/              # Fine-tuning UI
│   │   ├── auth/                    # SSO login pages
│   │   └── offline.tsx              # PWA offline page
│   │
│   ├── components/                  # React Components
│   │   ├── agents/
│   │   ├── chat/
│   │   ├── collaboration/
│   │   ├── dashboard/
│   │   ├── finetuning/
│   │   ├── layout/
│   │   ├── marketplace/
│   │   ├── memory/
│   │   ├── mobile/
│   │   └── providers/
│   │
│   ├── hooks/                       # React Hooks
│   │   └── usePWA.ts
│   │
│   ├── lib/                         # Utilities
│   │   ├── api-client.ts
│   │   ├── graphql-client.ts
│   │   └── pwa/
│   │
│   ├── styles/                      # CSS/Tailwind
│   │
│   └── public/                      # Static Assets
│       ├── manifest.json            # PWA manifest
│       └── sw.js                    # Service worker
│
├── marketplace/                     # Agent Marketplace
│   ├── routes.py                    # Marketplace API
│   ├── models.py                    # Marketplace models
│   ├── installation.py              # Install/uninstall
│   └── publishing.py                # Publishing workflow
│
├── vscode-extension/                # VS Code Extension
│   ├── src/
│   │   ├── extension.ts             # Entry point
│   │   ├── providers/               # Tree data providers
│   │   ├── commands/                # VS Code commands
│   │   ├── services/                # API client
│   │   └── webviews/                # Custom panels
│   └── package.json
│
├── deploy/                          # Deployment
│   └── helm/                        # Kubernetes Helm charts
│       └── sankalpa/
│           ├── Chart.yaml
│           ├── values.yaml
│           ├── values-aws.yaml
│           ├── values-gcp.yaml
│           ├── values-azure.yaml
│           └── templates/
│
├── tenants/                         # Multi-tenancy
├── integrations/                    # External integrations
├── nlp/                             # NLP utilities
├── cli/                             # Command-line interface
├── catalog/                         # Agent catalog (JSON)
│   └── agent_catalog.json
│
├── tests/                           # Test Suites
│   ├── unit/
│   ├── integration/
│   ├── e2e/
│   ├── security/
│   └── performance/
│
├── docs/                            # Documentation
│   ├── API.md
│   ├── system_architecture.md
│   ├── deployment-guide.md
│   └── production-deployment.md
│
├── docker-compose.yml               # Container orchestration
├── Dockerfile                       # Backend container
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment template
└── run_sankalpa.py                  # Full system launcher
```

---

## Agent Ecosystem

### Agent Categories Overview

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           SANKALPA AGENT ECOSYSTEM                                   │
│                                  35+ AGENTS                                          │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│  ┌─────────────────────────────────────────────────────────────────────────────┐    │
│  │                         BUILDER AGENTS (11)                                  │    │
│  │  Generate complete application code from specifications                      │    │
│  │                                                                              │    │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐       │    │
│  │  │  project_    │ │  frontend_   │ │  backend_    │ │  api_        │       │    │
│  │  │  architect   │ │  builder     │ │  builder     │ │  builder     │       │    │
│  │  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘       │    │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐       │    │
│  │  │  db_schema   │ │  auth_       │ │  ui_         │ │  markdown_   │       │    │
│  │  │              │ │  builder     │ │  generator   │ │  editor      │       │    │
│  │  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘       │    │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐                        │    │
│  │  │  email_      │ │  stripe_     │ │  role_       │                        │    │
│  │  │  system      │ │  payment     │ │  auth        │                        │    │
│  │  └──────────────┘ └──────────────┘ └──────────────┘                        │    │
│  └─────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                      │
│  ┌─────────────────────────────────────────────────────────────────────────────┐    │
│  │                         TESTING AGENTS (4)                                   │    │
│  │  Create tests and perform code quality analysis                              │    │
│  │                                                                              │    │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐       │    │
│  │  │  test_suite  │ │ integration_ │ │  security_   │ │  critic      │       │    │
│  │  │              │ │  test        │ │  scanner     │ │              │       │    │
│  │  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘       │    │
│  └─────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                      │
│  ┌─────────────────────────────────────────────────────────────────────────────┐    │
│  │                       DEPLOYMENT AGENTS (3)                                  │    │
│  │  Handle CI/CD and cloud deployment                                          │    │
│  │                                                                              │    │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐                        │    │
│  │  │  deploy_     │ │  ci_         │ │  domain_     │                        │    │
│  │  │  executor    │ │  generator   │ │  linker      │                        │    │
│  │  └──────────────┘ └──────────────┘ └──────────────┘                        │    │
│  └─────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                      │
│  ┌─────────────────────────────────────────────────────────────────────────────┐    │
│  │                        MARKETING AGENTS (4)                                  │    │
│  │  Generate documentation and marketing materials                              │    │
│  │                                                                              │    │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐       │    │
│  │  │  readme_     │ │  seo_        │ │product_hunt_ │ │  pitch_deck_ │       │    │
│  │  │  writer      │ │  optimizer   │ │  copywriter  │ │  generator   │       │    │
│  │  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘       │    │
│  └─────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                      │
│  ┌─────────────────────────────────────────────────────────────────────────────┐    │
│  │                        ENHANCED AGENTS (6)                                   │    │
│  │  Advanced capabilities including self-replication                            │    │
│  │                                                                              │    │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐       │    │
│  │  │  copilot     │ │  self_       │ │  finetuner   │ │  plugin_     │       │    │
│  │  │              │ │  replicator  │ │              │ │  loader      │       │    │
│  │  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘       │    │
│  │  ┌──────────────┐ ┌──────────────┐                                         │    │
│  │  │  vs_code_    │ │  cli_        │                                         │    │
│  │  │  extension   │ │  runner      │                                         │    │
│  │  └──────────────┘ └──────────────┘                                         │    │
│  └─────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                      │
│  ┌────────────────────────────────────┐  ┌────────────────────────────────────┐    │
│  │         META AGENTS (2)            │  │     ORCHESTRATION AGENTS (3)       │    │
│  │  Cross-agent coordination          │  │  Workflow planning and execution   │    │
│  │                                    │  │                                    │    │
│  │  ┌──────────────┐ ┌──────────────┐│  │  ┌──────────────┐ ┌──────────────┐│    │
│  │  │multi_agent_  │ │  version_    ││  │  │  planner_    │ │  execution_  ││    │
│  │  │memory_manager│ │  tracker     ││  │  │  agent       │ │  manager     ││    │
│  │  └──────────────┘ └──────────────┘│  │  └──────────────┘ └──────────────┘│    │
│  │                                    │  │  ┌──────────────┐                 │    │
│  │                                    │  │  │  session_    │                 │    │
│  │                                    │  │  │  replayer    │                 │    │
│  │                                    │  │  └──────────────┘                 │    │
│  └────────────────────────────────────┘  └────────────────────────────────────┘    │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

### Builder Agents (11)

| Agent | Description | Key Inputs | Key Outputs |
|-------|-------------|------------|-------------|
| `project_architect` | Creates project structure and architecture | `app_name`, `type`, `features` | Folder structure, Docker, CI/CD, configs |
| `frontend_builder` | Generates Next.js/React UI | `app_name`, `pages`, `components` | Pages, components, styles, hooks |
| `backend_builder` | Creates FastAPI backend scaffold | `app_name`, `endpoints`, `features` | Routes, models, services, middleware |
| `api_builder` | Generates REST API endpoints | `resource`, `fields`, `operations` | OpenAPI spec, handlers, validators |
| `db_schema` | Designs database schemas | `app_name`, `entities`, `relationships` | SQLAlchemy models, Pydantic schemas, migrations |
| `auth_builder` | JWT authentication system | `auth_type`, `features` | Login, signup, password reset, JWT handling |
| `ui_generator` | UI layout with Tailwind | `components`, `theme` | Buttons, forms, cards, modals, tables |
| `markdown_editor` | Markdown editor with preview | `features` | Editor component, preview, syntax highlighting |
| `email_system` | SMTP email integration | `provider`, `templates` | Email templates, sender service |
| `stripe_payment` | Payment system integration | `products`, `plans` | Checkout, webhooks, subscription handling |
| `role_auth` | Role-based access control | `roles`, `permissions` | RBAC middleware, permission decorators |

<details>
<summary><b>Builder Agent Details</b></summary>

#### project_architect

**Purpose**: Creates the foundational project structure and architecture plan.

**System Prompt**:
```
You are an expert software architect. Create comprehensive project structures
with proper organization, configuration files, and deployment setup.
```

**Input Schema**:
```json
{
  "app_name": "TaskFlow",
  "type": "web",
  "features": ["auth", "dashboard", "api"],
  "tech_stack": {
    "frontend": "nextjs",
    "backend": "fastapi",
    "database": "postgresql"
  }
}
```

**Output**:
```json
{
  "message": "Project architecture created for TaskFlow",
  "files": {
    "docker-compose.yml": "...",
    "Dockerfile": "...",
    ".github/workflows/ci.yml": "...",
    "package.json": "...",
    "requirements.txt": "..."
  },
  "structure": ["src/", "components/", "api/", "models/"]
}
```

#### frontend_builder

**Purpose**: Generates complete Next.js frontend with pages and components.

**System Prompt**:
```
You are an expert frontend developer specializing in Next.js 14, React,
TypeScript, and TailwindCSS. Generate production-ready frontend code.
```

**Output Files**:
- `pages/index.tsx` - Homepage
- `pages/_app.tsx` - App wrapper
- `components/Layout.tsx` - Layout component
- `components/Header.tsx` - Navigation header
- `styles/globals.css` - Global styles

</details>

### Testing Agents (4)

| Agent | Description | Key Inputs | Key Outputs |
|-------|-------------|------------|-------------|
| `test_suite` | Unit test generation | `code`, `framework` | pytest/jest tests |
| `integration_test` | Integration test creation | `endpoints`, `scenarios` | API tests, database tests |
| `security_scanner` | Security vulnerability scanning | `code`, `type` | Vulnerability report |
| `critic` | Code quality review | `code`, `standards` | Code review, suggestions |

### Deployment Agents (3)

| Agent | Description | Key Inputs | Key Outputs |
|-------|-------------|------------|-------------|
| `deploy_executor` | Deploy to cloud platforms | `target`, `config` | Deployment scripts, logs |
| `ci_generator` | GitHub Actions workflows | `tests`, `deploy_target` | CI/CD YAML files |
| `domain_linker` | Custom domain configuration | `domain`, `provider` | DNS records, SSL config |

### Marketing Agents (4)

| Agent | Description | Key Inputs | Key Outputs |
|-------|-------------|------------|-------------|
| `readme_writer` | README.md generation | `project`, `features` | Professional README |
| `seo_optimizer` | SEO meta tags and keywords | `content`, `target_audience` | Meta tags, sitemap, structured data |
| `product_hunt_copywriter` | Launch copy for Product Hunt | `product`, `tagline` | Launch copy, taglines |
| `pitch_deck_generator` | Pitch deck outline | `product`, `market` | 10-slide deck outline |

### Enhanced Agents (6)

| Agent | Description | Key Inputs | Key Outputs |
|-------|-------------|------------|-------------|
| `copilot` | Interactive AI assistant | `query`, `context` | Suggestions, code snippets |
| `self_replicator` | Creates new agents from prompts | `agent_description` | New agent Python file |
| `finetuner` | LLM fine-tuning automation | `dataset`, `model` | Fine-tuning job config |
| `plugin_loader` | Third-party plugin integration | `plugin_name` | Loaded plugin instance |
| `vs_code_extension` | VS Code extension generation | `features` | Extension source code |
| `cli_runner` | CLI command execution | `commands` | Command output |

<details>
<summary><b>Self-Replicator Agent Details</b></summary>

The `self_replicator` agent is a unique meta-agent that can create new agents from natural language descriptions.

**Example Input**:
```json
{
  "agent_description": "Create an agent that generates GraphQL schemas from database models",
  "agent_name": "graphql_generator",
  "category": "builder"
}
```

**Output**:
```python
# agents/custom/graphql_generator_agent.py
from agents.base import BaseAgent

class GraphQLGeneratorAgent(BaseAgent):
    SYSTEM_PROMPT = """You are an expert at generating GraphQL schemas..."""

    def __init__(self, name="graphql_generator", memory=None):
        super().__init__(name, memory)
        self.category = "builder"
        self.description = "Generates GraphQL schemas from database models"

    def run(self, input_data):
        # Implementation generated by self-replicator
        ...
```

</details>

### Meta Agents (2)

| Agent | Description | Key Inputs | Key Outputs |
|-------|-------------|------------|-------------|
| `multi_agent_memory_manager` | Cross-agent memory coordination | `agents`, `session_id` | Shared memory state |
| `version_tracker` | Version control and tracking | `changes` | Version history |

### Orchestration Agents (4)

| Agent | Description | Key Inputs | Key Outputs |
|-------|-------------|------------|-------------|
| `intelligent_orchestrator` | **NEW** Auto-analyzes tasks & creates optimal chains | `task`, `app_name` | Complete codebase |
| `planner_agent` | Task planning and workflow design | `task`, `constraints` | Step-by-step plan |
| `execution_manager` | Agent execution orchestration | `plan`, `agents` | Execution results |
| `session_replayer` | Session replay and debugging | `session_id` | Replay transcript |

<details>
<summary><b>Intelligent Orchestrator Details (NEW)</b></summary>

The `intelligent_orchestrator` is the recommended way to use Sankalpa. It automatically:
1. Analyzes your task description to detect the type (full_stack, backend_api, frontend_app, etc.)
2. Selects optimal agents based on required capabilities
3. Validates the agent chain for dependency correctness
4. Executes the chain with proper context flow between agents

**Quick Usage:**

```python
from agents.orchestration.intelligent_orchestrator import auto_execute, suggest_for_task

# Option 1: Get suggestions first (for review)
suggestion = suggest_for_task("Build an e-commerce site with payments")
print(suggestion["suggested_agents"])
# ['project_architect', 'db_schema', 'backend_builder', 'auth_builder',
#  'frontend_builder', 'ui_generator', 'test_suite', 'readme_writer']

# Option 2: Auto-analyze and execute
result = auto_execute("Build a REST API with JWT auth", "MyAPI")
# Automatically creates chain, loads agents, executes, returns results
```

**Task Type Detection:**

| Task Keywords | Detected Type | Agents Selected |
|--------------|---------------|-----------------|
| "full stack", "saas", "complete app" | `full_stack` | 8 agents (architect → readme) |
| "api", "backend", "rest", "graphql" | `backend_api` | 6 agents (architect → tests) |
| "frontend", "ui", "landing page" | `frontend_app` | 4 agents (architect → seo) |
| "deploy", "ci/cd", "docker" | `deploy_ready` | 4 agents (architect → deploy) |

**Test Results (All Pass):**

```
============================================================
 INTELLIGENT ORCHESTRATOR TEST RESULTS
============================================================
[PASS] Full Stack SaaS task detected correctly
[PASS] Backend API task detected correctly
[PASS] Frontend App task detected correctly
[PASS] Deploy Ready task detected correctly
[PASS] Chain validation passed for all task types
[PASS] Agent loading and instantiation successful
============================================================
```

</details>

### Custom Agents

Custom agents can be created in the `agents/custom/` directory:

| Agent | Description |
|-------|-------------|
| `hello_world` | Simple test agent for verification |
| `custom_calculator` | Example calculator agent |

### Creating a Custom Agent

1. **Create the agent file**:

```python
# agents/custom/my_agent.py
from agents.base import BaseAgent
from typing import Dict, Any

class MyCustomAgent(BaseAgent):
    """My custom agent description."""

    SYSTEM_PROMPT = """You are an expert at [task description].
    Generate high-quality output based on the provided input."""

    def __init__(self, name="my_custom_agent", memory=None):
        super().__init__(name, memory)
        self.category = "custom"
        self.description = "My custom agent for specific tasks"

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent's main logic."""
        # Get app name from input
        app_name = self.get_app_name(input_data)

        # Build prompt
        prompt = f"""Generate output for "{app_name}"

Requirements:
{input_data.get('requirements', 'No specific requirements')}
"""

        # Add context if available (from chain execution)
        if self.context:
            prompt += f"\n\nContext from previous agents:\n{self.context}"

        # Generate using LLM
        files = self.generate_files_with_llm(
            prompt,
            ["output.json", "config.yaml"]
        )

        return {
            "message": f"Output generated for {app_name}",
            "files": files
        }
```

2. **Register in catalog**:

```json
// catalog/agent_catalog.json
{
  "my_custom_agent": {
    "description": "My custom agent for specific tasks",
    "category": "custom",
    "module": "agents.custom.my_agent",
    "class": "MyCustomAgent"
  }
}
```

3. **Test the agent**:

```bash
curl -X POST http://localhost:9000/api/agents/execute \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "my_custom_agent",
    "input_data": {
      "app_name": "TestApp",
      "requirements": "Generate a test output"
    }
  }'
```

---

## LLM Integration Test Results

### Task: Build "TaskFlow" - A Complete Project Management SaaS

We tested Sankalpa with a complex real-world task to demonstrate its full capabilities with OpenAI GPT-4o-mini integration:

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           TEST CASE: TaskFlow SaaS                                   │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│  Build a complete Project Management SaaS called 'TaskFlow' with:                   │
│                                                                                      │
│  1. USER MANAGEMENT                                                                  │
│     - JWT authentication                                                            │
│     - User profiles with avatars                                                    │
│     - Team management                                                               │
│     - Role-based access control (Admin, Manager, Member)                            │
│                                                                                      │
│  2. PROJECT FEATURES                                                                 │
│     - Project CRUD operations                                                       │
│     - Project dashboard with stats                                                  │
│     - Kanban board view                                                             │
│     - List view with filtering                                                      │
│                                                                                      │
│  3. TASK MANAGEMENT                                                                  │
│     - Task assignments                                                              │
│     - Priority levels (Low, Medium, High, Urgent)                                   │
│     - Due dates and reminders                                                       │
│     - Comments and attachments                                                      │
│                                                                                      │
│  4. COLLABORATION                                                                    │
│     - Real-time updates                                                             │
│     - Activity feed                                                                 │
│     - File sharing                                                                  │
│     - @mentions                                                                     │
│                                                                                      │
│  5. BILLING                                                                          │
│     - Stripe subscription integration                                               │
│     - Free tier (5 projects, 10 users)                                              │
│     - Pro tier ($15/user/month)                                                     │
│     - Enterprise tier (custom pricing)                                              │
│                                                                                      │
│  6. ANALYTICS                                                                        │
│     - Task completion rates                                                         │
│     - Productivity metrics                                                          │
│     - Burndown charts                                                               │
│     - Export reports                                                                │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

### Results: Before vs After LLM Integration

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           PERFORMANCE COMPARISON                                     │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│  ┌─────────────────────────────┐    ┌─────────────────────────────┐                │
│  │    BEFORE (Templates)       │    │    AFTER (OpenAI LLM)       │                │
│  │    ═══════════════════      │    │    ═════════════════════    │                │
│  │                             │    │                             │                │
│  │    Files Generated: 20      │    │    Files Generated: 107     │                │
│  │    Total Time: 22.7s        │    │    Total Time: 384.35s      │                │
│  │    Per Agent: ~2s           │    │    Per Agent: 21-54s        │                │
│  │    Code Quality: Scaffold   │    │    Code Quality: Production │                │
│  │    Input Usage: Ignored     │    │    Input Usage: Used        │                │
│  │    Context: None            │    │    Context: Accumulated     │                │
│  │                             │    │                             │                │
│  └─────────────────────────────┘    └─────────────────────────────┘                │
│                                                                                      │
│  IMPROVEMENT: 5.35x more files generated with production-ready code                 │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

| Metric | Before (Templates) | After (OpenAI LLM) | Improvement |
|--------|-------------------|-------------------|-------------|
| **Files Generated** | 20 | **107** | **5.35x** |
| **Total Time** | 22.7s | 384.35s | Real processing |
| **Agent Execution** | ~2s each | 21-54s each | Actual LLM calls |
| **Code Quality** | Scaffold stubs | Production-ready | Complete code |
| **Input Usage** | Ignored | **"TaskFlow" used** | Context-aware |
| **Context Sharing** | None | **Full accumulation** | Chain memory |

### Files Generated Per Agent

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                        FILES GENERATED BY AGENT                                      │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│  Agent                │ Files │ Time    │ Description                               │
│  ─────────────────────┼───────┼─────────┼──────────────────────────────────────────│
│  project_architect    │  27   │ 54.2s   │ Project structure, Docker, CI/CD         │
│  db_schema            │  16   │ 45.3s   │ SQLAlchemy models + Pydantic schemas     │
│  auth_builder         │   7   │ 32.1s   │ JWT auth, password hashing               │
│  backend_builder      │  10   │ 38.7s   │ FastAPI routes, services                 │
│  api_builder          │   4   │ 21.4s   │ REST endpoints, pagination               │
│  frontend_builder     │  15   │ 42.6s   │ Next.js pages, components, hooks         │
│  ui_generator         │  13   │ 35.8s   │ Button, Card, Modal, Table, Toast        │
│  stripe_payment       │   7   │ 28.9s   │ Checkout, webhooks, pricing UI           │
│  test_suite           │   1   │ 18.2s   │ Pytest configuration                     │
│  readme_writer        │   1   │ 22.5s   │ Professional documentation               │
│  seo_optimizer        │   6   │ 24.6s   │ Meta tags, structured data, sitemap      │
│  ─────────────────────┼───────┼─────────┼──────────────────────────────────────────│
│  TOTAL                │ 107   │ 384.35s │ Complete full-stack application          │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

### Sample Generated Code Quality

**Database Model (User) - SQLAlchemy with relationships:**
```python
class User(BaseModel):
    __tablename__ = 'users'
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    team_id = Column(Integer, ForeignKey('teams.id'))

    team = relationship('Team', back_populates='members')
    projects = relationship('Project', back_populates='owner')
```

**Frontend Homepage (TaskFlow-branded):**
```tsx
<Head>
    <title>TaskFlow - Project Management SaaS</title>
    <meta name="description" content="Manage your projects efficiently with TaskFlow." />
</Head>
<section className="flex flex-col items-center justify-center h-screen bg-gray-100">
    <h1 className="text-4xl font-bold mb-4">Welcome to TaskFlow</h1>
    <p className="text-lg mb-8">Your ultimate project management solution.</p>
    <a href="/auth/login" className="bg-blue-500 text-white px-4 py-2 rounded">Get Started</a>
</section>
```

**JWT Authentication - Production-ready:**
```python
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Token has expired')
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail='Invalid token')
```

### Key Achievements

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           KEY ACHIEVEMENTS                                           │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│  Issue                              │ Before          │ After                       │
│  ───────────────────────────────────┼─────────────────┼────────────────────────────│
│  Hard-coded templates               │ Yes             │ ✅ LLM-generated code      │
│  Input parameters ignored           │ Yes             │ ✅ "TaskFlow" everywhere   │
│  Context sharing between agents     │ None            │ ✅ Full accumulation       │
│  README character-by-character bug  │ Broken          │ ✅ Fixed                   │
│  Invalid file formats (HTML in TSX) │ Common          │ ✅ Valid TSX generated     │
│  Minimal 2-field models             │ Yes             │ ✅ Full relationships      │
│  No indexes on database columns     │ Yes             │ ✅ Indexed columns         │
│  Generic "MyApp" naming             │ Yes             │ ✅ "TaskFlow" branding     │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

### How to Run This Test

```bash
# 1. Set your OpenAI API key in .env
echo "OPENAI_API_KEY=sk-your-key-here" >> .env

# 2. Start the backend server
python -m uvicorn backend.enhanced_main:app --host 0.0.0.0 --port 9000

# 3. Run the complex task test
python test_complex_task.py

# 4. Check generated output
ls -la generated_output/
```

---
<img width="1536" height="1024" alt="20251229_1644_Sankalpa AI Platform_simple_compose_01kdnfxh8jfztveq7h3e1sjet7" src="https://github.com/user-attachments/assets/f4d4d199-ce7b-4275-81cf-e6eaea724517" />
---

## API Reference

### Base URL

```
http://localhost:9000/api
```

### Authentication

All authenticated endpoints require a JWT token in the Authorization header:

```bash
# Login to get token
curl -X POST http://localhost:9000/api/users/login \
  -H "Content-Type: application/json" \
  -d '{"username": "user@example.com", "password": "password"}'

# Response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}

# Use token in subsequent requests
curl -H "Authorization: Bearer <token>" http://localhost:9000/api/me
```

### Agents API

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/agents` | List all agents | No |
| GET | `/api/agents/enhanced` | List enhanced agents | No |
| POST | `/api/agents/execute` | Execute an agent | No |
| GET | `/api/agents/{name}` | Get agent details | No |

```bash
# List all agents
curl http://localhost:9000/api/agents

# Execute an agent
curl -X POST http://localhost:9000/api/agents/execute \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "frontend_builder",
    "input_data": {
      "app_name": "MyApp",
      "features": ["auth", "dashboard"]
    }
  }'
```

### Chains API

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/chains` | List chain templates | No |
| POST | `/api/chains/execute` | Execute a chain | No |
| GET | `/api/chains/{name}` | Get chain details | No |

```bash
# Execute a chain
curl -X POST http://localhost:9000/api/chains/execute \
  -H "Content-Type: application/json" \
  -d '{
    "chain_name": "full_stack_builder",
    "agents": ["project_architect", "db_schema", "backend_builder", "frontend_builder"],
    "input_data": {"app_name": "TaskFlow"},
    "session_id": "sess_123"
  }'
```

### Memory API

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/memory/save` | Save to memory | No |
| POST | `/api/memory/load` | Load from memory | No |
| DELETE | `/api/memory/{session_id}` | Clear session | No |
| POST | `/api/memory/search/vector` | Vector search (v2.0) | Yes |

### GraphQL API (v2.0)

```graphql
# Endpoint: POST /graphql

# Query agents
query {
  agents {
    id
    name
    category
    description
  }
}

# Execute agent
mutation {
  executeAgent(name: "project_architect", input: {appName: "MyApp"}) {
    executionId
    result
    executionTime
  }
}

# Real-time subscription
subscription {
  chainProgress(chainId: "chain_123") {
    step
    agent
    status
    output
  }
}
```

### WebSocket API

```javascript
// Connect to WebSocket
const ws = new WebSocket('ws://localhost:9000/ws');

// Subscribe to chain progress
ws.send(JSON.stringify({
  type: 'subscribe',
  channel: 'chain_progress',
  chain_id: 'chain_123'
}));

// Receive updates
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Progress:', data);
};
```

### SSO API (v2.0)

```bash
# Get SSO login URL
curl "http://localhost:9000/api/sso/login?provider=azure_ad&redirect_uri=http://localhost:9001/auth/callback"

# Handle callback
curl -X POST http://localhost:9000/api/sso/callback \
  -H "Content-Type: application/json" \
  -d '{"code": "auth_code", "state": "state_value"}'
```

### Fine-tuning API (v2.0)

```bash
# List jobs
curl -H "Authorization: Bearer <token>" http://localhost:9000/api/finetuning/jobs

# Create job
curl -X POST http://localhost:9000/api/finetuning/jobs \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-3.5-turbo",
    "dataset_id": "dataset_123",
    "hyperparameters": {"epochs": 3}
  }'

# Get job status
curl -H "Authorization: Bearer <token>" http://localhost:9000/api/finetuning/jobs/job_123
```

For complete API documentation, see [docs/API.md](./docs/API.md).

---

## Visual Workflow Composer

### Features

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│  SANKALPA WORKFLOW COMPOSER                                              [─][□][×]  │
├─────────────────────────────────────────────────────────────────────────────────────┤
│ ┌─────────────┐                                                                      │
│ │ AGENTS      │    ┌──────────┐      ┌──────────┐      ┌──────────┐               │
│ ├─────────────┤    │ Project  │─────▶│ Frontend │─────▶│  Deploy  │               │
│ │ ○ Architect │    │ Architect│      │ Builder  │      │ Executor │               │
│ │ ○ Frontend  │    └──────────┘      └──────────┘      └──────────┘               │
│ │ ○ Backend   │          │                                    │                    │
│ │ ○ Database  │          │           ┌──────────┐             │                    │
│ │ ○ Auth      │          └──────────▶│ Backend  │─────────────┘                    │
│ │ ○ Deploy    │                      │ Builder  │                                  │
│ │ ○ Test      │                      └──────────┘                                  │
│ └─────────────┘                                                                      │
│                                                                                      │
│ [Run Chain]  [Save]  [Export]  [Import]                           Agents: 4        │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

- **Drag-and-drop nodes** - Add agents by dragging from the palette
- **Visual connections** - Connect agents with edges to define flow
- **Real-time execution** - Run chains and see progress live
- **Template workflows** - Load pre-built workflow templates
- **Export/Import** - Save and share workflow JSON files

### Access

```
http://localhost:9001/composer
```

### Workflow JSON Format

```json
{
  "name": "full_stack_builder",
  "description": "Build a complete full-stack application",
  "nodes": [
    {"id": "1", "type": "agent", "position": {"x": 100, "y": 100}, "data": {"agent": "project_architect"}},
    {"id": "2", "type": "agent", "position": {"x": 300, "y": 100}, "data": {"agent": "frontend_builder"}},
    {"id": "3", "type": "agent", "position": {"x": 300, "y": 250}, "data": {"agent": "backend_builder"}}
  ],
  "edges": [
    {"source": "1", "target": "2", "id": "e1-2"},
    {"source": "1", "target": "3", "id": "e1-3"}
  ]
}
```

---

## Security

### Authentication & Authorization

| Feature | Implementation | Details |
|---------|----------------|---------|
| **JWT Tokens** | HS256 algorithm | Configurable expiry (default: 30 min) |
| **Password Hashing** | bcrypt with salt | 12 rounds by default |
| **Role-Based Access** | Admin, User, Guest | Middleware-based enforcement |
| **Rate Limiting** | Per-IP tracking | 60 requests/minute default |
| **CORS Protection** | Configurable origins | Whitelist-based |
| **Enterprise SSO** | SAML 2.0, OIDC | Azure AD, Okta, Google |
| **PKCE Support** | OAuth2 + PKCE | Secure SPA flows |

### Security Headers

```python
# Applied to all responses
{
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Content-Security-Policy": "default-src 'self'",
    "Referrer-Policy": "strict-origin-when-cross-origin"
}
```

### Security Best Practices

1. **Environment Variables**: Never commit `.env` files
2. **JWT Secret**: Use a strong, random secret (32+ characters)
3. **HTTPS**: Always use HTTPS in production
4. **Input Validation**: All inputs validated with Pydantic
5. **SQL Injection**: Parameterized queries via SQLAlchemy
6. **XSS Protection**: React's built-in escaping + CSP headers

### Security Configuration

```bash
# .env security settings
SANKALPA_JWT_SECRET=your-very-long-random-secret-key-at-least-32-chars
SANKALPA_JWT_ALGORITHM=HS256
SANKALPA_JWT_EXPIRE_MINUTES=30
SANKALPA_ALLOWED_ORIGINS=https://yourdomain.com
SANKALPA_RATE_LIMIT=60
```

---

## Configuration

### Environment Variables

```bash
# ═══════════════════════════════════════════════════════════════════
# APPLICATION SETTINGS
# ═══════════════════════════════════════════════════════════════════
SANKALPA_ENV=development              # development | production
SANKALPA_DEBUG=true                   # Enable debug mode
SANKALPA_LOG_LEVEL=INFO               # DEBUG | INFO | WARNING | ERROR

# ═══════════════════════════════════════════════════════════════════
# API SERVER
# ═══════════════════════════════════════════════════════════════════
API_HOST=0.0.0.0                      # Bind address
API_PORT=9000                         # Backend port
FRONTEND_URL=http://localhost:9001    # Frontend URL for CORS

# ═══════════════════════════════════════════════════════════════════
# SECURITY
# ═══════════════════════════════════════════════════════════════════
SANKALPA_JWT_SECRET=your-secret-key   # REQUIRED: JWT signing key
SANKALPA_JWT_ALGORITHM=HS256          # JWT algorithm
SANKALPA_JWT_EXPIRE_MINUTES=30        # Token expiry
SANKALPA_ALLOWED_ORIGINS=http://localhost:9001,http://localhost:3000
SANKALPA_RATE_LIMIT=60                # Requests per minute

# ═══════════════════════════════════════════════════════════════════
# DATABASE (Optional - for production)
# ═══════════════════════════════════════════════════════════════════
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=sankalpa
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# ═══════════════════════════════════════════════════════════════════
# REDIS (Optional - for caching & pub/sub)
# ═══════════════════════════════════════════════════════════════════
REDIS_URL=redis://localhost:6379/0

# ═══════════════════════════════════════════════════════════════════
# LLM INTEGRATION
# ═══════════════════════════════════════════════════════════════════
OPENAI_API_KEY=sk-your-openai-key     # OpenAI API key
OPENAI_MODEL=gpt-4o-mini              # Default model
OPENAI_TEMPERATURE=0.7                # Generation temperature
OPENAI_MAX_TOKENS=4096                # Max tokens per request

# ═══════════════════════════════════════════════════════════════════
# EXTERNAL INTEGRATIONS
# ═══════════════════════════════════════════════════════════════════
GITHUB_TOKEN=ghp_your-token           # GitHub API access
STRIPE_SECRET_KEY=sk_test_xxx         # Stripe payments
STRIPE_WEBHOOK_SECRET=whsec_xxx       # Stripe webhooks
SENDGRID_API_KEY=SG.xxx               # Email sending

# ═══════════════════════════════════════════════════════════════════
# ENTERPRISE SSO (v2.0)
# ═══════════════════════════════════════════════════════════════════
AZURE_AD_CLIENT_ID=xxx                # Azure AD app ID
AZURE_AD_CLIENT_SECRET=xxx            # Azure AD secret
AZURE_AD_TENANT_ID=xxx                # Azure AD tenant
OKTA_CLIENT_ID=xxx                    # Okta app ID
OKTA_CLIENT_SECRET=xxx                # Okta secret
OKTA_DOMAIN=xxx.okta.com              # Okta domain

# ═══════════════════════════════════════════════════════════════════
# VECTOR MEMORY (v2.0)
# ═══════════════════════════════════════════════════════════════════
VECTOR_STORE=chromadb                 # chromadb | pinecone | weaviate
PINECONE_API_KEY=xxx                  # Pinecone API key
PINECONE_ENVIRONMENT=us-west1-gcp     # Pinecone environment
WEAVIATE_URL=http://localhost:8080    # Weaviate URL
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

# Rebuild images
docker-compose build --no-cache
```

**docker-compose.yml overview:**
```yaml
services:
  backend:
    build: .
    ports:
      - "9000:9000"
    environment:
      - SANKALPA_ENV=production
    depends_on:
      - postgres
      - redis

  frontend:
    build: ./frontend
    ports:
      - "9001:9001"

  postgres:
    image: postgres:15
    volumes:
      - pgdata:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
```

### Kubernetes Deployment (Helm)

```bash
# Add Sankalpa Helm repository
helm repo add sankalpa https://charts.sankalpa.dev

# Install with default values
helm install sankalpa sankalpa/sankalpa

# Install with custom values
helm install sankalpa sankalpa/sankalpa \
  --set backend.replicas=3 \
  --set frontend.replicas=2 \
  --set redis.enabled=true

# AWS EKS deployment
helm install sankalpa sankalpa/sankalpa -f deploy/helm/sankalpa/values-aws.yaml

# GCP GKE deployment
helm install sankalpa sankalpa/sankalpa -f deploy/helm/sankalpa/values-gcp.yaml

# Azure AKS deployment
helm install sankalpa sankalpa/sankalpa -f deploy/helm/sankalpa/values-azure.yaml
```

### Production Checklist

- [ ] Set `SANKALPA_ENV=production`
- [ ] Configure strong `SANKALPA_JWT_SECRET`
- [ ] Enable HTTPS with valid SSL certificates
- [ ] Configure proper `SANKALPA_ALLOWED_ORIGINS`
- [ ] Set up PostgreSQL for database
- [ ] Set up Redis for caching and sessions
- [ ] Configure rate limiting
- [ ] Set up monitoring and alerting
- [ ] Configure log aggregation
- [ ] Set up backup procedures
- [ ] Configure CDN for frontend assets

For detailed deployment instructions, see [docs/deployment-guide.md](./docs/deployment-guide.md).

---

## Protocols & Integrations

Sankalpa integrates multiple AI agent protocols and frameworks:

| Protocol | Purpose | Implementation | Location |
|----------|---------|----------------|----------|
| **LangChain** | Agent chaining, memory | ChainManager, MemoryManager | `agents/chain_manager.py` |
| **MCP** | Model Context Protocol | Agent orchestration | `agents/orchestration/` |
| **CrewAI** | Multi-agent collaboration | Role-based agents | `agents/enhanced/` |
| **AutoGen** | Task planning | PlannerAgent | `agents/orchestration/planner_agent.py` |
| **ReAct** | Reasoning + tool use | Copilot, Critic | `agents/enhanced/copilot_agent.py` |
| **PromptFlow** | Visual workflows | Composer UI | `frontend/pages/composer.tsx` |
| **GPT Engineer** | Project generation | Builder agents | `agents/builder/` |
| **BabyAGI** | Task planning | Planning system | `agents/orchestration/` |
| **Agent Contracts** | Input/Output schemas, validation | DependencyResolver | `agents/contracts.py` |

### Agent Integration Architecture (NEW)

Sankalpa v2.0 introduces a sophisticated agent integration system:

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        AGENT INTEGRATION ARCHITECTURE                            │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│   User Task                    Intelligent Orchestrator                          │
│   ──────────                   ─────────────────────────                         │
│   "Build a SaaS app"  ───────▶  analyze_task()                                  │
│                                       │                                          │
│                                       ▼                                          │
│                              ┌────────────────┐                                  │
│                              │ Task Analysis  │                                  │
│                              │ - Type: full_stack                               │
│                              │ - Caps: auth, db, ui                             │
│                              │ - Confidence: 0.9                                │
│                              └───────┬────────┘                                  │
│                                      │                                          │
│                                      ▼                                          │
│                              ┌────────────────┐                                  │
│                              │ Agent Contracts│                                  │
│                              │ (contracts.py) │                                  │
│                              │                │                                  │
│                              │ ┌────────────┐ │                                  │
│                              │ │ Capability │ │                                  │
│                              │ │ provides:  │ │                                  │
│                              │ │ requires:  │ │                                  │
│                              │ │ optional:  │ │                                  │
│                              │ └────────────┘ │                                  │
│                              └───────┬────────┘                                  │
│                                      │                                          │
│                                      ▼                                          │
│                              ┌────────────────┐                                  │
│                              │  Dependency    │                                  │
│                              │  Resolver      │                                  │
│                              │                │                                  │
│                              │ - validate_chain()                               │
│                              │ - filter_context()                               │
│                              │ - optimize_order()                               │
│                              └───────┬────────┘                                  │
│                                      │                                          │
│                                      ▼                                          │
│                         ┌────────────────────────┐                              │
│                         │     Chain Manager       │                              │
│                         │                         │                              │
│                         │  Agent 1 ──▶ Agent 2 ──▶ Agent N                     │
│                         │     │           │           │                          │
│                         │     ▼           ▼           ▼                          │
│                         │  Context     Context     Context                       │
│                         │  (filtered)  (filtered)  (filtered)                    │
│                         └────────────────────────┘                              │
│                                      │                                          │
│                                      ▼                                          │
│                              Generated Files                                     │
│                              + Accumulated Context                               │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

**Key Components:**

| Component | File | Purpose |
|-----------|------|---------|
| `AgentCapability` | `agents/contracts.py` | Declares what each agent provides/requires |
| `DependencyResolver` | `agents/contracts.py` | Validates chains, filters context |
| `ChainManager` | `agents/chain_manager.py` | Executes chains with tracking |
| `IntelligentOrchestrator` | `agents/orchestration/intelligent_orchestrator.py` | Auto-analyzes tasks |

**Benefits:**

- **Token Optimization**: Agents only receive context keys they need (reduces LLM costs by ~40%)
- **Validation**: Catch misconfigurations before runtime
- **Traceability**: Track exactly what each agent provided
- **Error Handling**: Chain continues even if one agent fails (configurable)

### External Integrations

| Integration | Purpose | Configuration |
|-------------|---------|---------------|
| **OpenAI** | LLM generation | `OPENAI_API_KEY` |
| **GitHub** | Code repositories | `GITHUB_TOKEN` |
| **Stripe** | Payment processing | `STRIPE_SECRET_KEY` |
| **SendGrid** | Email delivery | `SENDGRID_API_KEY` |
| **Azure AD** | Enterprise SSO | `AZURE_AD_*` |
| **Okta** | Enterprise SSO | `OKTA_*` |
| **Vercel** | Frontend deployment | Vercel CLI |
| **AWS** | Cloud deployment | AWS SDK |
| **GCP** | Cloud deployment | GCP SDK |

---

## Troubleshooting

### Common Issues

<details>
<summary><b>Backend won't start</b></summary>

```bash
# Check if port 9000 is in use
netstat -ano | findstr :9000  # Windows
lsof -i :9000                  # Linux/Mac

# Kill the process using the port
taskkill /PID <pid> /F         # Windows
kill -9 <pid>                  # Linux/Mac

# Try alternative port
python -m uvicorn backend.simple_main:app --port 9001
```
</details>

<details>
<summary><b>Frontend build fails</b></summary>

```bash
# Clear cache and reinstall
cd frontend
rm -rf node_modules package-lock.json .next
npm install
npm run dev
```
</details>

<details>
<summary><b>LLM Client not available</b></summary>

```bash
# Verify OpenAI key is set
echo $OPENAI_API_KEY

# Add to .env file
echo "OPENAI_API_KEY=sk-your-key" >> .env

# Restart the backend
python -m uvicorn backend.enhanced_main:app --reload
```
</details>

<details>
<summary><b>Agent not found error</b></summary>

```bash
# Verify agent exists in catalog
cat catalog/agent_catalog.json | grep "agent_name"

# Check agent file exists
ls agents/custom/
ls agents/builder/
```
</details>

<details>
<summary><b>CORS errors in browser</b></summary>

```bash
# Add your frontend URL to .env
SANKALPA_ALLOWED_ORIGINS=http://localhost:9001,http://localhost:3000

# Restart backend
```
</details>

### Debug Mode

```bash
# Enable verbose logging
SANKALPA_DEBUG=true
SANKALPA_LOG_LEVEL=DEBUG

# Run with debug flag
python -m uvicorn backend.enhanced_main:app --reload --log-level debug
```

---

## FAQ

<details>
<summary><b>What is Sankalpa?</b></summary>

Sankalpa is a multi-agent AI platform that autonomously builds, tests, and deploys complete software applications. Give it a prompt, and it orchestrates 35+ specialized AI agents to create your application.
</details>

<details>
<summary><b>Is Sankalpa free to use?</b></summary>

Yes, Sankalpa is open-source under the MIT license. You can use it freely for personal and commercial projects. LLM features require an OpenAI API key (pay-as-you-go).
</details>

<details>
<summary><b>Do I need an OpenAI API key?</b></summary>

For basic agent functionality, no. For LLM-powered code generation (recommended), you'll need an OpenAI API key set in your `.env` file.
</details>

<details>
<summary><b>Can agents run in parallel?</b></summary>

Yes! The Chain Manager supports sequential, parallel, and conditional execution modes.
</details>

<details>
<summary><b>How do I create a custom agent?</b></summary>

See the [Creating a Custom Agent](#creating-a-custom-agent) section above.
</details>

---

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

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
| [README.md](./README.md) | This file - project overview |
| [CONTRIBUTING.md](./CONTRIBUTING.md) | Contribution guidelines |
| [CLAUDE.md](./CLAUDE.md) | AI assistant quick reference |
| [docs/API.md](./docs/API.md) | Complete API documentation |
| [docs/system_architecture.md](./docs/system_architecture.md) | Architecture deep-dive |
| [docs/deployment-guide.md](./docs/deployment-guide.md) | Deployment guide |

---

## Roadmap

### Current Version (v2.0) - All Complete

- [x] 35+ specialized agents
- [x] Visual workflow composer
- [x] Memory system with sessions
- [x] Chain execution engine with context sharing
- [x] REST API with authentication
- [x] Next.js frontend
- [x] Docker deployment
- [x] Real-time WebSocket collaboration
- [x] Vector memory with embeddings
- [x] GraphQL API
- [x] Plugin system (50+ hooks)
- [x] Advanced LLM fine-tuning UI
- [x] Agent marketplace
- [x] VS Code extension
- [x] Enterprise SSO (SAML 2.0, OIDC)
- [x] Kubernetes Helm charts
- [x] Mobile PWA
- [x] OpenAI LLM integration

### Future Plans

- [ ] Native mobile apps (iOS/Android)
- [ ] Multi-language agent support
- [ ] AI model registry integration
- [ ] Advanced analytics dashboard
- [ ] Team collaboration features
- [ ] Anthropic Claude integration
- [ ] Local LLM support (Ollama, LM Studio)

---

## Support

- **Documentation**: [docs/](./docs/)
- **Issues**: [GitHub Issues](https://github.com/sreejagatab/Sankalpa/issues)
- **Discussions**: GitHub Discussions

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

[Get Started](#quick-start) | [Documentation](./docs/) | [Contributing](./CONTRIBUTING.md) | [Report Issue](https://github.com/sreejagatab/Sankalpa/issues)

---

Made with intention by the Sankalpa Team

</div>
