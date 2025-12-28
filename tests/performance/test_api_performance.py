"""
Performance tests for API endpoints
"""

import pytest
import os
import sys
import time
import json
import requests
import statistics
from concurrent.futures import ThreadPoolExecutor

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Skip these tests if the performance tests are not enabled
pytestmark = pytest.mark.skipif(
    not os.environ.get("RUN_PERFORMANCE_TESTS"),
    reason="Performance tests are only run when RUN_PERFORMANCE_TESTS environment variable is set"
)

@pytest.fixture(scope="module")
def api_url():
    """Get the API URL"""
    return "http://localhost:8000"

@pytest.fixture(scope="module")
def app_server():
    """Start the application server for testing"""
    import subprocess
    import time
    
    # Start the backend server
    backend_process = subprocess.Popen(
        ["python", "run_sankalpa.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for the server to start
    time.sleep(5)
    
    yield
    
    # Clean up
    backend_process.terminate()
    backend_process.wait()

def measure_response_time(url, method="get", json_data=None, num_requests=10):
    """Measure the response time for a given URL"""
    response_times = []
    
    for _ in range(num_requests):
        start_time = time.time()
        
        if method.lower() == "get":
            response = requests.get(url)
        elif method.lower() == "post":
            response = requests.post(url, json=json_data)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        end_time = time.time()
        response_time = end_time - start_time
        
        # Only include successful responses
        if response.status_code == 200:
            response_times.append(response_time)
        
        # Add a small delay between requests
        time.sleep(0.1)
    
    if not response_times:
        return None
    
    # Calculate statistics
    avg_time = statistics.mean(response_times)
    min_time = min(response_times)
    max_time = max(response_times)
    p95_time = sorted(response_times)[int(len(response_times) * 0.95)]
    
    return {
        "avg": avg_time,
        "min": min_time,
        "max": max_time,
        "p95": p95_time,
        "samples": len(response_times)
    }

def test_api_status_performance(api_url, app_server):
    """Test the performance of the API status endpoint"""
    url = f"{api_url}/api/status"
    stats = measure_response_time(url, num_requests=50)
    
    assert stats is not None
    assert stats["avg"] < 0.5  # Average response time should be less than 500ms
    assert stats["p95"] < 1.0  # 95th percentile should be less than 1 second
    
    print(f"\nAPI Status Performance: {stats}")

def test_agents_list_performance(api_url, app_server):
    """Test the performance of the agents list endpoint"""
    url = f"{api_url}/api/agents"
    stats = measure_response_time(url, num_requests=20)
    
    assert stats is not None
    assert stats["avg"] < 1.0  # Average response time should be less than 1 second
    assert stats["p95"] < 2.0  # 95th percentile should be less than 2 seconds
    
    print(f"\nAgents List Performance: {stats}")

def test_memory_performance(api_url, app_server):
    """Test the performance of memory operations"""
    # Test saving to memory
    save_url = f"{api_url}/api/memory/perf_test_key"
    save_stats = measure_response_time(
        save_url,
        method="post",
        json_data={"value": "performance_test"},
        num_requests=20
    )
    
    assert save_stats is not None
    assert save_stats["avg"] < 0.5  # Average response time should be less than 500ms
    
    # Test retrieving from memory
    get_url = f"{api_url}/api/memory/perf_test_key"
    get_stats = measure_response_time(get_url, num_requests=20)
    
    assert get_stats is not None
    assert get_stats["avg"] < 0.5  # Average response time should be less than 500ms
    
    print(f"\nMemory Save Performance: {save_stats}")
    print(f"Memory Get Performance: {get_stats}")

def test_concurrent_requests(api_url, app_server):
    """Test the performance under concurrent requests"""
    url = f"{api_url}/api/status"
    num_concurrent = 10
    num_requests_per_thread = 10
    
    def make_requests():
        times = []
        for _ in range(num_requests_per_thread):
            start_time = time.time()
            response = requests.get(url)
            end_time = time.time()
            
            if response.status_code == 200:
                times.append(end_time - start_time)
            
            time.sleep(0.1)
        
        return times
    
    # Execute concurrent requests
    with ThreadPoolExecutor(max_workers=num_concurrent) as executor:
        results = list(executor.map(lambda _: make_requests(), range(num_concurrent)))
    
    # Flatten the results
    all_times = [time for thread_times in results for time in thread_times]
    
    # Calculate statistics
    stats = {
        "avg": statistics.mean(all_times),
        "min": min(all_times),
        "max": max(all_times),
        "p95": sorted(all_times)[int(len(all_times) * 0.95)],
        "samples": len(all_times)
    }
    
    assert stats["avg"] < 1.0  # Average response time should be less than 1 second
    assert stats["p95"] < 2.0  # 95th percentile should be less than 2 seconds
    
    print(f"\nConcurrent Requests Performance: {stats}")

def test_agent_execution_performance(api_url, app_server):
    """Test the performance of agent execution"""
    # First, get the list of agents
    response = requests.get(f"{api_url}/api/agents")
    assert response.status_code == 200
    data = response.json()
    
    # Get the first agent
    if data["agents"]:
        agent_id = data["agents"][0]["id"]
        
        # Test agent execution performance
        url = f"{api_url}/api/agents/execute/{agent_id}"
        stats = measure_response_time(
            url,
            method="post",
            json_data={"input": "Performance test input"},
            num_requests=5  # Fewer requests as this is more resource-intensive
        )
        
        assert stats is not None
        # Agent execution can take longer, so we allow more time
        assert stats["avg"] < 5.0  # Average response time should be less than 5 seconds
        
        print(f"\nAgent Execution Performance: {stats}")

def test_memory_scaling(api_url, app_server):
    """Test memory performance with increasing data size"""
    base_url = f"{api_url}/api/memory/scaling_test"
    
    # Test with different data sizes
    data_sizes = [10, 100, 1000, 10000]
    results = {}
    
    for size in data_sizes:
        # Create data of the specified size
        test_data = {
            "value": "x" * size,
            "size": size
        }
        
        # Measure save performance
        save_stats = measure_response_time(
            base_url,
            method="post",
            json_data=test_data,
            num_requests=5
        )
        
        # Measure get performance
        get_stats = measure_response_time(base_url, num_requests=5)
        
        results[size] = {
            "save": save_stats,
            "get": get_stats
        }
    
    # Print results
    print("\nMemory Scaling Performance:")
    for size, stats in results.items():
        print(f"Data Size: {size} bytes")
        print(f"  Save: {stats['save']}")
        print(f"  Get: {stats['get']}")
    
    # Check that performance doesn't degrade too much with larger data
    assert results[10000]["save"]["avg"] < 1.0  # Even large data should save quickly
    assert results[10000]["get"]["avg"] < 1.0  # Even large data should retrieve quickly
