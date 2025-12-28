#!/usr/bin/env python3
"""
Check the status of all Sankalpa components
"""

import os
import sys
import json
import requests
from datetime import datetime

def print_header(title):
    print("\n" + "=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80)

def check_api_server():
    print_header("API Server Status")
    try:
        # Check the status endpoint
        response = requests.get("http://localhost:8080/api/status", timeout=3)
        if response.status_code == 200:
            print(f"✅ API server is running")
            print(f"Status: {response.json()}")
            return True
        else:
            print(f"❌ API server returned status code {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Failed to connect to API server: {str(e)}")
        return False

def check_frontend_server():
    print_header("Frontend Server Status")
    try:
        response = requests.get("http://localhost:3003/", timeout=3)
        if response.status_code == 200:
            print(f"✅ Frontend server is running")
            print(f"Response length: {len(response.text)} bytes")
            return True
        else:
            print(f"⚠️ Frontend server returned status code {response.status_code}")
            print(f"Response length: {len(response.text)} bytes")
            return False
    except Exception as e:
        print(f"❌ Failed to connect to frontend server: {str(e)}")
        return False

def check_agents():
    print_header("Available Agents")
    try:
        response = requests.get("http://localhost:8080/api/agents", timeout=3)
        if response.status_code == 200:
            agents = response.json()["agents"]
            print(f"✅ Found {len(agents)} agents")
            for agent in agents:
                print(f"- {agent['name']}: {agent['description']}")
            return True
        else:
            print(f"❌ Failed to get agents: Status code {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Failed to get agents: {str(e)}")
        return False

def check_agent_execution():
    print_header("Agent Execution Test")
    try:
        # Try to execute project_architect agent
        data = {"project": "test_project"}
        response = requests.post(
            "http://localhost:8080/api/agents/execute/project_architect", 
            json=data,
            timeout=5
        )
        
        if response.status_code == 200:
            print(f"✅ Successfully executed project_architect agent")
            print(f"Result: {json.dumps(response.json()['result'], indent=2)}")
            return True
        else:
            print(f"❌ Failed to execute agent: Status code {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Failed to execute agent: {str(e)}")
        return False

def main():
    print(f"Sankalpa System Check - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python version: {sys.version}")
    print(f"Current directory: {os.getcwd()}")
    
    api_ok = check_api_server()
    frontend_ok = check_frontend_server()
    agents_ok = check_agents()
    execution_ok = check_agent_execution()
    
    print_header("System Status Summary")
    print(f"API Server:       {'✅ Running' if api_ok else '❌ Not running'}")
    print(f"Frontend Server:  {'✅ Running' if frontend_ok else '❌ Not running'}")
    print(f"Agents Available: {'✅ Yes' if agents_ok else '❌ No'}")
    print(f"Agent Execution:  {'✅ Working' if execution_ok else '❌ Not working'}")
    
    if api_ok and agents_ok and execution_ok:
        print("\n✅ Core functionality is working correctly!")
        
        if not frontend_ok:
            print("⚠️ The frontend server is not running correctly, but the backend API is functional.")
            print("   You can use the API directly or try fixing the frontend server.")
    else:
        print("\n❌ Some components are not working correctly.")
        print("   Please check the issues and try to fix them.")

if __name__ == "__main__":
    main()