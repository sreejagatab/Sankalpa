import json
from agents.loader import load_agent
from memory.memory_manager import MemoryManager
from agents.chain_manager import ChainManager

def run_flow_from_file(flow_path):
    with open(flow_path, "r") as f:
        flow = json.load(f)

    agent_names = [
        node["label"].lower().replace("agent ", "").strip()
        for node in flow
        if "Agent" in node["label"]
    ]

    agents = [load_agent(name) for name in agent_names if load_agent(name)]
    chain = ChainManager(agents, MemoryManager())
    result = chain.run({"prompt": "Running saved flow chain."})
    print(json.dumps(result, indent=2))
