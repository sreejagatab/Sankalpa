#!/bin/bash
# Start script for Sankalpa

echo "Starting Sankalpa..."
echo "Activating virtual environment..."
source venv/bin/activate

# Check if the API server is already running
if lsof -i:8080 > /dev/null; then
    echo "API server is already running on port 8080"
else
    echo "Starting API server..."
    python minimal_api_server.py > api_server.log 2>&1 &
    echo $! > api_server.pid
    echo "API server started with PID $(cat api_server.pid)"
fi

# Check if the frontend server is already running
if lsof -i:3003 > /dev/null; then
    echo "Frontend server is already running on port 3003"
else
    echo "Starting frontend server..."
    node server.js > frontend_server.log 2>&1 &
    echo $! > frontend_server.pid
    echo "Frontend server started with PID $(cat frontend_server.pid)"
fi

echo "Waiting for servers to start..."
sleep 3

echo "Running system check..."
python check_all.py

echo "Sankalpa has been started."
echo "API Server: http://localhost:8080"
echo "Frontend Server: http://localhost:3003"
echo ""
echo "To interact with Sankalpa, use:"
echo "- API Endpoints: http://localhost:8080/api/..."
echo "- Frontend: http://localhost:3003/"
echo "- Simple CLI: python simple_run.py"