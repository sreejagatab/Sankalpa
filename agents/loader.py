
import sys
import os
import json
import importlib
import glob
from typing import List, Dict, Any, Optional

# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

def load_agent(agent_name):
    """Load an agent by name"""
    try:
        # Special case handlers
        if agent_name == "enhanced.self_replicator" or agent_name == "self_replicator":
            from agents.enhanced.self_replicator_agent import SelfReplicatorAgent
            return SelfReplicatorAgent("self_replicator")
            
        if agent_name == "project_architect":
            from agents.builder.project_architect_agent import ProjectArchitectAgent
            return ProjectArchitectAgent(agent_name)
            
        # Handle custom agents
        if agent_name.startswith("custom.") or os.path.exists(f"agents/custom/{agent_name}.py"):
            name = agent_name.split(".")[-1] if "." in agent_name else agent_name
            module_name = f"agents.custom.{name}"
            class_name = name.title().replace('_', '') + 'Agent'
            
            try:
                module = importlib.import_module(module_name)
                agent_class = getattr(module, class_name)
                return agent_class(name)
            except Exception as e:
                print(f"Error loading custom agent {agent_name}: {str(e)}")
                return None
        
        # Try loading from catalog
        catalog_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "catalog", "agent_catalog.json")
        if os.path.exists(catalog_path):
            with open(catalog_path, "r") as f:
                catalog = json.load(f)
                
            if agent_name in catalog:
                module_path = catalog[agent_name].get("module", "")
                if module_path:
                    module_name = f"agents.{module_path}"
                    class_name = agent_name.title().replace('_', '') + 'Agent'
                    
                    module = importlib.import_module(module_name)
                    agent_class = getattr(module, class_name)
                    return agent_class(agent_name)
        
        # Generic loader for other agents
        for folder in ["builder", "testing", "deployment", "marketing", "enhanced", "orchestration"]:
            try:
                module_name = f"agents.{folder}.{agent_name}_agent"
                module = importlib.import_module(module_name)
                class_name = agent_name.title().replace('_', '') + 'Agent'
                agent_class = getattr(module, class_name)
                return agent_class(agent_name)
            except (ImportError, AttributeError):
                continue
                
        # Try direct module import
        try:
            module = importlib.import_module(f"agents.{agent_name}")
            agent_class = getattr(module, agent_name.title().replace('_', '') + 'Agent')
            return agent_class(agent_name)
        except Exception:
            pass
            
        raise ImportError(f"Could not find agent: {agent_name}")
        
    except Exception as e:
        print(f"Error loading agent {agent_name}: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def get_available_agents() -> List[Dict[str, Any]]:
    """Get a list of all available agents"""
    agents = []
    
    # Check catalog first
    catalog_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "catalog", "agent_catalog.json")
    if os.path.exists(catalog_path):
        try:
            with open(catalog_path, "r") as f:
                catalog = json.load(f)
            
            # Add agents from catalog
            for agent_id, agent_info in catalog.items():
                agents.append({
                    "name": agent_id,
                    "description": agent_info.get("description", ""),
                    "category": agent_info.get("category", "custom"),
                    "module": agent_info.get("module", ""),
                    "model": agent_info.get("model", "GPT-4"),
                    "inputs": agent_info.get("inputs", [{"name": "input", "type": "string"}]),
                    "outputs": agent_info.get("outputs", [{"name": "output", "type": "object"}])
                })
        except Exception as e:
            print(f"Error loading catalog: {str(e)}")
    
    # Add core agents
    core_agents = [
        {
            "name": "finetuner",
            "description": "Fine-tunes LLMs on custom datasets",
            "category": "enhanced",
            "module": "enhanced.finetuner_agent",
            "model": "GPT-4",
            "inputs": [
                {"name": "model", "type": "string"},
                {"name": "dataset", "type": "string"},
                {"name": "epochs", "type": "integer"},
                {"name": "batch_size", "type": "integer"},
                {"name": "learning_rate", "type": "number"}
            ],
            "outputs": [{"name": "files", "type": "object"}, {"name": "config", "type": "object"}]
        },
        {
            "name": "self_replicator",
            "description": "Creates specialized agents for specific tasks",
            "category": "enhanced",
            "module": "enhanced.self_replicator_agent",
            "model": "GPT-4",
            "inputs": [
                {"name": "name", "type": "string"},
                {"name": "description", "type": "string"},
                {"name": "category", "type": "string"},
                {"name": "logic", "type": "string"}
            ],
            "outputs": [{"name": "files", "type": "object"}]
        },
        {
            "name": "vs_code_extension",
            "description": "Creates VS Code extensions for agent integration",
            "category": "enhanced",
            "module": "enhanced.vs_code_extension_agent",
            "model": "GPT-4",
            "inputs": [
                {"name": "name", "type": "string"},
                {"name": "display_name", "type": "string"},
                {"name": "description", "type": "string"}
            ],
            "outputs": [{"name": "files", "type": "object"}]
        },
        {
            "name": "deploy_executor",
            "description": "Deploys projects to various platforms",
            "category": "deployment",
            "module": "deployment.deploy_executor_agent",
            "model": "GPT-4",
            "inputs": [
                {"name": "platform", "type": "string"},
                {"name": "project_type", "type": "string"},
                {"name": "project_path", "type": "string"}
            ],
            "outputs": [{"name": "files", "type": "object"}]
        },
        {
            "name": "project_architect",
            "description": "Creates project structures based on requirements",
            "category": "builder",
            "module": "builder.project_architect_agent",
            "model": "GPT-4",
            "inputs": [{"name": "requirements", "type": "string"}],
            "outputs": [{"name": "project_structure", "type": "object"}]
        }
    ]
    
    # Add core agents if not already in the list
    for core_agent in core_agents:
        if not any(a["name"] == core_agent["name"] for a in agents):
            agents.append(core_agent)
    
    # Add custom agents
    custom_dir = os.path.join(os.path.dirname(__file__), "custom")
    if os.path.exists(custom_dir):
        for filename in os.listdir(custom_dir):
            if filename.endswith(".py") and filename != "__init__.py":
                agent_name = filename[:-3]
                if not any(a["name"] == agent_name for a in agents):
                    agents.append({
                        "name": agent_name,
                        "description": f"Custom agent: {agent_name}",
                        "category": "custom",
                        "module": f"custom.{agent_name}",
                        "model": "GPT-4",
                        "inputs": [{"name": "input", "type": "string"}],
                        "outputs": [{"name": "output", "type": "object"}]
                    })
    
    # Find all potential agent modules in subdirectories
    agent_dirs = ["builder", "testing", "deployment", "marketing", "enhanced", "orchestration", "meta", "implementation"]
    for agent_dir in agent_dirs:
        dir_path = os.path.join(os.path.dirname(__file__), agent_dir)
        if os.path.exists(dir_path):
            for filename in glob.glob(os.path.join(dir_path, "*_agent.py")):
                base_name = os.path.basename(filename)[:-9]  # Remove _agent.py suffix
                if not any(a["name"] == base_name for a in agents):
                    agents.append({
                        "name": base_name,
                        "description": f"{agent_dir.capitalize()} agent: {base_name}",
                        "category": agent_dir,
                        "module": f"{agent_dir}.{base_name}_agent",
                        "model": "GPT-4",
                        "inputs": [{"name": "input", "type": "string"}],
                        "outputs": [{"name": "output", "type": "object"}]
                    })
    
    return agents
