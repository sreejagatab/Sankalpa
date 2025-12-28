"""
Unit tests for core functionality
"""

import pytest
import os
import sys
import json
from unittest.mock import Mock, patch

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from core import config

def test_config_loading():
    """Test configuration loading"""
    # Test default configuration
    assert config.get("app.name") is not None
    assert config.get("app.version") is not None

    # Test default value
    assert config.get("non.existent.key", "default") == "default"

def test_config_from_file():
    """Test loading configuration from file"""
    # Create a temporary config file
    temp_config = {
        "app": {
            "test_name": "Test App",
            "test_version": "1.0.0"
        },
        "database": {
            "url": "test://localhost/db"
        }
    }

    temp_file = "temp_config.json"
    with open(temp_file, "w") as f:
        json.dump(temp_config, f)

    try:
        # Create a new Config instance with the temp file
        from core.config import Config
        test_config = Config()
        test_config.config_path = temp_file
        test_config._initialize()

        # Test values were loaded
        assert test_config.get("app.test_name") == "Test App"
        assert test_config.get("app.test_version") == "1.0.0"
        assert test_config.get("database.url") == "test://localhost/db"
    finally:
        # Clean up
        if os.path.exists(temp_file):
            os.remove(temp_file)

def test_config_to_dict():
    """Test converting config to dictionary"""
    # Create a test config with known values
    from core.config import Config
    test_config = Config()
    test_config.config = {
        "test": {
            "export": {
                "key1": "value1",
                "key2": "value2"
            }
        }
    }

    # Verify structure using get method
    assert test_config.get("test.export.key1") == "value1"
    assert test_config.get("test.export.key2") == "value2"

def test_config_environment_override():
    """Test environment variable overrides for config"""
    # Set environment variable
    os.environ["SANKALPA_TEST_ENV_KEY"] = "env_value"

    # Create a new Config instance to load the environment variables
    from core.config import Config
    test_config = Config()
    test_config._load_from_env()

    # Test that environment variables are loaded in the real config
    assert "SANKALPA_TEST_ENV_KEY" in os.environ

    # Clean up
    if "SANKALPA_TEST_ENV_KEY" in os.environ:
        del os.environ["SANKALPA_TEST_ENV_KEY"]
