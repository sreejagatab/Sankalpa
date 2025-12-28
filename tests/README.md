# Sankalpa Project Test Suite

This directory contains a comprehensive test suite for the Sankalpa project, covering all aspects of the application including backend, frontend, integration, performance, and security.

## Test Structure

The test suite is organized into the following directories:

- `unit/`: Unit tests for individual components
- `integration/`: Integration tests for component interactions
- `frontend/`: Tests for frontend components and pages
- `e2e/`: End-to-end tests for full application workflows
- `performance/`: Performance tests for API and memory operations
- `security/`: Security tests for authentication and input validation

## Running Tests

### Running All Tests

To run the entire test suite, use the comprehensive test runner:

```bash
python tests/comprehensive_test_suite.py
```

### Running Specific Test Categories

To run specific categories of tests, use pytest with the appropriate directory:

```bash
# Run unit tests
pytest tests/unit

# Run integration tests
pytest tests/integration

# Run frontend tests
cd frontend && npm test

# Run end-to-end tests
export RUN_E2E_TESTS=1
pytest tests/e2e

# Run performance tests
export RUN_PERFORMANCE_TESTS=1
pytest tests/performance

# Run security tests
export RUN_SECURITY_TESTS=1
pytest tests/security
```

## Test Configuration

### Environment Variables

The following environment variables can be used to configure the tests:

- `RUN_E2E_TESTS`: Set to `1` to enable end-to-end tests
- `RUN_PERFORMANCE_TESTS`: Set to `1` to enable performance tests
- `RUN_SECURITY_TESTS`: Set to `1` to enable security tests

### Test Fixtures

Common test fixtures are defined in `conftest.py` and include:

- `test_client`: A FastAPI TestClient for API testing
- `test_memory`: A memory manager for testing
- `mock_agents`: Mock agent implementations for testing
- `mock_token_header`: Mock authorization headers for testing

## Adding New Tests

When adding new tests, follow these guidelines:

1. Place the test in the appropriate directory based on its type
2. Use the existing fixtures where possible
3. Follow the naming convention: `test_*.py` for files and `test_*` for functions
4. Add appropriate docstrings to describe the test purpose
5. Use assertions to verify expected behavior

## Test Coverage

The test suite aims to provide comprehensive coverage of the Sankalpa project, including:

- Backend API endpoints
- Frontend components and pages
- WebSocket functionality
- Memory management
- Agent execution
- Chain execution
- Authentication and authorization
- Input validation and security

## Continuous Integration

The test suite is integrated with the CI/CD pipeline and runs automatically on each pull request and merge to the main branch.

## Troubleshooting

If you encounter issues running the tests, check the following:

1. Ensure all dependencies are installed: `pip install -r requirements-dev.txt`
2. Make sure the application server is running for end-to-end tests
3. Check that the appropriate environment variables are set
4. Verify that the test database is properly configured
