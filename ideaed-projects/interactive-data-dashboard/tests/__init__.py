"""Test package for Interactive Data Dashboard.

This package contains all test modules for the Interactive Data Dashboard project.
It includes unit tests, integration tests, and performance tests.

Test Structure:
- test_main.py: Tests for main application components
- test_data_processing.py: Tests for data processing utilities
- test_chart_generation.py: Tests for chart generation
- test_ui_components.py: Tests for UI components
- test_integration.py: Integration tests
- test_performance.py: Performance and load tests

Usage:
    Run all tests:
    $ pytest tests/
    
    Run specific test file:
    $ pytest tests/test_main.py
    
    Run with coverage:
    $ pytest tests/ --cov=interactive_data_dashboard
    
    Run with verbose output:
    $ pytest tests/ -v

Test Configuration:
    Tests use pytest framework with the following plugins:
    - pytest-cov: For coverage reporting
    - pytest-mock: For mocking
    - pytest-xdist: For parallel test execution
    - pytest-benchmark: For performance testing

Test Data:
    Test fixtures and sample data are located in the fixtures/ directory.
    Mock data is generated programmatically in test setup methods.

Author: petrelpost
License: MIT
"""

__version__ = "1.0.0"
__author__ = "petrelpost"

# Test configuration
TEST_CONFIG = {
    'test_data_size': 1000,
    'performance_threshold_seconds': 5.0,
    'memory_threshold_mb': 100,
    'coverage_threshold': 80,
    'test_timeout_seconds': 30
}

# Test utilities
def get_test_config():
    """Get test configuration.
    
    Returns:
        dict: Test configuration settings
    """
    return TEST_CONFIG.copy()

def setup_test_environment():
    """Set up test environment with necessary configurations."""
    import os
    import sys
    from pathlib import Path
    
    # Add src directory to Python path
    project_root = Path(__file__).parent.parent
    src_path = project_root / 'src'
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))
    
    # Set test environment variables
    os.environ['TESTING'] = 'true'
    os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
    os.environ['STREAMLIT_SERVER_PORT'] = '8501'
    
    return True

def teardown_test_environment():
    """Clean up test environment."""
    import os
    
    # Remove test environment variables
    test_vars = ['TESTING', 'STREAMLIT_SERVER_HEADLESS', 'STREAMLIT_SERVER_PORT']
    for var in test_vars:
        if var in os.environ:
            del os.environ[var]
    
    return True

# Automatically set up test environment when module is imported
setup_test_environment()