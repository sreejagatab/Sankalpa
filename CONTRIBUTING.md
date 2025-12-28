# Contributing to Sankalpa

Thank you for your interest in contributing to Sankalpa! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [How to Contribute](#how-to-contribute)
- [Creating Agents](#creating-agents)
- [Pull Request Process](#pull-request-process)
- [Code Style](#code-style)
- [Testing](#testing)
- [Documentation](#documentation)

---

## Code of Conduct

- Be respectful and inclusive in all interactions
- Help others who have questions or issues
- Share ideas and suggestions constructively
- Follow the project's technical guidelines

---

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/sankalpa.git
   cd sankalpa
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/original/sankalpa.git
   ```

---

## Development Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- Git

### Backend Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install dev dependencies
pip install -r requirements-dev.txt
```

### Frontend Setup

```bash
cd frontend
npm install
```

### Running the Development Server

```bash
# Terminal 1: Backend
python -m uvicorn backend.simple_main:app --host 0.0.0.0 --port 9000 --reload

# Terminal 2: Frontend
cd frontend && npm run dev
```

### Running with Docker

```bash
docker-compose up -d
```

---

## Project Structure

```
sankalpa/
├── agents/                 # AI Agents
│   ├── base.py            # BaseAgent class
│   ├── loader.py          # Dynamic agent loader
│   ├── builder/           # Builder agents (11)
│   ├── testing/           # Testing agents (4)
│   ├── deployment/        # Deployment agents (3)
│   ├── marketing/         # Marketing agents (4)
│   ├── enhanced/          # Enhanced agents (6)
│   ├── meta/              # Meta agents (2)
│   ├── orchestration/     # Orchestration agents (3)
│   └── custom/            # Custom agents (5+)
├── backend/               # FastAPI Backend
│   ├── simple_main.py     # API server
│   ├── routers/           # API endpoints
│   └── db/                # Database models
├── core/                  # Core Services
│   ├── config.py          # Configuration
│   ├── security.py        # Authentication
│   ├── caching.py         # Caching layer
│   └── monitoring.py      # Metrics
├── memory/                # Memory System
├── frontend/              # Next.js Frontend
│   ├── pages/             # App pages
│   └── components/        # React components
├── tests/                 # Test suites
│   ├── unit/
│   ├── integration/
│   └── e2e/
└── docs/                  # Documentation
```

---

## How to Contribute

### Types of Contributions

1. **Bug Fixes**: Fix existing issues
2. **New Features**: Add new functionality
3. **New Agents**: Create specialized agents
4. **Documentation**: Improve docs and examples
5. **Tests**: Add or improve test coverage
6. **Performance**: Optimize existing code

### Finding Issues to Work On

- Check [GitHub Issues](https://github.com/original/sankalpa/issues)
- Look for `good first issue` labels for beginners
- Look for `help wanted` labels for priority items

---

## Creating Agents

### Step 1: Create the Agent File

Create a new file in the appropriate category folder:

```python
# agents/custom/my_agent.py
from agents.base import BaseAgent
from typing import Dict, Any

class MyCustomAgent(BaseAgent):
    """
    Description of what your agent does.

    Category: custom
    """

    def __init__(self, name="my_custom_agent", memory=None):
        super().__init__(name, memory)
        self.category = "custom"
        self.description = "My custom agent description"

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the agent with the given input data.

        Args:
            input_data: Dictionary containing input parameters

        Returns:
            Dictionary containing agent output
        """
        # Validate inputs
        required_fields = ["field1", "field2"]
        for field in required_fields:
            if field not in input_data:
                return {
                    "status": "error",
                    "error": f"Missing required input: {field}"
                }

        # Your agent logic here
        result = {
            "output": "processed data",
            "field1": input_data.get("field1")
        }

        return {
            "status": "success",
            "message": "Agent executed successfully",
            "data": result
        }
```

### Step 2: Register in Agent Catalog

Add your agent to `catalog/agent_catalog.json`:

```json
{
  "my_custom_agent": {
    "description": "My custom agent description",
    "category": "custom",
    "model": "GPT-4",
    "module": "agents.custom.my_agent",
    "class": "MyCustomAgent",
    "inputs": [
      {"name": "field1", "type": "string"},
      {"name": "field2", "type": "object"}
    ],
    "outputs": [
      {"name": "output", "type": "string"},
      {"name": "data", "type": "object"}
    ]
  }
}
```

### Step 3: Add Tests

Create tests for your agent:

```python
# tests/unit/agents/test_my_agent.py
import pytest
from agents.custom.my_agent import MyCustomAgent

def test_my_agent_success():
    agent = MyCustomAgent()
    result = agent.run({
        "field1": "value1",
        "field2": {"key": "value"}
    })
    assert result["status"] == "success"

def test_my_agent_missing_input():
    agent = MyCustomAgent()
    result = agent.run({})
    assert result["status"] == "error"
    assert "Missing required input" in result["error"]
```

### Step 4: Test Your Agent

```bash
# Run via API
curl -X POST http://localhost:9000/api/agents/execute \
  -H "Content-Type: application/json" \
  -d '{"agent_name": "my_custom_agent", "input_data": {"field1": "test"}}'

# Run tests
pytest tests/unit/agents/test_my_agent.py -v
```

---

## Pull Request Process

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

### 2. Make Your Changes

- Write clean, readable code
- Follow the code style guidelines
- Add tests for new functionality
- Update documentation as needed

### 3. Commit Your Changes

```bash
git add .
git commit -m "Brief description of changes"
```

**Commit Message Format:**
- `feat: Add new feature`
- `fix: Fix bug description`
- `docs: Update documentation`
- `test: Add tests for feature`
- `refactor: Refactor code`

### 4. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

### 5. PR Review Checklist

- [ ] Code follows project style guidelines
- [ ] All tests pass
- [ ] New functionality has tests
- [ ] Documentation is updated
- [ ] No security vulnerabilities introduced
- [ ] PR description clearly explains changes

---

## Code Style

### Python

We use the following tools:

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking

```bash
# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Run manually
black .
isort .
flake8 .
mypy .
```

**Style Guidelines:**

```python
# Use type hints
def process_data(input_data: Dict[str, Any]) -> Dict[str, Any]:
    pass

# Use docstrings
def my_function(param: str) -> str:
    """
    Brief description.

    Args:
        param: Description of parameter

    Returns:
        Description of return value
    """
    pass

# Constants in UPPER_CASE
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30

# Class names in PascalCase
class MyCustomAgent(BaseAgent):
    pass

# Function and variable names in snake_case
def process_input_data():
    user_input = get_input()
```

### TypeScript/JavaScript

We use:

- **ESLint**: Linting
- **Prettier**: Code formatting

```bash
cd frontend
npm run lint
npm run format
```

**Style Guidelines:**

```typescript
// Use TypeScript types
interface AgentResult {
  status: string;
  data: Record<string, unknown>;
}

// Use functional components
const AgentCard: React.FC<AgentCardProps> = ({ agent }) => {
  return <div>{agent.name}</div>;
};

// Use async/await
async function fetchAgents(): Promise<Agent[]> {
  const response = await fetch('/api/agents');
  return response.json();
}
```

---

## Testing

### Running Tests

```bash
# All backend tests
pytest

# With coverage
pytest --cov=sankalpa tests/

# Specific test file
pytest tests/unit/test_agents.py

# Frontend tests
cd frontend && npm test
```

### Test Categories

- `tests/unit/`: Unit tests for individual components
- `tests/integration/`: Integration tests for API endpoints
- `tests/e2e/`: End-to-end tests for workflows
- `tests/security/`: Security-focused tests
- `tests/performance/`: Performance benchmarks

### Writing Tests

```python
# Use descriptive names
def test_agent_returns_error_when_input_missing():
    pass

# Use fixtures
@pytest.fixture
def sample_agent():
    return HelloWorldAgent()

def test_agent_execution(sample_agent):
    result = sample_agent.run({"name": "Test"})
    assert result["greeting"] == "Hello, Test!"

# Use parametrize for multiple cases
@pytest.mark.parametrize("input,expected", [
    ({"a": 1, "b": 2}, 3),
    ({"a": -1, "b": 1}, 0),
])
def test_calculator_add(input, expected):
    agent = CalculatorAgent()
    result = agent.run({**input, "operation": "add"})
    assert result["data"]["calculation"] == expected
```

---

## Documentation

### When to Update Docs

- Adding new features
- Adding new agents
- Changing API endpoints
- Changing configuration options

### Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Project overview and quick start |
| `CONTRIBUTING.md` | Contribution guidelines |
| `CLAUDE.md` | Quick reference for AI assistants |
| `docs/system_architecture.md` | Architecture details |
| `docs/API.md` | API documentation |
| `docs/production-deployment.md` | Deployment guide |

### Documentation Style

- Use clear, concise language
- Include code examples
- Use tables for structured data
- Add diagrams for complex concepts

---

## Questions?

- Check existing [GitHub Issues](https://github.com/original/sankalpa/issues)
- Open a new issue for questions
- Join community discussions

Thank you for contributing to Sankalpa!
