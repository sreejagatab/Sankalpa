import requests
import json
import sys

# URL for the test server
BASE_URL = "http://localhost:8080"

def create_agent():
    """Test creating a new agent with the self-replicator"""
    url = f"{BASE_URL}/api/create-agent"
    
    # Agent definition
    data = {
        "name": "custom_calculator",
        "description": "A simple calculator agent that performs arithmetic operations",
        "category": "utility",
        "logic": '''result = {}

        # Get operation type
        operation = input_data.get("operation", "add")
        num1 = input_data.get("num1", 0)
        num2 = input_data.get("num2", 0)
        
        # Perform the calculation
        if operation == "add":
            result["calculation"] = num1 + num2
        elif operation == "subtract":
            result["calculation"] = num1 - num2
        elif operation == "multiply":
            result["calculation"] = num1 * num2
        elif operation == "divide":
            if num2 == 0:
                return {"error": "Cannot divide by zero", "status": "error"}
            result["calculation"] = num1 / num2
        else:
            return {"error": f"Unknown operation: {operation}", "status": "error"}''',
        "inputs": [
            {"name": "operation", "type": "string"},
            {"name": "num1", "type": "number"},
            {"name": "num2", "type": "number"}
        ],
        "outputs": [
            {"name": "calculation", "type": "number"}
        ]
    }
    
    # Make the request
    response = requests.post(url, json=data)
    
    print(f"Status Code: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    
    return response.json()

def test_calculator():
    """Test the newly created calculator agent"""
    url = f"{BASE_URL}/api/agents/execute/custom_calculator"
    
    # Test data for addition
    data = {
        "operation": "add",
        "num1": 5,
        "num2": 3
    }
    
    # Make the request
    response = requests.post(url, json=data)
    
    print(f"Status Code: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    
    return response.json()

if __name__ == "__main__":
    # Check if the server is running
    try:
        status_response = requests.get(f"{BASE_URL}/api/status")
        print(f"Server status: {status_response.json()}")
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to the server. Make sure it's running on http://localhost:8080")
        sys.exit(1)
    
    # Create the calculator agent
    print("\n=== Creating Calculator Agent ===")
    create_result = create_agent()
    
    # Test the calculator agent
    print("\n=== Testing Calculator Agent ===")
    test_result = test_calculator()