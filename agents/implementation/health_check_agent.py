
import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from typing import Dict, Any, List, Optional
import time
import psutil
import os
import platform
import socket
import json
import requests
from datetime import datetime

from agents.enhanced_base import EnhancedBaseAgent, ValidationError
from core import get_logger, config

logger = get_logger("agent.health_check")

class HealthCheckAgent(EnhancedBaseAgent):
    """Agent for system health checking
    
    This agent monitors system health, checks connectivity to external
    services, and runs diagnostics to ensure system stability.
    """
    
    def __init__(self, name: str = "health_check", **kwargs):
        super().__init__(name, **kwargs)
        
    def _execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute health check operations
        
        Args:
            input_data: Dictionary containing:
                - checks: List of checks to perform (system, connectivity, services, all)
                - services: Optional list of services to check (for connectivity checks)
                - timeout: Optional timeout for connectivity checks
                
        Returns:
            Health check results
            
        Raises:
            ValidationError: If input is invalid
        """
        checks_to_run = input_data.get("checks", ["all"])
        if not isinstance(checks_to_run, list):
            checks_to_run = [checks_to_run]
            
        if "all" in checks_to_run:
            checks_to_run = ["system", "connectivity", "services"]
            
        results = {
            "timestamp": datetime.utcnow().isoformat(),
            "hostname": socket.gethostname()
        }
        
        if "system" in checks_to_run:
            results["system"] = self._check_system()
            
        if "connectivity" in checks_to_run:
            services = input_data.get("services", ["google.com", "github.com"])
            timeout = input_data.get("timeout", 5)
            results["connectivity"] = self._check_connectivity(services, timeout)
            
        if "services" in checks_to_run:
            results["services"] = self._check_services()
            
        # Determine overall health status
        status = "healthy"
        
        # Check system metrics
        if "system" in results:
            system = results["system"]
            if system["cpu_percent"] > 90 or system["memory_percent"] > 90:
                status = "warning"
                
            if system["disk_percent"] > 95:
                status = "critical"
                
        # Check connectivity
        if "connectivity" in results:
            conn = results["connectivity"]
            failure_count = sum(1 for check in conn["checks"] if not check["success"])
            total_count = len(conn["checks"])
            
            if failure_count > 0:
                if failure_count == total_count:
                    status = "critical"  # All connectivity checks failed
                else:
                    status = "warning"  # Some connectivity checks failed
                    
        # Check services
        if "services" in results:
            services = results["services"]
            if not services["api"]["online"]:
                status = "critical"  # API service is down
            elif not services["database"]["online"] or not services["cache"]["online"]:
                status = "warning"  # Database or cache service is down
                
        results["status"] = status
        
        return results
    
    def _check_system(self) -> Dict[str, Any]:
        """Check system metrics
        
        Returns:
            Dictionary of system metrics
        """
        # Get process info
        process = psutil.Process(os.getpid())
        
        # Get system info
        cpu_percent = psutil.cpu_percent()
        memory_percent = process.memory_percent()
        disk_percent = psutil.disk_usage('/').percent
        
        # Get system info
        uname = platform.uname()
        
        return {
            "cpu_percent": cpu_percent,
            "memory_percent": memory_percent,
            "disk_percent": disk_percent,
            "python_version": platform.python_version(),
            "os": {
                "system": uname.system,
                "release": uname.release,
                "version": uname.version,
                "machine": uname.machine
            },
            "load_average": psutil.getloadavg() if hasattr(psutil, 'getloadavg') else None,
            "uptime": time.time() - psutil.boot_time()
        }
    
    def _check_connectivity(self, services: List[str], timeout: int) -> Dict[str, Any]:
        """Check connectivity to external services
        
        Args:
            services: List of services to check
            timeout: Timeout for connection attempts
            
        Returns:
            Dictionary of connectivity test results
        """
        results = {
            "checks": []
        }
        
        for service in services:
            start_time = time.time()
            success = False
            latency = 0
            error = None
            
            try:
                # Try to connect
                if service.startswith(("http://", "https://")):
                    response = requests.get(service, timeout=timeout)
                    success = response.status_code < 400
                    latency = time.time() - start_time
                else:
                    # Assume it's a hostname
                    socket.setdefaulttimeout(timeout)
                    socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((service, 80))
                    latency = time.time() - start_time
                    success = True
            except Exception as e:
                error = str(e)
                
            results["checks"].append({
                "service": service,
                "success": success,
                "latency": latency,
                "error": error
            })
            
        # Calculate overall statistics
        successful_checks = [c for c in results["checks"] if c["success"]]
        results["success_rate"] = len(successful_checks) / len(results["checks"]) if results["checks"] else 1.0
        results["average_latency"] = sum(c["latency"] for c in successful_checks) / len(successful_checks) if successful_checks else 0
        
        return results
    
    def _check_services(self) -> Dict[str, Any]:
        """Check internal services
        
        Returns:
            Dictionary of service health checks
        """
        results = {}
        
        # Check API service
        api_url = config.get("api.health_check_url", "http://localhost:8000/api/health")
        api_result = {
            "online": False,
            "latency": 0,
            "details": None,
            "error": None
        }
        
        try:
            start_time = time.time()
            response = requests.get(api_url, timeout=5)
            api_result["latency"] = time.time() - start_time
            
            if response.status_code == 200:
                api_result["online"] = True
                api_result["details"] = response.json()
        except Exception as e:
            api_result["error"] = str(e)
            
        results["api"] = api_result
        
        # Check database service
        from backend.db.database import db
        db_result = {
            "online": False,
            "latency": 0,
            "error": None
        }
        
        try:
            if db.available:
                start_time = time.time()
                # Simple query to check connection
                db.execute("SELECT 1")
                db_result["latency"] = time.time() - start_time
                db_result["online"] = True
        except Exception as e:
            db_result["error"] = str(e)
            
        results["database"] = db_result
        
        # Check cache service
        from core.caching import cache
        cache_result = {
            "online": False,
            "latency": 0,
            "error": None
        }
        
        try:
            if hasattr(cache.backend, 'available') and cache.backend.available:
                start_time = time.time()
                # Test cache operations
                cache.set("__health_check__", {"timestamp": time.time()})
                value = cache.get("__health_check__")
                cache_result["latency"] = time.time() - start_time
                cache_result["online"] = value is not None
        except Exception as e:
            cache_result["error"] = str(e)
            
        results["cache"] = cache_result
        
        return results