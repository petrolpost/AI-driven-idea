#!/usr/bin/env python3
"""
MCP Server for Project Navigator
符合 Anthropic Model Context Protocol 标准的项目导航工具
"""

import asyncio
import json
import sys
from typing import Any, Dict, List, Optional
from dataclasses import asdict

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)

import requests
import os
from datetime import date

# 设置代理绕过
os.environ['no_proxy'] = '127.0.0.1,localhost'

# 服务器配置
API_BASE_URL = "http://127.0.0.1:8000"
SERVER_NAME = "project-navigator"
SERVER_VERSION = "1.0.0"

app = Server(SERVER_NAME)

@app.list_tools()
async def handle_list_tools() -> List[Tool]:
    """列出所有可用的工具"""
    return [
        Tool(
            name="add_project",
            description="添加新的项目记录到导航系统中",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "项目名称"
                    },
                    "project_type": {
                        "type": "string",
                        "description": "项目类型",
                        "enum": ["工具类", "分析类", "AI应用", "Web服务", "框架类", "理论类"]
                    },
                    "maturity": {
                        "type": "string",
                        "description": "构想成熟度",
                        "enum": ["🟢 高", "🟡 中", "🔴 低"]
                    },
                    "status": {
                        "type": "string",
                        "description": "项目状态",
                        "enum": ["✅ 完成", "🔍 研究中", "📋 规划中", "📚 已归档"]
                    },
                    "description": {
                        "type": "string",
                        "description": "项目描述"
                    },
                    "readme_path": {
                        "type": "string",
                        "description": "README文件路径（可选，会自动生成）",
                        "default": ""
                    }
                },
                "required": ["name", "project_type", "maturity", "status", "description"]
            }
        ),
        Tool(
            name="list_projects",
            description="列出所有项目记录",
            inputSchema={
                "type": "object",
                "properties": {
                    "filter_type": {
                        "type": "string",
                        "description": "按类型筛选（可选）",
                        "enum": ["工具类", "分析类", "AI应用", "Web服务", "框架类", "理论类"]
                    },
                    "filter_maturity": {
                        "type": "string",
                        "description": "按成熟度筛选（可选）",
                        "enum": ["🟢 高", "🟡 中", "🔴 低"]
                    },
                    "filter_status": {
                        "type": "string",
                        "description": "按状态筛选（可选）",
                        "enum": ["✅ 完成", "🔍 研究中", "📋 规划中", "📚 已归档"]
                    }
                }
            }
        ),
        Tool(
            name="search_projects",
            description="搜索项目记录",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜索关键词"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_project",
            description="获取特定项目的详细信息",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {
                        "type": "integer",
                        "description": "项目ID"
                    }
                },
                "required": ["project_id"]
            }
        ),
        Tool(
            name="update_project_status",
            description="更新项目状态",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {
                        "type": "integer", 
                        "description": "项目ID"
                    },
                    "new_status": {
                        "type": "string",
                        "description": "新状态",
                        "enum": ["✅ 完成", "🔍 研究中", "📋 规划中", "📚 已归档"]
                    }
                },
                "required": ["project_id", "new_status"]
            }
        )
    ]

@app.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """处理工具调用"""
    try:
        if name == "add_project":
            return await add_project(arguments)
        elif name == "list_projects":
            return await list_projects(arguments)
        elif name == "search_projects":
            return await search_projects(arguments)
        elif name == "get_project":
            return await get_project(arguments)
        elif name == "update_project_status":
            return await update_project_status(arguments)
        else:
            return [TextContent(type="text", text=f"未知工具: {name}")]
    except Exception as e:
        return [TextContent(type="text", text=f"执行工具 {name} 时出错: {str(e)}")]

async def add_project(args: Dict[str, Any]) -> List[TextContent]:
    """添加项目"""
    # 如果没有提供readme_path，自动生成
    if not args.get("readme_path"):
        project_slug = args["name"].lower().replace(" ", "-")
        args["readme_path"] = f"ideaed-projects/{project_slug}/README.md"
    
    # 添加创建日期
    args["created_date"] = date.today().isoformat()
    
    try:
        response = requests.post(f"{API_BASE_URL}/api/projects", json=args)
        response.raise_for_status()
        
        project_data = response.json()
        return [TextContent(
            type="text", 
            text=f"✅ 项目创建成功！\n\n"
                 f"项目ID: {project_data.get('id')}\n"
                 f"项目名称: {args['name']}\n"
                 f"项目类型: {args['project_type']}\n"
                 f"成熟度: {args['maturity']}\n"
                 f"状态: {args['status']}\n"
                 f"README路径: {args['readme_path']}\n"
                 f"创建日期: {args['created_date']}"
        )]
    except requests.exceptions.RequestException as e:
        return [TextContent(type="text", text=f"❌ 创建项目失败: {str(e)}")]

