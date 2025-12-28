import uvicorn
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Set up some debugging to understand imports
print(f"Python path: {sys.path}")
print(f"Current directory: {os.getcwd()}")

try:
    # Try to import the minimal server which has fewer dependencies
    from backend.minimal_server import app
    print("Successfully imported minimal_server")
except Exception as e:
    print(f"Error importing minimal_server: {str(e)}")
    sys.exit(1)

if __name__ == "__main__":
    # Run the minimal server
    uvicorn.run("backend.minimal_server:app", host="0.0.0.0", port=8080, reload=True)