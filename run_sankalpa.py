#!/usr/bin/env python3
"""
Sankalpa Full System Runner
---------------------------
This script launches the complete Sankalpa system with all enhanced components:
1. Backend API server with all enhanced agents
2. Frontend with React Flow-based workflow composer
3. Websocket connections for real-time collaboration
4. Memory persistence system
5. Enhanced agent execution framework

This integrated system represents the complete vision of Sankalpa as a
multi-agent AI platform for autonomous software development.
"""

import os
import sys
import json
import time
import signal
import subprocess
import threading
import webbrowser
from datetime import datetime

# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Terminal colors for better output
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
RESET = "\033[0m"
BOLD = "\033[1m"

# Process holders
processes = {}
stop_event = threading.Event()

# Configuration
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
API_PORT = 9000  # Changed to higher port to avoid conflicts
FRONTEND_PORT = 9001  # Changed to higher port to avoid conflicts
AUTO_OPEN_BROWSER = False

# Print with timestamps and colors
def log(message, color=RESET):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{color}[{timestamp}] {message}{RESET}")

def section(title):
    """Print a section header"""
    separator = "=" * 80
    print(f"\n{CYAN}{separator}")
    print(f" {title} ".center(80, "="))
    print(f"{separator}{RESET}\n")

def print_banner():
    """Print Sankalpa banner"""
    banner = """
    ███████╗ █████╗ ███╗   ██╗██╗  ██╗ █████╗ ██╗     ██████╗  █████╗ 
    ██╔════╝██╔══██╗████╗  ██║██║ ██╔╝██╔══██╗██║     ██╔══██╗██╔══██╗
    ███████╗███████║██╔██╗ ██║█████╔╝ ███████║██║     ██████╔╝███████║
    ╚════██║██╔══██║██║╚██╗██║██╔═██╗ ██╔══██║██║     ██╔═══╝ ██╔══██║
    ███████║██║  ██║██║ ╚████║██║  ██╗██║  ██║███████╗██║     ██║  ██║
    ╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝  ╚═╝
    """
    print(f"{CYAN}{banner}{RESET}")
    print(f"{BOLD}Multi-Agent AI Platform for Autonomous Software Development{RESET}")
    print(f"{BOLD}=========================================================={RESET}")
    print(f"{MAGENTA}API Server: http://localhost:{API_PORT}{RESET}")
    print(f"{MAGENTA}Frontend:   http://localhost:{FRONTEND_PORT}{RESET}")
    print(f"{BOLD}=========================================================={RESET}\n")

# Make sure the required directories exist
def setup_directories():
    """Create required directories if they don't exist"""
    required_dirs = [
        os.path.join(ROOT_DIR, "agents", "custom"),
        os.path.join(ROOT_DIR, "memory", "sessions"),
        os.path.join(ROOT_DIR, "fine_tuning", "data"),
        os.path.join(ROOT_DIR, "catalog"),
        os.path.join(ROOT_DIR, "logs")
    ]
    
    for dir_path in required_dirs:
        os.makedirs(dir_path, exist_ok=True)
        log(f"Created directory: {dir_path}", BLUE)
    
    # Initialize catalog file if it doesn't exist
    catalog_path = os.path.join(ROOT_DIR, "catalog", "agent_catalog.json")
    if not os.path.exists(catalog_path):
        with open(catalog_path, "w") as f:
            json.dump({}, f, indent=2)
        log(f"Created agent catalog at {catalog_path}", BLUE)

