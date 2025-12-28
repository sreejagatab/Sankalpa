"""
Performance tests for memory manager
"""

import pytest
import os
import sys
import time
import json
import statistics
import random
import string

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from sankalpa.memory.enhanced_memory_manager import EnhancedMemoryManager

# Skip these tests if the performance tests are not enabled
pytestmark = pytest.mark.skipif(
    not os.environ.get("RUN_PERFORMANCE_TESTS"),
    reason="Performance tests are only run when RUN_PERFORMANCE_TESTS environment variable is set"
)

def generate_random_string(length):
    """Generate a random string of the specified length"""
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

def measure_operation_time(func, *args, **kwargs):
    """Measure the time taken to execute a function"""
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    return end_time - start_time, result

def test_memory_save_performance():
    """Test the performance of saving data to memory"""
    memory = EnhancedMemoryManager()
    
    # Test with different data sizes
    data_sizes = [10, 100, 1000, 10000, 100000]
    results = {}
    
    for size in data_sizes:
        # Create data of the specified size
        test_data = generate_random_string(size)
        
        # Measure save performance (multiple times)
        times = []
        for i in range(10):
            key = f"perf_test_{size}_{i}"
            time_taken, _ = measure_operation_time(memory.save, key, test_data)
            times.append(time_taken)
        
        # Calculate statistics
        results[size] = {
            "avg": statistics.mean(times),
            "min": min(times),
            "max": max(times),
            "p95": sorted(times)[int(len(times) * 0.95)],
            "samples": len(times)
        }
    
    # Print results
    print("\nMemory Save Performance:")
    for size, stats in results.items():
        print(f"Data Size: {size} bytes")
        print(f"  Stats: {stats}")
    
    # Check that performance doesn't degrade too much with larger data
    assert results[100000]["avg"] < 0.1  # Even large data should save quickly

def test_memory_load_performance():
    """Test the performance of loading data from memory"""
    memory = EnhancedMemoryManager()
    
    # Test with different data sizes
    data_sizes = [10, 100, 1000, 10000, 100000]
    results = {}
    
    for size in data_sizes:
        # Create and save data of the specified size
        test_data = generate_random_string(size)
        key = f"perf_test_load_{size}"
        memory.save(key, test_data)
        
        # Measure load performance (multiple times)
        times = []
        for _ in range(50):
            time_taken, _ = measure_operation_time(memory.load, key)
            times.append(time_taken)
        
        # Calculate statistics
        results[size] = {
            "avg": statistics.mean(times),
            "min": min(times),
            "max": max(times),
            "p95": sorted(times)[int(len(times) * 0.95)],
            "samples": len(times)
        }
    
    # Print results
    print("\nMemory Load Performance:")
    for size, stats in results.items():
        print(f"Data Size: {size} bytes")
        print(f"  Stats: {stats}")
    
    # Check that performance doesn't degrade too much with larger data
    assert results[100000]["avg"] < 0.01  # Even large data should load quickly

def test_memory_transaction_performance():
    """Test the performance of memory transactions"""
    memory = EnhancedMemoryManager()
    
    # Test with different numbers of operations
    operation_counts = [10, 100, 1000]
    results = {}
    
    for count in operation_counts:
        # Measure transaction performance
        times = []
        for _ in range(5):
            # Define a transaction with the specified number of operations
            def run_transaction():
                with memory.transaction() as tx:
                    for i in range(count):
                        tx.save(f"tx_test_{i}", f"value_{i}")
            
            time_taken, _ = measure_operation_time(run_transaction)
            times.append(time_taken)
        
        # Calculate statistics
        results[count] = {
            "avg": statistics.mean(times),
            "min": min(times),
            "max": max(times),
            "p95": sorted(times)[int(len(times) * 0.95)],
            "samples": len(times)
        }
    
    # Print results
    print("\nMemory Transaction Performance:")
    for count, stats in results.items():
        print(f"Operation Count: {count}")
        print(f"  Stats: {stats}")
    
    # Check that performance scales reasonably
    assert results[1000]["avg"] < 1.0  # Even large transactions should be quick

def test_memory_concurrent_access():
    """Test the performance of concurrent memory access"""
    memory = EnhancedMemoryManager()
    
    # Test with different numbers of concurrent operations
    from concurrent.futures import ThreadPoolExecutor
    
    concurrent_counts = [5, 10, 20]
    results = {}
    
    for count in concurrent_counts:
        # Define the operation to perform
        def perform_operation(_):
            key = f"concurrent_test_{random.randint(1, 100)}"
            value = generate_random_string(100)
            memory.save(key, value)
            return memory.load(key)
        
        # Measure concurrent performance
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=count) as executor:
            futures = [executor.submit(perform_operation, i) for i in range(100)]
            results_list = [future.result() for future in futures]
        
        end_time = time.time()
        total_time = end_time - start_time
        
        results[count] = {
            "total_time": total_time,
            "operations_per_second": 100 / total_time
        }
    
    # Print results
    print("\nMemory Concurrent Access Performance:")
    for count, stats in results.items():
        print(f"Concurrent Count: {count}")
        print(f"  Total Time: {stats['total_time']:.4f} seconds")
        print(f"  Operations/Second: {stats['operations_per_second']:.2f}")
    
    # Check that performance scales reasonably
    assert results[20]["operations_per_second"] > 50  # Should handle at least 50 ops/sec

def test_memory_session_switching():
    """Test the performance of switching between memory sessions"""
    memory = EnhancedMemoryManager()
    
    # Create multiple sessions
    session_count = 10
    sessions = [f"perf_session_{i}" for i in range(session_count)]
    
    # Initialize each session with some data
    for session in sessions:
        memory.switch_session(session)
        for i in range(10):
            memory.save(f"key_{i}", f"value_{i}")
    
    # Measure session switching performance
    times = []
    for _ in range(50):
        session = random.choice(sessions)
        time_taken, _ = measure_operation_time(memory.switch_session, session)
        times.append(time_taken)
    
    # Calculate statistics
    stats = {
        "avg": statistics.mean(times),
        "min": min(times),
        "max": max(times),
        "p95": sorted(times)[int(len(times) * 0.95)],
        "samples": len(times)
    }
    
    # Print results
    print("\nMemory Session Switching Performance:")
    print(f"Stats: {stats}")
    
    # Check that session switching is quick
    assert stats["avg"] < 0.01  # Session switching should be very fast