async def list_projects(args: Dict[str, Any]) -> List[TextContent]:
    """列出项目"""
    try:
        params = {}
        if args.get("filter_type"):
            params["type"] = args["filter_type"]
        if args.get("filter_maturity"):
            params["maturity"] = args["filter_maturity"]
        if args.get("filter_status"):
            params["status"] = args["filter_status"]
            
        response = requests.get(f"{API_BASE_URL}/api/projects", params=params)
        response.raise_for_status()
        
        projects = response.json()
        
        if not projects:
            return [TextContent(type="text", text="📋 没有找到符合条件的项目")]
        
        # 格式化项目列表
        result = "📋 **项目列表**\n\n"
        for project in projects:
            result += f"**{project['id']}. {project['name']}**\n"
            result += f"   类型: {project['project_type']} | "
            result += f"成熟度: {project['maturity']} | "
            result += f"状态: {project['status']}\n"
            result += f"   描述: {project['description'][:100]}{'...' if len(project['description']) > 100 else ''}\n"
            result += f"   创建: {project['created_date']}\n\n"
        
        return [TextContent(type="text", text=result)]
    except requests.exceptions.RequestException as e:
        return [TextContent(type="text", text=f"❌ 获取项目列表失败: {str(e)}")]

async def search_projects(args: Dict[str, Any]) -> List[TextContent]:
    """搜索项目"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/projects")
        response.raise_for_status()
        
        projects = response.json()
        query = args["query"].lower()
        
        # 简单的关键词搜索
        filtered_projects = []
        for project in projects:
            if (query in project["name"].lower() or 
                query in project["description"].lower() or
                query in project["project_type"].lower()):
                filtered_projects.append(project)
        
        if not filtered_projects:
            return [TextContent(type="text", text=f"🔍 没有找到包含 '{args['query']}' 的项目")]
        
        result = f"🔍 **搜索结果 (关键词: {args['query']})**\n\n"
        for project in filtered_projects:
            result += f"**{project['id']}. {project['name']}**\n"
            result += f"   类型: {project['project_type']} | "
            result += f"成熟度: {project['maturity']} | "
            result += f"状态: {project['status']}\n"
            result += f"   描述: {project['description'][:100]}{'...' if len(project['description']) > 100 else ''}\n\n"
        
        return [TextContent(type="text", text=result)]
    except requests.exceptions.RequestException as e:
        return [TextContent(type="text", text=f"❌ 搜索失败: {str(e)}")]

async def get_project(args: Dict[str, Any]) -> List[TextContent]:
    """获取项目详情"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/projects/{args['project_id']}")
        response.raise_for_status()
        
        project = response.json()
        
        result = f"📄 **项目详情**\n\n"
        result += f"**ID**: {project['id']}\n"
        result += f"**名称**: {project['name']}\n"
        result += f"**类型**: {project['project_type']}\n"
        result += f"**成熟度**: {project['maturity']}\n"
        result += f"**状态**: {project['status']}\n"
        result += f"**描述**: {project['description']}\n"
        result += f"**README路径**: {project['readme_path']}\n"
        result += f"**创建日期**: {project['created_date']}\n"
        
        return [TextContent(type="text", text=result)]
    except requests.exceptions.RequestException as e:
        if "404" in str(e):
            return [TextContent(type="text", text=f"❌ 项目 ID {args['project_id']} 不存在")]
        return [TextContent(type="text", text=f"❌ 获取项目详情失败: {str(e)}")]

