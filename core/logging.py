
import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
import logging
import json
import sys
import os
from datetime import datetime

class CustomJsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcfromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
            
        return json.dumps(log_record)

def configure_logging(log_level=None, log_file=None):
    """Configure the logging system for Sankalpa."""
    if log_level is None:
        log_level = os.environ.get("SANKALPA_LOG_LEVEL", "INFO")
        
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Create handlers
    handlers = []
    
    # Always add console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(CustomJsonFormatter())
    handlers.append(console_handler)
    
    # Add file handler if specified
    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(CustomJsonFormatter())
        handlers.append(file_handler)
    
    # Configure root logger
    logging.basicConfig(
        level=numeric_level,
        handlers=handlers,
        force=True  # Override any existing configuration
    )
    
    # Create Sankalpa logger
    logger = logging.getLogger("sankalpa")
    logger.setLevel(numeric_level)
    
    return logger

def get_logger(name):
    """Get a logger with the given name, properly configured."""
    return logging.getLogger(f"sankalpa.{name}")