
import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
import os
import json
from pathlib import Path

class Config:
    """Configuration management for Sankalpa"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        # Default configuration
        self.default_config = {
            "app": {
                "name": "Sankalpa",
                "version": "1.0.0",
                "description": "AI-powered development automation platform"
            },
            "api": {
                "host": "0.0.0.0",
                "port": 8000,
                "debug": False,
                "allowed_origins": ["http://localhost:3000"]
            },
            "security": {
                "jwt_secret": "",  # Should be overridden by env var
                "jwt_algorithm": "HS256",
                "token_expire_minutes": 60,
                "refresh_token_expire_days": 7,
                "password_hash_iterations": 100000
            },
            "memory": {
                "default_store": "json",  # Options: json, redis, postgres
                "json_path": "memory/sessions",
                "redis_url": "redis://localhost:6379/0",
                "postgres_url": ""
            },
            "agents": {
                "timeout_seconds": 60,
                "max_retries": 3,
                "backoff_factor": 2,
                "recovery_strategy": "continue"  # Options: continue, retry, fail
            },
            "logging": {
                "level": "INFO",
                "file": "logs/sankalpa.log",
                "rotate": True,
                "max_size": 10485760,  # 10MB
                "backup_count": 5
            }
        }
        
        # Load configuration from file
        self.config_path = os.environ.get("SANKALPA_CONFIG", "config.json")
        self.config = self.default_config.copy()
        
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f:
                file_config = json.load(f)
                self._update_nested_dict(self.config, file_config)
        
        # Override with environment variables
        self._load_from_env()
        
        # Ensure critical directories exist
        self._ensure_directories()
    
    def _update_nested_dict(self, d, u):
        """Update nested dictionary with another dictionary"""
        for k, v in u.items():
            if isinstance(v, dict) and k in d and isinstance(d[k], dict):
                self._update_nested_dict(d[k], v)
            else:
                d[k] = v
    
    def _load_from_env(self):
        """Load configuration from environment variables"""
        # Critical security settings from env vars
        if jwt_secret := os.environ.get("SANKALPA_JWT_SECRET"):
            self.config["security"]["jwt_secret"] = jwt_secret
        
        # Other common settings
        if log_level := os.environ.get("SANKALPA_LOG_LEVEL"):
            self.config["logging"]["level"] = log_level
            
        if api_port := os.environ.get("SANKALPA_API_PORT"):
            self.config["api"]["port"] = int(api_port)
            
        if debug := os.environ.get("SANKALPA_DEBUG"):
            self.config["api"]["debug"] = debug.lower() == "true"
            
        # Handle allowed origins as comma-separated list
        if origins := os.environ.get("SANKALPA_ALLOWED_ORIGINS"):
            self.config["api"]["allowed_origins"] = [o.strip() for o in origins.split(",")]
    
    def _ensure_directories(self):
        """Ensure required directories exist"""
        directories = [
            self.config["memory"]["json_path"],
            os.path.dirname(self.config["logging"]["file"])
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
    
    def get(self, path, default=None):
        """Get a configuration value by dot-separated path"""
        parts = path.split(".")
        current = self.config
        
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return default
                
        return current
    
    def save(self):
        """Save the current configuration to file"""
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=2)
        
# Global config instance
config = Config()