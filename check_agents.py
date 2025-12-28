import requests
import json

response = requests.get('http://localhost:8080/api/agents')
agents = response.json()["agents"]

print(f'Available agents: {len(agents)}')
print("First 5 agents:")
for agent in agents[:5]:
    print(f"- {agent['name']}: {agent['description']}")