async def update_project_status(args: Dict[str, Any]) -> List[TextContent]:
    """更新项目状态"""
    try:
        # 先获取项目信息
        get_response = requests.get(f"{API_BASE_URL}/api/projects/{args['project_id']}")
        get_response.raise_for_status()
        project = get_response.json()
        
        # 更新状态
        project["status"] = args["new_status"]
        
        update_response = requests.put(
            f"{API_BASE_URL}/api/projects/{args['project_id']}", 
            json=project
        )
        update_response.raise_for_status()
        
        return [TextContent(
            type="text", 
            text=f"✅ 项目状态更新成功！\n\n"
                 f"项目: {project['name']}\n"
                 f"新状态: {args['new_status']}"
        )]
    except requests.exceptions.RequestException as e:
        if "404" in str(e):
            return [TextContent(type="text", text=f"❌ 项目 ID {args['project_id']} 不存在")]
        return [TextContent(type="text", text=f"❌ 更新项目状态失败: {str(e)}")]

@app.list_resources()
async def handle_list_resources() -> List[Resource]:
    """列出可用资源"""
    return [
        Resource(
            uri="project://navigator/summary",
            name="项目导航概览",
            description="显示项目导航系统的总体统计信息",
            mimeType="text/plain"
        ),
        Resource(
            uri="project://navigator/config",
            name="系统配置",
            description="显示MCP服务器的配置信息",
            mimeType="application/json"
        )
    ]

@app.read_resource()
async def handle_read_resource(uri: str) -> str:
    """读取资源"""
    if uri == "project://navigator/summary":
        try:
            response = requests.get(f"{API_BASE_URL}/api/projects")
            response.raise_for_status()
            projects = response.json()
            
            # 统计信息
            total = len(projects)
            by_type = {}
            by_maturity = {}
            by_status = {}
            
            for project in projects:
                # 统计类型
                ptype = project['project_type']
                by_type[ptype] = by_type.get(ptype, 0) + 1
                
                # 统计成熟度
                maturity = project['maturity']
                by_maturity[maturity] = by_maturity.get(maturity, 0) + 1
                
                # 统计状态
                status = project['status']
                by_status[status] = by_status.get(status, 0) + 1
            
            summary = f"📊 项目导航系统概览\n\n"
            summary += f"总项目数: {total}\n\n"
            
            summary += "按类型分布:\n"
            for ptype, count in by_type.items():
                summary += f"  {ptype}: {count}\n"
            
            summary += "\n按成熟度分布:\n"
            for maturity, count in by_maturity.items():
                summary += f"  {maturity}: {count}\n"
            
            summary += "\n按状态分布:\n"
            for status, count in by_status.items():
                summary += f"  {status}: {count}\n"
            
            return summary
        except Exception as e:
            return f"❌ 获取概览信息失败: {str(e)}"
    
    elif uri == "project://navigator/config":
        config = {
            "server_name": SERVER_NAME,
            "server_version": SERVER_VERSION,
            "api_base_url": API_BASE_URL,
            "supported_tools": [
                "add_project",
                "list_projects", 
                "search_projects",
                "get_project",
                "update_project_status"
            ],
            "project_types": ["工具类", "分析类", "AI应用", "Web服务", "框架类", "理论类"],
            "maturity_levels": ["🟢 高", "🟡 中", "🔴 低"],
            "status_options": ["✅ 完成", "🔍 研究中", "📋 规划中", "📚 已归档"]
        }
        return json.dumps(config, ensure_ascii=False, indent=2)
    
    else:
        raise ValueError(f"未知资源: {uri}")

async def main():
    """主函数"""
    # 检查API服务器连接
    try:
        response = requests.get(f"{API_BASE_URL}/api/projects", timeout=5)
        response.raise_for_status()
        print(f"✅ 成功连接到API服务器: {API_BASE_URL}", file=sys.stderr)
    except Exception as e:
        print(f"⚠️  警告: 无法连接到API服务器 ({API_BASE_URL}): {e}", file=sys.stderr)
        print("请确保navigator服务器正在运行: uvicorn navigator.app.main:app --reload --port 8000", file=sys.stderr)
    
    # 启动MCP服务器
    try:
        async with stdio_server() as (read_stream, write_stream):
            await app.run(read_stream, write_stream, InitializationOptions())
    except Exception as e:
        print(f"❌ MCP服务器运行时错误: {e}", file=sys.stderr)
        raise

def main_sync():
    """同步入口点函数，用于setuptools entry points"""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 MCP服务器已停止", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"❌ 启动MCP服务器失败: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main_sync() 