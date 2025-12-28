# Sankalpa Platform Demonstration

This document provides instructions on how to run and demonstrate the Sankalpa platform.

## System Overview

Sankalpa is a multi-agent AI platform that can autonomously build, test, and deploy projects. Key capabilities include:

- **Agent Generation**: Create new specialized agents dynamically
- **Chain Execution**: Run sequences of agents in a workflow
- **Memory Management**: Persistent storage of agent inputs and outputs
- **Visual Interface**: Web-based interface for interacting with agents

## Running the System

1. Make sure you have the required dependencies installed:
   ```
   pip install -r requirements.txt
   ```

2. Start the complete system with:
   ```
   python run_sankalpa.py
   ```

3. For testing individual components, use:
   ```
   python comprehensive_test.py  # Test core agent functionality
   python test_minimal_api.py    # Test API functionality
   ```

## Component Testing

### 1. Testing the Self-Replicator Agent

The self-replicator agent is the most powerful component of Sankalpa, allowing you to create new agents on demand:

```python
from agents.enhanced.self_replicator_agent import SelfReplicatorAgent
from memory.memory_manager import MemoryManager

# Create memory manager and agent
memory = MemoryManager()
agent = SelfReplicatorAgent("self_replicator", memory)

# Define a new agent
agent_spec = {
    "name": "text_analyzer",
    "description": "Analyzes text for sentiment and key metrics",
    "category": "nlp",
    "logic": """
        text = input_data.get("text", "")
        if not text:
            return {"error": "No text provided"}
            
        # Basic analysis
        word_count = len(text.split())
        char_count = len(text)
        
        # Simple sentiment (very basic)
        positive_words = ["good", "great", "excellent", "happy", "like", "love"]
        negative_words = ["bad", "terrible", "awful", "sad", "hate", "dislike"]
        
        positive_count = sum(1 for word in text.lower().split() if word in positive_words)
        negative_count = sum(1 for word in text.lower().split() if word in negative_words)
        
        sentiment = "neutral"
        if positive_count > negative_count:
            sentiment = "positive"
        elif negative_count > positive_count:
            sentiment = "negative"
            
        result = {
            "word_count": word_count,
            "character_count": char_count,
            "sentiment": sentiment
        }
        
        return result
    """,
    "inputs": [
        {"name": "text", "type": "string"}
    ],
    "outputs": [
        {"name": "word_count", "type": "number"},
        {"name": "character_count", "type": "number"},
        {"name": "sentiment", "type": "string"}
    ]
}

# Create the agent
result = agent.run(agent_spec)
print(f"Agent creation result: {result}")

# Now import and use the agent
from agents.custom.text_analyzer import TextAnalyzerAgent

analyzer = TextAnalyzerAgent("text_analyzer", memory)
text = "I really love the Sankalpa platform. It's an excellent tool!"
analysis = analyzer.run({"text": text})
print(f"Text analysis: {analysis}")
```

### 2. Testing Agent Chains

Sankalpa can chain multiple agents together to create complex workflows:

```python
from agents.chain_manager import ChainManager
from agents.builder.project_architect_agent import ProjectArchitectAgent
from agents.custom.hello_world import HelloWorldAgent

# Create a chain with two agents
chain = ChainManager([
    ProjectArchitectAgent("project_architect", memory),
    HelloWorldAgent("hello_world", memory)
], memory)

# Run the chain
result = chain.run({
    "project": "demo_project",
    "name": "Sankalpa"
})

print(f"Chain result: {result}")
```

## API Endpoints

Once the server is running, the following API endpoints are available:

- `GET /api/status`: Check server status
- `GET /api/agents`: List all available agents
- `GET /api/memory`: View memory contents
- `POST /api/create-agent`: Create a new agent
- `POST /api/agents/execute/{agent_name}`: Execute an agent

Example API call to create a new agent:
```
POST /api/create-agent
{
    "name": "text_summarizer",
    "description": "Summarizes text by extracting key sentences",
    "category": "nlp",
    "logic": "...",
    "inputs": [{"name": "text", "type": "string"}],
    "outputs": [{"name": "summary", "type": "string"}]
}
```

## Web Interface

The web interface provides a chat-based interaction with agents at:
```
http://localhost:3003/
```

## Troubleshooting

If you encounter issues:

1. Make sure all dependencies are installed: `pip install -r requirements.txt`
2. Check for port conflicts on 8080 and 3003
3. Ensure the `agents` and `memory` directories are properly initialized
4. Look for error messages in the console output