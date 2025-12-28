"""
Sankalpa - AI-Powered Development Automation Platform

A comprehensive AI-powered development automation platform 
that uses a multi-agent architecture to accelerate and enhance 
software development workflows.
"""

__version__ = "1.0.0"

# Add core subdirectories to the package
from . import agents
from . import memory
from . import core

# Make sure these are importable
try:
    from .agents.base import BaseAgent
    from .agents.chain_manager import ChainManager
except ImportError:
    pass