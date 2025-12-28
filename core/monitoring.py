
import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
import time
import threading
import psutil
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

from .logging import get_logger

logger = get_logger("monitoring")

@dataclass
class PerformanceMetrics:
    """Container for system performance metrics"""
    cpu_percent: float = 0.0
    memory_percent: float = 0.0
    disk_usage_percent: float = 0.0
    open_file_descriptors: int = 0
    thread_count: int = 0
    timestamp: float = 0.0

@dataclass
class ApiMetrics:
    """Container for API request metrics"""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    response_times: List[float] = field(default_factory=list)
    endpoints: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    
    @property
    def average_response_time(self) -> float:
        """Calculate average response time"""
        if not self.response_times:
            return 0.0
        return sum(self.response_times) / len(self.response_times)
    
    @property
    def success_rate(self) -> float:
        """Calculate API success rate"""
        if self.total_requests == 0:
            return 100.0
        return (self.successful_requests / self.total_requests) * 100

@dataclass
class AgentMetrics:
    """Container for agent execution metrics"""
    total_executions: int = 0
    successful_executions: int = 0
    failed_executions: int = 0
    average_execution_time: float = 0.0
    executions_by_agent: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    
    @property
    def success_rate(self) -> float:
        """Calculate agent success rate"""
        if self.total_executions == 0:
            return 100.0
        return (self.successful_executions / self.total_executions) * 100

