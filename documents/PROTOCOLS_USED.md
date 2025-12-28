# 🧠 Protocols Used in Ultimate Sankalpa

Ultimate Sankalpa integrates the best of modern agent-based AI systems by combining the following protocols and concepts:

| Capability | Source Protocols | Implementation |
|------------|------------------|----------------|
| Agent Chaining | LangChain, MCP | ChainManager, ExecutionManager |
| Memory Recall | MemGPT, LangChain | MemoryManager, session logs, replayer |
| Multi-Agent Roles | CrewAI, AutoGen | Distinct agents: planner, builder, tester, deployer, critic |
| Reasoning + Tools | ReAct, LangChain | Used in copilot and critic agent logic |
| Self-Expanding Agents | MCP, AutoGPT | self_replicator_agent.py |
| Visual Workflow UI | PromptFlow, Flowise | composer.tsx (React Flow) |
| Project Generation | GPT Engineer | project_architect, builder agents |
| Task Planning | BabyAGI, AutoGen | planner_agent.py |
| Deployment Integration | MCP, GPT Engineer | deploy_executor_agent, domain_linker_agent |
| Test/Debug Agents | CrewAI, MCP | test_suite, integration_test, critic_agent |
| Chain Replay & Logs | LangGraph, MCP | session_replayer, memory log viewer |
| Plugin Integration | LangChain, MCP | plugin_loader_agent, plugin_registry |
| Fine-tuning & ML | OpenAI API, HuggingFace | finetuner_agent.py |
| Marketplace Support | AgentOps-style | Plugin + Template folders, chain registry |