# Start the enhanced backend server
def start_enhanced_api_server():
    """Start the enhanced backend API server with all capabilities"""
    log("Starting enhanced backend API server...", GREEN)
    
    # Determine Python executable
    python_exec = sys.executable
    
    # Command to run the enhanced backend
    cmd = [python_exec, "backend/enhanced_main.py"]
    env = os.environ.copy()
    env["SANKALPA_LOG_LEVEL"] = "INFO"
    
    log(f"Running command: {' '.join(cmd)}", BLUE)
    
    # Start the process
    try:
        process = subprocess.Popen(
            cmd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Store the process
        processes["backend"] = process
        
        # Start threads to read output
        def read_output(stream, prefix, color):
            for line in iter(stream.readline, ''):
                if stop_event.is_set():
                    break
                log(f"{prefix} {line.rstrip()}", color)
        
        threading.Thread(target=read_output, args=(process.stdout, "[BACKEND]", BLUE), daemon=True).start()
        threading.Thread(target=read_output, args=(process.stderr, "[BACKEND ERR]", RED), daemon=True).start()
        
        log(f"Backend API server started with PID {process.pid}", GREEN)
        return True
    except Exception as e:
        log(f"Failed to start backend server: {str(e)}", RED)
        return False

# Start the frontend server
def start_frontend_server():
    """Start the frontend development server with the React Flow workflow composer"""
    log("Starting frontend server...", GREEN)
    
    # Check if frontend directory exists
    if not os.path.isdir(os.path.join(ROOT_DIR, "frontend")):
        log("Frontend directory not found!", RED)
        return False
    
    # Start the frontend server
    try:
        # Command to run the frontend
        cmd = ["npm", "run", "dev"]
        env = os.environ.copy()
        env["PORT"] = str(FRONTEND_PORT)
        
        log(f"Running command: {' '.join(cmd)} in frontend directory", BLUE)
        
        process = subprocess.Popen(
            cmd,
            cwd=os.path.join(ROOT_DIR, "frontend"),
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Store the process
        processes["frontend"] = process
        
        # Start threads to read output
        def read_output(stream, prefix, color):
            for line in iter(stream.readline, ''):
                if stop_event.is_set():
                    break
                log(f"{prefix} {line.rstrip()}", color)
        
        threading.Thread(target=read_output, args=(process.stdout, "[FRONTEND]", GREEN), daemon=True).start()
        threading.Thread(target=read_output, args=(process.stderr, "[FRONTEND ERR]", RED), daemon=True).start()
        
        log(f"Frontend server started with PID {process.pid}", GREEN)
        return True
    except Exception as e:
        log(f"Failed to start frontend server: {str(e)}", RED)
        return False

# Check if the API server is running
def check_api_server():
    """Check if the API server is responding"""
    import requests
    try:
        response = requests.get(f"http://localhost:{API_PORT}/api/status", timeout=5)
        if response.status_code == 200:
            log("API server is responding", GREEN)
            return True
    except Exception:
        pass
    
    log("API server is not responding", YELLOW)
    return False

# Check if the frontend server is running
def check_frontend_server():
    """Check if the frontend server is responding"""
    import requests
    try:
        response = requests.get(f"http://localhost:{FRONTEND_PORT}", timeout=5)
        if response.status_code == 200:
            log("Frontend server is responding", GREEN)
            return True
    except Exception:
        pass
    
    log("Frontend server is not responding", YELLOW)
    return False

# Initialize the system components
def initialize_system():
    """Initialize and verify system components"""
    section("SYSTEM INITIALIZATION")
    
    log("Checking Python dependencies...", YELLOW)
    
    # Check for required Python packages
    required_packages = ["fastapi", "uvicorn", "pydantic"]
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            log(f"✓ {package} is installed", GREEN)
        except ImportError:
            missing_packages.append(package)
            log(f"✗ {package} is not installed", RED)
    
    if missing_packages:
        log(f"Installing missing packages: {', '.join(missing_packages)}", YELLOW)
        subprocess.run([sys.executable, "-m", "pip", "install", *missing_packages])
    
    # Check for Node.js dependencies
    frontend_dir = os.path.join(ROOT_DIR, "frontend")
    if os.path.isdir(frontend_dir):
        log("Checking frontend dependencies...", YELLOW)
        
        if not os.path.isdir(os.path.join(frontend_dir, "node_modules")):
            log("Frontend dependencies not installed, running npm install...", YELLOW)
            subprocess.run(["npm", "install"], cwd=frontend_dir)
        else:
            log("✓ Frontend dependencies found", GREEN)
    
    # Create required directories
    setup_directories()
    
    # Initialize memory system
    log("Initializing memory system...", YELLOW)
    try:
        from memory.enhanced_memory_manager import EnhancedMemoryManager
        memory = EnhancedMemoryManager()
        log("✓ Memory system initialized", GREEN)
    except Exception as e:
        log(f"✗ Failed to initialize memory system: {str(e)}", RED)
    
    # Check for the enhanced agents
    log("Checking for enhanced agents...", YELLOW)
    
    # Try to import the enhanced agents
    enhanced_agents = {
        "finetuner": "agents.enhanced.finetuner_agent",
        "self_replicator": "agents.enhanced.self_replicator_agent",
        "vs_code_extension": "agents.enhanced.vs_code_extension_agent",
        "deploy_executor": "agents.deployment.deploy_executor_agent"
    }
    
    for agent_name, module_path in enhanced_agents.items():
        try:
            __import__(module_path)
            log(f"✓ {agent_name} agent is available", GREEN)
        except Exception as e:
            log(f"✗ {agent_name} agent is not available: {str(e)}", RED)
    
    return True

# Handle signals for graceful shutdown
def signal_handler(sig, frame):
    """Handle signals for graceful shutdown"""
    log("Shutting down Sankalpa...", YELLOW)
    stop_event.set()
    
    # Terminate all processes
    for name, process in processes.items():
        log(f"Terminating {name} process...", YELLOW)
        try:
            process.terminate()
            # Wait a bit for graceful termination
            time.sleep(1)
            # Force kill if still running
            if process.poll() is None:
                process.kill()
        except Exception as e:
            log(f"Error terminating {name} process: {str(e)}", RED)
    
    log("Sankalpa shutdown complete", GREEN)
    sys.exit(0)

# Open the browser to the workflow composer
def open_browser():
    """Open the browser to the workflow composer"""
    time.sleep(5)  # Wait for servers to start
    log("Opening browser to workflow composer...", GREEN)
    webbrowser.open(f"http://localhost:{FRONTEND_PORT}/composer")

# Monitor processes and keep the script running
def monitor_processes():
    """Monitor processes and keep the script running"""
    while not stop_event.is_set():
        # Check if any process has terminated
        for name, process in list(processes.items()):
            if process.poll() is not None:
                exit_code = process.poll()
                if exit_code != 0:
                    log(f"{name} process exited with code {exit_code}", RED)
                else:
                    log(f"{name} process exited normally", YELLOW)
                
                # Remove from process list
                del processes[name]
        
        # Exit if all processes have terminated
        if not processes:
            log("All processes have terminated", YELLOW)
            return
        
        # Sleep to avoid high CPU usage
        time.sleep(1)

# Main function
def main():
    """Main function to run the complete Sankalpa system"""
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Print banner
    print_banner()
    
    # Initialize the system
    if not initialize_system():
        log("System initialization failed", RED)
        return 1
    
    # Start the backend server
    if not start_enhanced_api_server():
        log("Failed to start backend server", RED)
        return 1
    
    # Wait a bit for the backend to start
    time.sleep(3)
    
    # Check if API server is running
    for _ in range(3):  # Try a few times
        if check_api_server():
            break
        log("Waiting for API server to start...", YELLOW)
        time.sleep(2)
    else:
        log("API server did not start successfully", RED)
    
    # Start the frontend server
    if not start_frontend_server():
        log("Failed to start frontend server", RED)
        log("Backend is still running", YELLOW)
    
    # Wait a bit for the frontend to start
    time.sleep(3)
    
    # Check if frontend server is running
    for _ in range(3):  # Try a few times
        if check_frontend_server():
            break
        log("Waiting for frontend server to start...", YELLOW)
        time.sleep(2)
    else:
        log("Frontend server did not start successfully", RED)
    
    # Open browser if both servers are running
    if check_api_server() and check_frontend_server() and AUTO_OPEN_BROWSER:
        threading.Thread(target=open_browser, daemon=True).start()
    
    section("SANKALPA IS RUNNING")
    log("Sankalpa is now running with all enhanced capabilities!", GREEN)
    log("Access the workflow composer at:", MAGENTA)
    log(f"http://localhost:{FRONTEND_PORT}/composer", BOLD)
    log("\nPress Ctrl+C to stop all services", YELLOW)
    
    # Monitor processes
    monitor_processes()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())