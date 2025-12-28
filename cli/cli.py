from agents.loader import load_agent
import typer

app = typer.Typer()

@app.command()
def run_agent(name: str, prompt: str = ""):
    agent = load_agent(name)
    if agent:
        result = agent.run({"prompt": prompt})
        print(result)

@app.command()
def run_chain(*names: str):
    from memory.memory_manager import MemoryManager
    from agents.chain_manager import ChainManager

    memory = MemoryManager()
    agents = [load_agent(name) for name in names if load_agent(name)]
    chain = ChainManager(agents, memory)
    result = chain.run({"prompt": "Auto-run from CLI"})
    print(result)

if __name__ == "__main__":
    app()
