#!/usr/bin/env python3
"""
Simple Sankalpa System Runner
---------------------------
This script launches a simplified version of the Sankalpa system for demonstration:
1. Backend API server with mocked enhanced agents
2. Frontend with React Flow-based workflow composer
"""

import os
import sys
import time
import signal
import subprocess
import threading
import webbrowser
from datetime import datetime

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
API_PORT = 9000
FRONTEND_PORT = 9001
AUTO_OPEN_BROWSER = False

# Print with timestamps and colors
def log(message, color=RESET):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{color}[{timestamp}] {message}{RESET}")

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
        os.path.join(ROOT_DIR, "logs")
    ]
    
    for dir_path in required_dirs:
        os.makedirs(dir_path, exist_ok=True)
        log(f"Created directory: {dir_path}", BLUE)

# Start the backend server
def start_api_server():
    """Start the simplified backend API server"""
    log("Starting simplified backend API server...", GREEN)
    
    # Determine Python executable
    python_exec = sys.executable
    
    # Command to run the backend
    cmd = [python_exec, "backend/simple_main.py"]
    env = os.environ.copy()
    env["API_PORT"] = str(API_PORT)
    
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
    """Start the frontend development server"""
    log("Starting frontend server...", GREEN)
    
    # Check if frontend directory exists
    if not os.path.isdir(os.path.join(ROOT_DIR, "frontend")):
        log("Frontend directory not found!", RED)
        return False
    
    # Start a simple HTTP server instead of next.js for demonstration
    cmd = [
        "npx", "http-server", "frontend/public", "-p", str(FRONTEND_PORT)
    ]
    env = os.environ.copy()
    
    log(f"Running command: {' '.join(cmd)}", BLUE)
    
    # Start the process
    try:
        process = subprocess.Popen(
            cmd,
            cwd=ROOT_DIR,
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
    time.sleep(3)  # Wait for servers to start
    log("Opening browser...", GREEN)
    webbrowser.open(f"http://localhost:{FRONTEND_PORT}/")

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
    """Main function to run the Sankalpa platform"""
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Print banner
    print_banner()
    
    # Setup directories
    setup_directories()
    
    # Start the backend server
    if not start_api_server():
        log("Failed to start backend server", RED)
        return 1
    
    # Wait a bit for the backend to start
    time.sleep(2)
    
    # Check if API server is running
    for _ in range(3):  # Try a few times
        if check_api_server():
            break
        log("Waiting for API server to start...", YELLOW)
        time.sleep(1)
    else:
        log("API server did not start successfully", RED)
    
    # Start the frontend server
    if not start_frontend_server():
        log("Failed to start frontend server", RED)
        log("Backend is still running", YELLOW)
    
    # Open browser if both servers are running
    if check_api_server() and AUTO_OPEN_BROWSER:
        threading.Thread(target=open_browser, daemon=True).start()
    
    log("Sankalpa is now running!", GREEN)
    log("Press Ctrl+C to stop all services", YELLOW)
    
    # Monitor processes
    monitor_processes()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())