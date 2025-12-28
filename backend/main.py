
import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from backend.routers import agents, chains, memory, users
from backend.websockets import websocket_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add routers
app.include_router(agents.router, prefix="/api")
app.include_router(chains.router, prefix="/api")
app.include_router(memory.router, prefix="/api")
app.include_router(users.router, prefix="/api")

# Add WebSocket router
app.include_router(websocket_router)

@app.get("/api/status")
def status():
    return {"status": "Ultimate Sankalpa API is running!"}