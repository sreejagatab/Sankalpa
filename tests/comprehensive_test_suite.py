"""
Comprehensive Test Suite for Sankalpa Project

This module orchestrates the execution of all tests in the Sankalpa project,
providing a single entry point for running the entire test suite.
"""

import os
import sys
import unittest
import pytest
import time
import json
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def run_all_tests():
    """Run all tests in the project"""
    start_time = time.time()
    
    # Run pytest for all test files
    print("=" * 80)
    print("Running all tests for Sankalpa project")
    print("=" * 80)
    
    # Run unit tests
    print("\n\nRunning Unit Tests...")
    pytest.main(['-xvs', 'tests/unit'])
    
    # Run integration tests
    print("\n\nRunning Integration Tests...")
    pytest.main(['-xvs', 'tests/integration'])
    
    # Run frontend tests
    print("\n\nRunning Frontend Tests...")
    pytest.main(['-xvs', 'tests/frontend'])
    
    # Run end-to-end tests
    print("\n\nRunning End-to-End Tests...")
    pytest.main(['-xvs', 'tests/e2e'])
    
    # Run performance tests
    print("\n\nRunning Performance Tests...")
    pytest.main(['-xvs', 'tests/performance'])
    
    # Run security tests
    print("\n\nRunning Security Tests...")
    pytest.main(['-xvs', 'tests/security'])
    
    # Calculate and display execution time
    execution_time = time.time() - start_time
    print("\n" + "=" * 80)
    print(f"All tests completed in {execution_time:.2f} seconds")
    print("=" * 80)

def generate_test_report():
    """Generate a comprehensive test report"""
    # Implementation for generating test reports
    pass

if __name__ == "__main__":
    run_all_tests()
