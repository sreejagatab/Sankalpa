import time
import sys
import os
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from core.monitoring import monitoring

class MetricsMiddleware(BaseHTTPMiddleware):
    """Middleware to collect API metrics"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Start timing the request
        start_time = time.time()
        
        # Process the request
        try:
            response = await call_next(request)
            
            # Record metrics for this request
            duration = time.time() - start_time
            method = request.method
            endpoint = self._get_endpoint_pattern(request)
            status_code = response.status_code
            
            # Update metrics
            monitoring.record_api_request(method, endpoint, status_code, duration)
            
            return response
            
        except Exception as e:
            # Record failed request
            duration = time.time() - start_time
            method = request.method
            endpoint = self._get_endpoint_pattern(request)
            
            # Update metrics with 500 status code
            monitoring.record_api_request(method, endpoint, 500, duration)
            
            # Re-raise the exception
            raise
    
    def _get_endpoint_pattern(self, request: Request) -> str:
        """Get a normalized pattern for the endpoint
        
        This converts paths like /users/123 to /users/{id} to prevent
        excessive cardinality in metrics
        """
        # Get the path from the request
        path = request.url.path
        
        # Replace numeric IDs with {id}
        # This is a simple heuristic and could be improved
        parts = path.split("/")
        for i, part in enumerate(parts):
            # If a path segment is entirely numeric, replace it with {id}
            if part.isdigit():
                parts[i] = "{id}"
                
            # UUIDs (simple heuristic)
            elif len(part) > 30 and "-" in part:
                parts[i] = "{id}"
        
        return "/".join(parts)