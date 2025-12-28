#!/usr/bin/env python3
import requests
import json
import time

API_BASE = "http://localhost:8080"

def test_endpoint(url, description):
    print(f"\n=== Testing {description} ===")
    try:
        response = requests.get(url, timeout=3)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def main():
    print("Testing Sankalpa Minimal API Server")
    
    # Test basic endpoints
    test_endpoint(f"{API_BASE}/", "Root endpoint")
    test_endpoint(f"{API_BASE}/api/status", "Status endpoint")
    test_endpoint(f"{API_BASE}/api/agents", "Agents list")
    test_endpoint(f"{API_BASE}/api/memory", "Memory contents")
    
    # Test project architect agent
    print("\n=== Testing project_architect agent ===")
    try:
        response = requests.post(
            f"{API_BASE}/api/agents/execute/project_architect",
            json={"project": "test_api_project"},
            timeout=5
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {str(e)}")
    
    # Test self-replicator agent to create a new agent
    print("\n=== Testing self-replicator to create new agent ===")
    try:
        # Define a text processor agent
        agent_spec = {
            "name": "text_processor",
            "description": "A text processing agent that capitalizes, reverses, or counts words in text",
            "category": "utility",
            "logic": '''
                text = input_data.get("text", "")
                operation = input_data.get("operation", "capitalize")
                
                if not text:
                    return {"error": "No text provided", "status": "error"}
                    
                result = {}
                
                if operation == "capitalize":
                    result["processed_text"] = text.upper()
                elif operation == "reverse":
                    result["processed_text"] = text[::-1]
                elif operation == "word_count":
                    result["processed_text"] = str(len(text.split()))
                else:
                    return {"error": f"Unknown operation: {operation}", "status": "error"}
                    
                return result
            ''',
            "inputs": [
                {"name": "text", "type": "string"},
                {"name": "operation", "type": "string"}
            ],
            "outputs": [
                {"name": "processed_text", "type": "string"}
            ]
        }
        
        response = requests.post(
            f"{API_BASE}/api/create-agent",
            json=agent_spec,
            timeout=10
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        # If successful, test the new agent
        if response.status_code == 200:
            print("\n=== Testing newly created text_processor agent ===")
            # Wait a moment for the agent to be available
            time.sleep(2)
            
            test_response = requests.post(
                f"{API_BASE}/api/agents/execute/text_processor",
                json={"text": "Hello Sankalpa!", "operation": "capitalize"},
                timeout=5
            )
            print(f"Status: {test_response.status_code}")
            print(f"Response: {json.dumps(test_response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {str(e)}")
    
    print("\nAPI testing complete!")

if __name__ == "__main__":
    main()