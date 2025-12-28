import requests
import json

def test_endpoint(url, description):
    print(f"\n=== Testing {description} ===")
    try:
        response = requests.get(url)
        print(f"Status code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

API_BASE = "http://localhost:8080"

# Test endpoints
test_endpoint(f"{API_BASE}/api/status", "Status endpoint")
test_endpoint(f"{API_BASE}/api/agents", "Agents list endpoint")
test_endpoint(f"{API_BASE}/api/memory", "Memory endpoint")

# Test creating a calculation agent
print("\n=== Testing agent creation ===")
try:
    agent_data = {
        "name": "calculator",
        "description": "A simple calculator agent",
        "category": "utility",
        "logic": """
            operation = input_data.get("operation", "add")
            num1 = input_data.get("num1", 0)
            num2 = input_data.get("num2", 0)
            
            result = {}
            
            if operation == "add":
                result["answer"] = num1 + num2
            elif operation == "subtract":
                result["answer"] = num1 - num2
            elif operation == "multiply":
                result["answer"] = num1 * num2
            elif operation == "divide":
                if num2 == 0:
                    return {"error": "Cannot divide by zero"}
                result["answer"] = num1 / num2
            else:
                return {"error": f"Unknown operation: {operation}"}
            
            return result
        """,
        "inputs": [
            {"name": "operation", "type": "string"},
            {"name": "num1", "type": "number"},
            {"name": "num2", "type": "number"}
        ],
        "outputs": [
            {"name": "answer", "type": "number"}
        ]
    }
    
    response = requests.post(f"{API_BASE}/api/create-agent", json=agent_data)
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test the calculator agent
    if response.status_code == 200:
        print("\n=== Testing calculator agent ===")
        calc_data = {
            "operation": "add",
            "num1": 5,
            "num2": 3
        }
        
        calc_response = requests.post(f"{API_BASE}/api/agents/execute/calculator", json=calc_data)
        print(f"Status code: {calc_response.status_code}")
        print(f"Response: {json.dumps(calc_response.json(), indent=2)}")
        
except Exception as e:
    print(f"Error: {str(e)}")

print("\nAPI Testing Complete!")