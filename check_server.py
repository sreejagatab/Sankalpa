import requests

def check_server(url):
    try:
        resp = requests.get(url, timeout=5)
        print(f"Server at {url} - Status: {resp.status_code}")
        print(f"Headers: {resp.headers}")
        print(f"First 100 chars of content: {resp.text[:100]}...")
        return True
    except Exception as e:
        print(f"Server at {url} - Error: {str(e)}")
        return False

# Check frontend server
print("Checking frontend server...")
frontend_running = check_server("http://localhost:3003/")

# Check backend server
print("\nChecking backend server...")
backend_running = check_server("http://localhost:8080/")

print("\nSummary:")
print(f"Frontend server running: {frontend_running}")
print(f"Backend server running: {backend_running}")