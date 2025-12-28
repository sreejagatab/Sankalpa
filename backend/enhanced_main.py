from fastapi import FastAPI, Depends, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import time
import traceback
import os
import sys

# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

# Direct imports instead of package imports
from core import config
from core.logging import get_logger
from core.security import (
    get_current_user, RateLimiter, SecurityHeaders,
    RateLimitExceededError, SecurityError
)
from core.monitoring import monitoring
from backend.middleware.metrics import MetricsMiddleware
from backend.db.database import db

# Initialize logger
logger = get_logger("api")

# Create the FastAPI application
app = FastAPI(
    title=config.get("app.name", "Sankalpa"),
    description=config.get("app.description", "AI-powered development automation platform"),
    version=config.get("app.version", "1.0.0"),
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Initialize rate limiter
rate_limiter = RateLimiter(
    requests_per_minute=config.get("api.rate_limit", 60)
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.get("api.allowed_origins", ["http://localhost:3000"]),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

# Add metrics middleware
app.add_middleware(MetricsMiddleware)

# Add security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """Add security headers to responses"""
    response = await call_next(request)
    
    # Add security headers
    for header, value in SecurityHeaders.get_secure_headers().items():
        response.headers[header] = value
        
    return response

# Add rate limiting middleware
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    """Apply rate limiting to all requests"""
    try:
        # Skip rate limiting for certain paths
        if request.url.path in ["/api/docs", "/api/redoc", "/api/openapi.json"]:
            return await call_next(request)
            
        await rate_limiter.check_rate_limit(request)
        return await call_next(request)
    except RateLimitExceededError:
        return JSONResponse(
            status_code=429,
            content={"detail": "Too many requests. Please try again later."}
        )

# Add request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests and responses"""
    start_time = time.time()
    
    # Generate a request ID
    request_id = request.headers.get("X-Request-ID", f"req_{int(start_time)}")
    
    # Log the request
    logger.info(
        f"Request started",
        extra={
            "request_id": request_id,
            "method": request.method,
            "url": str(request.url),
            "client": request.client.host
        }
    )
    
    try:
        # Process the request
        response = await call_next(request)
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Add processing time header
        response.headers["X-Process-Time"] = str(process_time)
        response.headers["X-Request-ID"] = request_id
        
        # Log the response
        logger.info(
            f"Request completed",
            extra={
                "request_id": request_id,
                "status_code": response.status_code,
                "process_time": process_time
            }
        )
        
        return response
    except Exception as e:
        # Log the error
        logger.error(
            f"Request failed: {str(e)}",
            extra={
                "request_id": request_id,
                "exception": str(e),
                "traceback": traceback.format_exc()
            }
        )
        
        # Return a 500 response
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )

# Exception handler for security errors
@app.exception_handler(SecurityError)
async def security_exception_handler(request: Request, exc: SecurityError):
    """Handle security-related exceptions"""
    if isinstance(exc, RateLimitExceededError):
        status_code = 429
    else:
        status_code = 401
        
    return JSONResponse(
        status_code=status_code,
        content={"detail": str(exc)}
    )

# Health check endpoint
@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    # Get system health status from monitoring
    health_status = monitoring.get_system_health()
    
    return {
        "status": "ok" if health_status["status"] == "healthy" else "degraded",
        "version": config.get("app.version"),
        "timestamp": time.time(),
        "health": health_status
    }

# Metrics endpoint
@app.get("/api/metrics")
def get_metrics(current_user = Depends(get_current_user)):
    """Get system metrics"""
    return {
        "system": monitoring.system_metrics.__dict__,
        "api": {
            "total_requests": monitoring.api_metrics.total_requests,
            "successful_requests": monitoring.api_metrics.successful_requests,
            "failed_requests": monitoring.api_metrics.failed_requests,
            "average_response_time": monitoring.api_metrics.average_response_time,
            "success_rate": monitoring.api_metrics.success_rate
        },
        "agents": {
            "total_executions": monitoring.agent_metrics.total_executions,
            "successful_executions": monitoring.agent_metrics.successful_executions,
            "failed_executions": monitoring.agent_metrics.failed_executions,
            "average_execution_time": monitoring.agent_metrics.average_execution_time,
            "success_rate": monitoring.agent_metrics.success_rate
        }
    }

# Example protected endpoint
@app.get("/api/me")
def read_users_me(current_user = Depends(get_current_user)):
    """Get current user information"""
    return current_user

# Add API routers
from backend.routers import users, agents, chains, memory

app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(agents.router, prefix="/api/agents", tags=["agents"])
app.include_router(chains.router, prefix="/api/chains", tags=["chains"])
app.include_router(memory.router, prefix="/api/memory", tags=["memory"])

# API entrypoint
@app.get("/api")
def api_root():
    """API root endpoint"""
    return {
        "name": config.get("app.name"),
        "version": config.get("app.version"),
        "description": config.get("app.description")
    }

# Legacy status endpoint
@app.get("/api/status")
def status():
    """Legacy status endpoint"""
    return {"status": "Ultimate Sankalpa API is running!"}

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize the application on startup"""
    monitoring.start()
    logger.info("API started")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    monitoring.stop()
    logger.info("API shutdown")


# Main entrypoint
if __name__ == "__main__":
    host = config.get("api.host", "0.0.0.0")
    port = int(config.get("api.port", 9000))  # Using port 9000 for backend API
    debug = config.get("api.debug", False)
    
    logger.info(f"Starting API server on {host}:{port}")

    if os.environ.get("SANKALPA_RELOAD", "").lower() == "true":
        # Development mode with auto-reload
        import uvicorn
        uvicorn.run(
            "backend.enhanced_main:app",  # Updated import path
            host=host,
            port=port,
            reload=True,
            ws="none"  # Disable WebSockets
        )
    else:
        # Production mode
        import uvicorn
        # Try alternative ports if default is busy
        for port in [port, port+1, port+2, port+3]:
            try:
                uvicorn.run(
                    app,
                    host=host,
                    port=port,
                    ws="none"  # Disable WebSockets
                )
                break
            except OSError as e:
                if "address already in use" in str(e):
                    logger.warning(f"Port {port} in use, trying next available...")
                    continue
                raise
