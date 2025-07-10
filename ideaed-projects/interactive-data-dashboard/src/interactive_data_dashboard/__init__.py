"""Interactive Data Dashboard Package

A Streamlit-based interactive data visualization dashboard that combines
Pandas for data processing and Plotly for creating interactive charts.

This package provides:
- Data loading and processing utilities
- Interactive chart generation
- Streamlit-based web interface
- Configurable dashboard components

Example:
    >>> from interactive_data_dashboard import main
    >>> main.main()  # Launch the dashboard

Author: Interactive Data Dashboard Team
License: MIT
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "petrelpost"
__email__ = "chg_g@msn.com"
__license__ = "MIT"
__description__ = "Interactive data visualization dashboard built with Streamlit, Pandas, and Plotly"

# Package metadata
__all__ = [
    "main",
    "DataProcessor", 
    "ChartGenerator",
    "__version__",
    "__author__",
    "__email__",
    "__license__",
    "__description__"
]

# Import main components for easy access
try:
    from .main import DataProcessor, ChartGenerator
except ImportError:
    # Handle case where dependencies might not be installed
    pass

# Version info tuple
version_info = tuple(map(int, __version__.split('.')))

# Package configuration
CONFIG = {
    'name': 'interactive-data-dashboard',
    'version': __version__,
    'description': __description__,
    'author': __author__,
    'license': __license__,
    'python_requires': '>=3.8',
    'keywords': ['streamlit', 'pandas', 'plotly', 'dashboard', 'visualization'],
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Data Scientists',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
}

def get_version() -> str:
    """Get the current version of the package.
    
    Returns:
        str: The version string
    """
    return __version__

def get_info() -> dict:
    """Get package information.
    
    Returns:
        dict: Package metadata
    """
    return CONFIG.copy()