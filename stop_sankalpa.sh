#!/bin/bash
# Stop script for Sankalpa

echo "Stopping Sankalpa..."

# Stop API server
if [ -f api_server.pid ]; then
    PID=$(cat api_server.pid)
    if ps -p $PID > /dev/null; then
        echo "Stopping API server (PID: $PID)..."
        kill -9 $PID
        rm api_server.pid
    else
        echo "API server not running"
        rm api_server.pid
    fi
else
    echo "API server PID file not found"
fi

# Stop frontend server
if [ -f frontend_server.pid ]; then
    PID=$(cat frontend_server.pid)
    if ps -p $PID > /dev/null; then
        echo "Stopping frontend server (PID: $PID)..."
        kill -9 $PID
        rm frontend_server.pid
    else
        echo "Frontend server not running"
        rm frontend_server.pid
    fi
else
    echo "Frontend server PID file not found"
fi

# Check if any processes are still using the ports
echo "Checking if ports are still in use..."
API_PORT=$(lsof -i:8080 | grep LISTEN | awk '{print $2}')
if [ ! -z "$API_PORT" ]; then
    echo "Port 8080 is still in use by PID $API_PORT. Stopping it..."
    kill -9 $API_PORT
fi

FRONTEND_PORT=$(lsof -i:3003 | grep LISTEN | awk '{print $2}')
if [ ! -z "$FRONTEND_PORT" ]; then
    echo "Port 3003 is still in use by PID $FRONTEND_PORT. Stopping it..."
    kill -9 $FRONTEND_PORT
fi

echo "Sankalpa has been stopped."