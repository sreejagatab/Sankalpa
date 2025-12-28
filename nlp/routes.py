from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import BaseModel
from typing import Dict, Any, List, Optional

from sankalpa.nlp.processor import nlp_processor
from sankalpa.core.security import get_current_user
from sankalpa.core import get_logger

router = APIRouter()
logger = get_logger("nlp.routes")

class NaturalLanguageRequest(BaseModel):
    """Request model for natural language commands"""
    command: str
    context: Optional[Dict[str, Any]] = None
    options: Optional[Dict[str, Any]] = None

class NaturalLanguageResponse(BaseModel):
    """Response model for natural language commands"""
    chain: Dict[str, Any]
    analysis: Dict[str, Any]
    execution_ready: bool

@router.post("/process", response_model=NaturalLanguageResponse)
async def process_command(
    request: NaturalLanguageRequest,
    current_user = Depends(get_current_user)
):
    """Process a natural language command into a chain specification
    
    This endpoint takes a natural language command and converts it into
    a structured chain specification that can be executed.
    """
    try:
        # Process the command
        chain = await nlp_processor.process_command(request.command)
        
        # Basic analysis
        analysis = {
            "agent_count": len(chain.get("agents", [])),
            "chain_type": chain.get("type", "sequential"),
            "estimated_complexity": _calculate_complexity(chain),
            "identified_entities": _extract_entities(request.command),
            "identified_requirements": _extract_requirements(request.command),
        }
        
        # Check if the chain is ready for execution
        execution_ready = _is_execution_ready(chain)
        
        return {
            "chain": chain,
            "analysis": analysis,
            "execution_ready": execution_ready
        }
    except Exception as e:
        logger.error(f"Error processing natural language command: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process command: {str(e)}")

def _calculate_complexity(chain: Dict[str, Any]) -> str:
    """Calculate the estimated complexity of a chain
    
    Args:
        chain: The chain specification
        
    Returns:
        Complexity level: "simple", "moderate", "complex"
    """
    agents_count = len(chain.get("agents", []))
    chain_type = chain.get("type", "sequential")
    
    if chain_type == "conditional":
        complexity_score = 5  # Base score for conditional chains
    elif chain_type == "parallel":
        complexity_score = 3  # Base score for parallel chains
    else:
        complexity_score = 1  # Base score for sequential chains
    
    # Add points based on number of agents
    complexity_score += min(agents_count, 7)
    
    # Determine complexity level
    if complexity_score <= 3:
        return "simple"
    elif complexity_score <= 7:
        return "moderate"
    else:
        return "complex"

def _extract_entities(command: str) -> List[str]:
    """Extract potential entities from the command
    
    Args:
        command: The natural language command
        
    Returns:
        List of identified entities
    """
    import re
    
    # This is a simplified entity extraction that looks for capitalized words
    # In a real implementation, you'd use NER from a library like spaCy
    entities = []
    
    # Look for capitalized words that might be entities
    matches = re.findall(r'\b[A-Z][a-zA-Z]*\b', command)
    for match in matches:
        if match not in ["I", "A", "The"] and len(match) > 1:
            entities.append(match)
    
    # Look for words that might be technical entities
    tech_patterns = [
        r'\b(?:REST|API|SQL|NoSQL|MongoDB|PostgreSQL|MySQL|React|Vue|Angular|Next\.js|Node\.js|Express|Django|Flask|FastAPI)\b',
    ]
    
    for pattern in tech_patterns:
        matches = re.findall(pattern, command, re.IGNORECASE)
        entities.extend([m.strip() for m in matches])
    
    return list(set(entities))  # Deduplicate

def _extract_requirements(command: str) -> List[str]:
    """Extract potential requirements from the command
    
    Args:
        command: The natural language command
        
    Returns:
        List of identified requirements
    """
    import re
    
    requirements = []
    
    # Look for requirement patterns
    requirement_patterns = [
        r'(?:should|must|needs to|has to) ([^,.;]+)',
        r'with ([^,.;]+ capabilities)',
        r'(?:include|support|provide) ([^,.;]+)'
    ]
    
    for pattern in requirement_patterns:
        matches = re.findall(pattern, command, re.IGNORECASE)
        requirements.extend([m.strip() for m in matches])
    
    return requirements

def _is_execution_ready(chain: Dict[str, Any]) -> bool:
    """Check if a chain is ready for execution
    
    Args:
        chain: The chain specification
        
    Returns:
        True if the chain is ready for execution
    """
    # Check if there are any agents
    if not chain.get("agents", []):
        return False
    
    # Check if all agents have required fields
    for agent in chain.get("agents", []):
        if not agent.get("name") or not agent.get("type"):
            return False
    
    # Check conditional chain requirements
    if chain.get("type") == "conditional":
        if not chain.get("condition_key") or not chain.get("condition_branches"):
            return False
            
        # Check if all branches reference valid agents
        agent_names = [a.get("name") for a in chain.get("agents", [])]
        for branch_agents in chain.get("condition_branches", {}).values():
            for agent_name in branch_agents:
                if agent_name not in agent_names:
                    return False
    
    return True