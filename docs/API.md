# Sankalpa API Documentation

## Overview

Sankalpa provides a RESTful API for agent execution, chain management, and memory operations. The API is built with FastAPI and includes JWT authentication, rate limiting, and comprehensive error handling.

## Base URL

```
http://localhost:9000/api
```

## Authentication

### JWT Token Authentication

Most endpoints require a valid JWT token. Obtain a token by logging in:

```bash
POST /api/users/login
Content-Type: application/json

{
  "username": "user@example.com",
  "password": "your-password"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### Using the Token

Include the token in the Authorization header:

```bash
Authorization: Bearer <access_token>
```

---

## Endpoints

### Status

#### GET /api/status

Health check endpoint. No authentication required.

**Request:**
```bash
curl http://localhost:9000/api/status
```

**Response:**
```json
{
  "status": "Sankalpa API Server is running!",
  "version": "1.0.0"
}
```

---

### Agents

#### GET /api/agents

List all available agents with their metadata.

**Request:**
```bash
curl http://localhost:9000/api/agents
```

**Response:**
```json
{
  "agents": [
    {
      "name": "hello_world",
      "description": "A simple hello world agent",
      "category": "testing",
      "model": "GPT-4",
      "inputs": [{"name": "name", "type": "string"}],
      "outputs": [{"name": "greeting", "type": "string"}]
    },
    {
      "name": "project_architect",
      "description": "Creates project structure and module plan",
      "category": "builder",
      "model": "GPT-4",
      "inputs": [{"name": "requirements", "type": "string"}],
      "outputs": [{"name": "project_structure", "type": "object"}]
    }
  ]
}
```

#### GET /api/agents/enhanced

List agents in enhanced format for the composer UI.

**Response:**
```json
[
  {
    "id": "hello_world",
    "name": "Hello World",
    "description": "A simple hello world agent",
    "category": "testing",
    "model": "GPT-4"
  }
]
```

#### POST /api/agents/execute

Execute a single agent with input data.

**Request:**
```bash
curl -X POST http://localhost:9000/api/agents/execute \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "hello_world",
    "input_data": {"name": "User"}
  }'
```

**Response:**
```json
{
  "agent_name": "hello_world",
  "execution_id": "exec_1234567890",
  "result": {
    "greeting": "Hello, User!"
  },
  "execution_time": 0.001234
}
```

**Error Response:**
```json
{
  "detail": "Agent 'unknown_agent' not found"
}
```

---

### Chains

#### GET /api/chains

List available chain templates.

**Request:**
```bash
curl http://localhost:9000/api/chains
```

**Response:**
```json
{
  "chains": [
    {
      "name": "full_stack_builder",
      "description": "Build a complete full-stack application",
      "agents": ["project_architect", "frontend_builder", "backend_builder", "db_schema"]
    },
    {
      "name": "api_generator",
      "description": "Generate a REST API with database schema",
      "agents": ["db_schema", "backend_builder", "api_builder"]
    }
  ]
}
```

#### POST /api/chains/execute

Execute a chain of agents sequentially.

**Request:**
```bash
curl -X POST http://localhost:9000/api/chains/execute \
  -H "Content-Type: application/json" \
  -d '{
    "chain_name": "builder_chain",
    "agents": ["project_architect", "frontend_builder"],
    "input_data": {"app_name": "MyApp", "type": "web"},
    "session_id": "optional-session-id"
  }'
```

**Response:**
```json
{
  "chain_name": "builder_chain",
  "status": "completed",
  "session_id": "abc123-def456",
  "results": [
    {
      "agent": "project_architect",
      "status": "success",
      "result": {
        "message": "Project structure initialized",
        "files": {...}
      },
      "execution_time": 0.005
    },
    {
      "agent": "frontend_builder",
      "status": "success",
      "result": {
        "message": "Frontend scaffold generated",
        "files": {...}
      },
      "execution_time": 0.003
    }
  ],
  "final_output": {...}
}
```

---

### Memory

#### POST /api/memory/save

Save a key-value pair to memory.

**Request:**
```bash
curl -X POST http://localhost:9000/api/memory/save \
  -H "Content-Type: application/json" \
  -d '{
    "key": "user_preferences",
    "value": {"theme": "dark", "language": "en"},
    "session_id": "my-session"
  }'
```

**Response:**
```json
{
  "status": "success",
  "message": "Saved key 'user_preferences' to memory",
  "session_id": "my-session"
}
```

#### POST /api/memory/load

Load a value from memory by key.

**Request:**
```bash
curl -X POST http://localhost:9000/api/memory/load \
  -H "Content-Type: application/json" \
  -d '{
    "key": "user_preferences",
    "session_id": "my-session"
  }'
