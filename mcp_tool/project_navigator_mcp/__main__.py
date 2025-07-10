#!/usr/bin/env python3
"""
Entry point for running Project Navigator MCP Server as a module.
This allows the package to be executed with: python -m project_navigator_mcp
"""

import sys
from .mcp_server import main_sync

if __name__ == "__main__":
    main_sync() 