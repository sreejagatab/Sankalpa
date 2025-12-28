#!/usr/bin/env python
"""
Test runner script for Sankalpa project

This script provides a command-line interface for running the Sankalpa test suite.
"""

import os
import sys
import argparse
import subprocess
import time

def run_command(command, cwd=None):
    """Run a command and return the result"""
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        cwd=cwd
    )
    stdout, stderr = process.communicate()
    return process.returncode, stdout.decode(), stderr.decode()

def run_unit_tests(verbose=False):
    """Run unit tests"""
    print("\n" + "=" * 80)
    print("Running Unit Tests")
    print("=" * 80)
    
    command = "pytest tests/unit"
    if verbose:
        command += " -v"
    
    returncode, stdout, stderr = run_command(command)
    print(stdout)
    if stderr:
        print(stderr)
    
    return returncode == 0

def run_integration_tests(verbose=False):
    """Run integration tests"""
    print("\n" + "=" * 80)
    print("Running Integration Tests")
    print("=" * 80)
    
    command = "pytest tests/integration"
    if verbose:
        command += " -v"
    
    returncode, stdout, stderr = run_command(command)
    print(stdout)
    if stderr:
        print(stderr)
    
    return returncode == 0

def run_frontend_tests(verbose=False):
    """Run frontend tests"""
    print("\n" + "=" * 80)
    print("Running Frontend Tests")
    print("=" * 80)
    
    # Check if Node.js is installed
    returncode, _, _ = run_command("node --version")
    if returncode != 0:
        print("Node.js is not installed. Skipping frontend tests.")
        return True
    
    # Check if the frontend directory has a package.json
    if not os.path.exists("frontend/package.json"):
        print("No package.json found in frontend directory. Skipping frontend tests.")
        return True
    
    # Run the tests
    command = "npm test"
    if verbose:
        command += " -- --verbose"
    
    returncode, stdout, stderr = run_command(command, cwd="frontend")
    print(stdout)
    if stderr:
        print(stderr)
    
    return returncode == 0

def run_e2e_tests(verbose=False):
    """Run end-to-end tests"""
    print("\n" + "=" * 80)
    print("Running End-to-End Tests")
    print("=" * 80)
    
    # Set the environment variable
    os.environ["RUN_E2E_TESTS"] = "1"
    
    command = "pytest tests/e2e"
    if verbose:
        command += " -v"
    
    returncode, stdout, stderr = run_command(command)
    print(stdout)
    if stderr:
        print(stderr)
    
    # Clean up
    if "RUN_E2E_TESTS" in os.environ:
        del os.environ["RUN_E2E_TESTS"]
    
    return returncode == 0

def run_performance_tests(verbose=False):
    """Run performance tests"""
    print("\n" + "=" * 80)
    print("Running Performance Tests")
    print("=" * 80)
    
    # Set the environment variable
    os.environ["RUN_PERFORMANCE_TESTS"] = "1"
    
    command = "pytest tests/performance"
    if verbose:
        command += " -v"
    
    returncode, stdout, stderr = run_command(command)
    print(stdout)
    if stderr:
        print(stderr)
    
    # Clean up
    if "RUN_PERFORMANCE_TESTS" in os.environ:
        del os.environ["RUN_PERFORMANCE_TESTS"]
    
    return returncode == 0

def run_security_tests(verbose=False):
    """Run security tests"""
    print("\n" + "=" * 80)
    print("Running Security Tests")
    print("=" * 80)
    
    # Set the environment variable
    os.environ["RUN_SECURITY_TESTS"] = "1"
    
    command = "pytest tests/security"
    if verbose:
        command += " -v"
    
    returncode, stdout, stderr = run_command(command)
    print(stdout)
    if stderr:
        print(stderr)
    
    # Clean up
    if "RUN_SECURITY_TESTS" in os.environ:
        del os.environ["RUN_SECURITY_TESTS"]
    
    return returncode == 0

def run_all_tests(verbose=False):
    """Run all tests"""
    start_time = time.time()
    
    results = {}
    
    # Run each test category
    results["unit"] = run_unit_tests(verbose)
    results["integration"] = run_integration_tests(verbose)
    results["frontend"] = run_frontend_tests(verbose)
    results["e2e"] = run_e2e_tests(verbose)
    results["performance"] = run_performance_tests(verbose)
    results["security"] = run_security_tests(verbose)
    
    # Calculate execution time
    execution_time = time.time() - start_time
    
    # Print summary
    print("\n" + "=" * 80)
    print("Test Summary")
    print("=" * 80)
    
    for category, success in results.items():
        status = "PASSED" if success else "FAILED"
        print(f"{category.upper()} Tests: {status}")
    
    print("-" * 80)
    print(f"Total Execution Time: {execution_time:.2f} seconds")
    print("=" * 80)
    
    # Return True if all tests passed, False otherwise
    return all(results.values())

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Run Sankalpa tests")
    parser.add_argument("--unit", action="store_true", help="Run unit tests")
    parser.add_argument("--integration", action="store_true", help="Run integration tests")
    parser.add_argument("--frontend", action="store_true", help="Run frontend tests")
    parser.add_argument("--e2e", action="store_true", help="Run end-to-end tests")
    parser.add_argument("--performance", action="store_true", help="Run performance tests")
    parser.add_argument("--security", action="store_true", help="Run security tests")
    parser.add_argument("--all", action="store_true", help="Run all tests")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    # If no specific test category is specified, run all tests
    if not any([args.unit, args.integration, args.frontend, args.e2e, args.performance, args.security, args.all]):
        args.all = True
    
    success = True
    
    if args.all:
        success = run_all_tests(args.verbose)
    else:
        if args.unit:
            success = success and run_unit_tests(args.verbose)
        
        if args.integration:
            success = success and run_integration_tests(args.verbose)
        
        if args.frontend:
            success = success and run_frontend_tests(args.verbose)
        
        if args.e2e:
            success = success and run_e2e_tests(args.verbose)
        
        if args.performance:
            success = success and run_performance_tests(args.verbose)
        
        if args.security:
            success = success and run_security_tests(args.verbose)
    
    # Exit with appropriate status code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