```

**Response:**
```json
{
  "status": "success",
  "key": "user_preferences",
  "value": {"theme": "dark", "language": "en"},
  "session_id": "my-session"
}
```

#### GET /api/memory/all

Get all memory items for a session.

**Request:**
```bash
curl "http://localhost:9000/api/memory/all?session_id=my-session"
```

**Response:**
```json
{
  "status": "success",
  "session_id": "my-session",
  "data": {
    "user_preferences": {"theme": "dark", "language": "en"},
    "last_agent": "project_architect"
  }
}
```

#### GET /api/memory/sessions

List all available memory sessions.

**Request:**
```bash
curl http://localhost:9000/api/memory/sessions
```

**Response:**
```json
{
  "status": "success",
  "sessions": [
    "my-session",
    "another-session",
    "default"
  ]
}
```

---

## Agent Examples

### Hello World Agent

```bash
curl -X POST http://localhost:9000/api/agents/execute \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "hello_world",
    "input_data": {"name": "World"}
  }'
```

### Calculator Agent

```bash
curl -X POST http://localhost:9000/api/agents/execute \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "custom_calculator",
    "input_data": {
      "operation": "add",
      "a": 10,
      "b": 25
    }
  }'
```

### Project Architect Agent

```bash
curl -X POST http://localhost:9000/api/agents/execute \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "project_architect",
    "input_data": {
      "app_name": "MyApp",
      "type": "web",
      "features": ["auth", "dashboard"]
    }
  }'
```

### Frontend Builder Agent

```bash
curl -X POST http://localhost:9000/api/agents/execute \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "frontend_builder",
    "input_data": {
      "component_name": "UserProfile",
      "fields": ["name", "email", "avatar"]
    }
  }'
```

### Backend Builder Agent

```bash
curl -X POST http://localhost:9000/api/agents/execute \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "backend_builder",
    "input_data": {
      "resource": "users",
      "methods": ["GET", "POST", "PUT", "DELETE"]
    }
  }'
```

---

## Chain Examples

### Full Stack Builder Chain

```bash
curl -X POST http://localhost:9000/api/chains/execute \
  -H "Content-Type: application/json" \
  -d '{
    "chain_name": "full_stack",
    "agents": ["project_architect", "frontend_builder", "backend_builder", "db_schema"],
    "input_data": {
      "app_name": "MyBlog",
      "type": "web",
      "features": ["auth", "posts", "comments"]
    }
  }'
```

### API Generator Chain

```bash
curl -X POST http://localhost:9000/api/chains/execute \
  -H "Content-Type: application/json" \
  -d '{
    "chain_name": "api_generator",
    "agents": ["db_schema", "backend_builder", "api_builder"],
    "input_data": {
      "resource": "products",
      "fields": ["id", "name", "price", "description"]
    }
  }'
```

---

## Error Handling

### Error Response Format

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Invalid or missing token |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource doesn't exist |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error |

### Error Examples

**Missing required field:**
```json
{
  "detail": "Missing 'agent_name' in request"
}
```

**Agent not found:**
```json
{
  "detail": "Agent 'unknown_agent' not found"
}
```

**Rate limit exceeded:**
```json
{
  "detail": "Rate limit exceeded. Try again in 60 seconds."
}
```

---

## Rate Limiting

The API implements per-IP rate limiting:

- **Default limit**: 100 requests per minute
- **Burst limit**: 10 requests per second

When exceeded, returns HTTP 429 with retry information.

---

## WebSocket Endpoints

### /ws/collaboration

Real-time collaboration WebSocket for multi-user sessions.

```javascript
const ws = new WebSocket('ws://localhost:9000/ws/collaboration');

ws.onopen = () => {
  ws.send(JSON.stringify({
    type: 'join',
    session_id: 'my-session',
    user_id: 'user123'
  }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
};
```

---

## SDK Usage

### Python

```python
import requests

BASE_URL = "http://localhost:9000/api"

# Execute agent
response = requests.post(
    f"{BASE_URL}/agents/execute",
    json={
        "agent_name": "hello_world",
        "input_data": {"name": "Python"}
    }
)
result = response.json()
print(result["result"]["greeting"])
```

### JavaScript/TypeScript

```typescript
const API_URL = 'http://localhost:9000/api';

async function executeAgent(agentName: string, inputData: object) {
  const response = await fetch(`${API_URL}/agents/execute`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      agent_name: agentName,
      input_data: inputData
    })
  });
  return response.json();
}

// Usage
const result = await executeAgent('hello_world', { name: 'JavaScript' });
console.log(result.result.greeting);
```

### cURL

```bash
# List agents
curl http://localhost:9000/api/agents

# Execute agent
curl -X POST http://localhost:9000/api/agents/execute \
  -H "Content-Type: application/json" \
  -d '{"agent_name": "hello_world", "input_data": {"name": "cURL"}}'

# Execute chain
curl -X POST http://localhost:9000/api/chains/execute \
  -H "Content-Type: application/json" \
  -d '{"chain_name": "test", "agents": ["hello_world"], "input_data": {"name": "Chain"}}'
```

---

## Pagination

For endpoints that return lists, use pagination parameters:

```bash
GET /api/agents?page=1&limit=20
```

**Response includes:**
```json
{
  "items": [...],
  "total": 35,
  "page": 1,
  "limit": 20,
  "pages": 2
}
```

---

## Versioning

The API version is included in responses:

```json
{
  "status": "...",
  "version": "1.0.0"
}
```

Future versions will be accessible via:
```
/api/v2/...
```