class MonitoringSystem:
    """System monitoring for Sankalpa"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MonitoringSystem, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize the monitoring system"""
        self.system_metrics = PerformanceMetrics()
        self.api_metrics = ApiMetrics()
        self.agent_metrics = AgentMetrics()
        self.is_collecting = False
        self.collection_thread = None
        self.collection_interval = 10  # seconds
        
        # Prometheus metrics (if installed)
        try:
            from prometheus_client import Counter, Gauge, Histogram
            
            # System metrics
            self.prom_cpu_usage = Gauge('sankalpa_cpu_usage_percent', 'Current CPU usage percentage')
            self.prom_memory_usage = Gauge('sankalpa_memory_usage_percent', 'Current memory usage percentage')
            self.prom_disk_usage = Gauge('sankalpa_disk_usage_percent', 'Current disk usage percentage')
            self.prom_open_files = Gauge('sankalpa_open_file_descriptors', 'Number of open file descriptors')
            
            # API metrics
            self.prom_http_requests_total = Counter('sankalpa_http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
            self.prom_http_request_duration = Histogram('sankalpa_http_request_duration_seconds', 'HTTP request duration in seconds', ['method', 'endpoint'])
            
            # Agent metrics
            self.prom_agent_executions_total = Counter('sankalpa_agent_executions_total', 'Total agent executions', ['agent', 'status'])
            self.prom_agent_execution_duration = Histogram('sankalpa_agent_execution_duration_seconds', 'Agent execution duration in seconds', ['agent'])
            
            self.has_prometheus = True
            logger.info("Prometheus metrics enabled")
        except ImportError:
            self.has_prometheus = False
            logger.info("Prometheus metrics not available")
    
    def start(self):
        """Start collecting metrics"""
        if self.is_collecting:
            return
            
        self.is_collecting = True
        self.collection_thread = threading.Thread(target=self._collect_metrics_loop, daemon=True)
        self.collection_thread.start()
        logger.info("Monitoring system started")
    
    def stop(self):
        """Stop collecting metrics"""
        self.is_collecting = False
        if self.collection_thread:
            self.collection_thread.join(timeout=1.0)
        logger.info("Monitoring system stopped")
    
    def _collect_metrics_loop(self):
        """Background thread to collect system metrics"""
        while self.is_collecting:
            try:
                self._collect_system_metrics()
                time.sleep(self.collection_interval)
            except Exception as e:
                logger.error(f"Error collecting metrics: {str(e)}")
    
    def _collect_system_metrics(self):
        """Collect current system performance metrics"""
        try:
            # Get process info
            process = psutil.Process(os.getpid())
            
            # Update metrics
            self.system_metrics.cpu_percent = psutil.cpu_percent()
            self.system_metrics.memory_percent = process.memory_percent()
            self.system_metrics.disk_usage_percent = psutil.disk_usage('/').percent
            self.system_metrics.open_file_descriptors = process.num_fds() if hasattr(process, 'num_fds') else 0
            self.system_metrics.thread_count = threading.active_count()
            self.system_metrics.timestamp = time.time()
            
            # Update Prometheus metrics if available
            if self.has_prometheus:
                self.prom_cpu_usage.set(self.system_metrics.cpu_percent)
                self.prom_memory_usage.set(self.system_metrics.memory_percent)
                self.prom_disk_usage.set(self.system_metrics.disk_usage_percent)
                self.prom_open_files.set(self.system_metrics.open_file_descriptors)
                
        except Exception as e:
            logger.error(f"Error collecting system metrics: {str(e)}")
    
    def record_api_request(self, method: str, endpoint: str, status_code: int, duration: float):
        """Record an API request"""
        self.api_metrics.total_requests += 1
        self.api_metrics.response_times.append(duration)
        
        # Limit memory usage by keeping only the last 1000 response times
        if len(self.api_metrics.response_times) > 1000:
            self.api_metrics.response_times = self.api_metrics.response_times[-1000:]
        
        # Update success/failure counts
        if 200 <= status_code < 400:
            self.api_metrics.successful_requests += 1
        else:
            self.api_metrics.failed_requests += 1
        
        # Update endpoint-specific metrics
        if endpoint not in self.api_metrics.endpoints:
            self.api_metrics.endpoints[endpoint] = {
                "total": 0,
                "success": 0,
                "failure": 0,
                "response_times": []
            }
        
        self.api_metrics.endpoints[endpoint]["total"] += 1
        self.api_metrics.endpoints[endpoint]["response_times"].append(duration)
        
        # Limit memory usage
        if len(self.api_metrics.endpoints[endpoint]["response_times"]) > 100:
            self.api_metrics.endpoints[endpoint]["response_times"] = self.api_metrics.endpoints[endpoint]["response_times"][-100:]
        
        if 200 <= status_code < 400:
            self.api_metrics.endpoints[endpoint]["success"] += 1
        else:
            self.api_metrics.endpoints[endpoint]["failure"] += 1
        
        # Update Prometheus metrics if available
        if self.has_prometheus:
            status_category = f"{status_code // 100}xx"
            self.prom_http_requests_total.labels(method=method, endpoint=endpoint, status=status_category).inc()
            self.prom_http_request_duration.labels(method=method, endpoint=endpoint).observe(duration)
    
    def record_agent_execution(self, agent_name: str, success: bool, execution_time: float):
        """Record an agent execution"""
        self.agent_metrics.total_executions += 1
        
        if success:
            self.agent_metrics.successful_executions += 1
        else:
            self.agent_metrics.failed_executions += 1
        
        # Update agent-specific metrics
        if agent_name not in self.agent_metrics.executions_by_agent:
            self.agent_metrics.executions_by_agent[agent_name] = {
                "total": 0,
                "success": 0,
                "failure": 0,
                "execution_times": [],
                "average_time": 0.0
            }
        
        agent_data = self.agent_metrics.executions_by_agent[agent_name]
        agent_data["total"] += 1
        agent_data["execution_times"].append(execution_time)
        
        # Limit memory usage
        if len(agent_data["execution_times"]) > 100:
            agent_data["execution_times"] = agent_data["execution_times"][-100:]
        
        agent_data["average_time"] = sum(agent_data["execution_times"]) / len(agent_data["execution_times"])
        
        if success:
            agent_data["success"] += 1
        else:
            agent_data["failure"] += 1
        
        # Update overall average execution time
        total_time = 0
        total_count = 0
        
        for agent_data in self.agent_metrics.executions_by_agent.values():
            total_time += sum(agent_data["execution_times"])
            total_count += len(agent_data["execution_times"])
        
        if total_count > 0:
            self.agent_metrics.average_execution_time = total_time / total_count
        
        # Update Prometheus metrics if available
        if self.has_prometheus:
            status = "success" if success else "failure"
            self.prom_agent_executions_total.labels(agent=agent_name, status=status).inc()
            self.prom_agent_execution_duration.labels(agent=agent_name).observe(execution_time)
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health status"""
        health_status = "healthy"
        
        # Check if CPU or memory usage is too high
        if self.system_metrics.cpu_percent > 90 or self.system_metrics.memory_percent > 90:
            health_status = "warning"
        
        # Check API failure rate
        api_failure_rate = 100 - self.api_metrics.success_rate
        if api_failure_rate > 10:  # More than 10% failures
            health_status = "warning"
        
        if api_failure_rate > 25:  # More than 25% failures
            health_status = "critical"
        
        # Check agent failure rate
        agent_failure_rate = 100 - self.agent_metrics.success_rate
        if agent_failure_rate > 10:  # More than 10% failures
            health_status = "warning"
        
        if agent_failure_rate > 25:  # More than 25% failures
            health_status = "critical"
        
        return {
            "status": health_status,
            "timestamp": time.time(),
            "metrics": {
                "system": {
                    "cpu_percent": self.system_metrics.cpu_percent,
                    "memory_percent": self.system_metrics.memory_percent,
                    "disk_usage_percent": self.system_metrics.disk_usage_percent,
                    "thread_count": self.system_metrics.thread_count
                },
                "api": {
                    "total_requests": self.api_metrics.total_requests,
                    "success_rate": self.api_metrics.success_rate,
                    "average_response_time": self.api_metrics.average_response_time
                },
                "agents": {
                    "total_executions": self.agent_metrics.total_executions,
                    "success_rate": self.agent_metrics.success_rate,
                    "average_execution_time": self.agent_metrics.average_execution_time
                }
            }
        }

# Singleton instance
monitoring = MonitoringSystem()