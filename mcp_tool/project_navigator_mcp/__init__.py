"""
Project Navigator MCP Server

Model Context Protocol (MCP) server for Project Navigator system.
Provides AI agents with tools to manage and interact with project data.
"""

__version__ = "1.0.0"
__author__ = "TRAE AI"
__email__ = "ai@trae.com"

from .mcp_server import main, main_sync
from .mcp_server_fastmcp import main as main_fastmcp

__all__ = ["main", "main_sync", "main_fastmcp"] 