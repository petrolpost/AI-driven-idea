#!/usr/bin/env python3
"""
简单的MCP服务器测试
"""

import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

app = Server("test-server")

@app.list_tools()
async def list_tools():
    return []

@app.list_resources()
async def list_resources():
    return []

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream)

if __name__ == "__main__":
    asyncio.run(main()) 