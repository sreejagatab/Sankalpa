import requests

try:
    response = requests.get('http://localhost:3003/', timeout=3)
    print(f'Frontend Server status: {response.status_code}')
    print(f'Content length: {len(response.text)} bytes')
except Exception as e:
    print(f'Error: {str(e)}')