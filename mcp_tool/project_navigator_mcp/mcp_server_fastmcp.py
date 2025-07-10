#!/usr/bin/env python3
"""
Fast MCP Server for Project Navigator
使用FastMCP库避免TaskGroup错误
"""

import sys
import requests
import os
from datetime import date
from mcp.server.fastmcp import FastMCP
from typing import Dict, Any, List

# 设置代理绕过
os.environ['no_proxy'] = '127.0.0.1,localhost'

# 服务器配置
API_BASE_URL = "http://127.0.0.1:8000"

# 创建FastMCP服务器
mcp = FastMCP("project-navigator")

@mcp.tool()
def add_project(
    name: str,
    project_type: str,
    maturity: str,
    status: str,
    description: str,
    readme_path: str = "",
    source_url: str = ""
) -> str:
    """添加新的项目记录到导航系统中
    
    Args:
        name: 项目名称
        project_type: 项目类型 (工具类, 分析类, AI应用, Web服务, 框架类, 理论类)
        maturity: 构想成熟度 (🟢 高, 🟡 中, 🔴 低)
        status: 项目状态 (✅ 完成, 🔍 研究中, 📋 规划中, 📚 已归档)
        description: 项目描述
        readme_path: README文件路径（可选，会自动生成）
        source_url: 引用原文URL（可选）
    """
    # 如果没有提供readme_path，自动生成
    if not readme_path:
        project_slug = name.lower().replace(" ", "-")
        readme_path = f"ideaed-projects/{project_slug}/README.md"
    
    # 准备项目数据
    project_data = {
        "name": name,
        "project_type": project_type,
        "maturity": maturity,
        "status": status,
        "description": description,
        "readme_path": readme_path,
        "source_url": source_url if source_url else None,
        "created_date": date.today().isoformat()
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/api/projects", json=project_data)
        response.raise_for_status()
        
        result = response.json()
        return f"✅ 项目创建成功！\n\n项目ID: {result.get('id')}\n项目名称: {name}\n项目类型: {project_type}\n成熟度: {maturity}\n状态: {status}\nREADME路径: {readme_path}\n创建日期: {project_data['created_date']}"
    except requests.exceptions.RequestException as e:
        return f"❌ 创建项目失败: {str(e)}"

@mcp.tool()
def list_projects(
    filter_type: str = "",
    filter_maturity: str = "",
    filter_status: str = ""
) -> str:
    """列出所有项目记录
    
    Args:
        filter_type: 按类型筛选（可选）
        filter_maturity: 按成熟度筛选（可选）
        filter_status: 按状态筛选（可选）
    """
    try:
        params = {}
        if filter_type:
            params["type"] = filter_type
        if filter_maturity:
            params["maturity"] = filter_maturity
        if filter_status:
            params["status"] = filter_status
            
        response = requests.get(f"{API_BASE_URL}/api/projects", params=params)
        response.raise_for_status()
        
        projects = response.json()
        
        if not projects:
            return "📋 没有找到符合条件的项目"
        
        # 格式化项目列表
        result = "📋 **项目列表**\n\n"
        for project in projects:
            result += f"**{project['id']}. {project['name']}**\n"
            result += f"   类型: {project['project_type']} | "
            result += f"成熟度: {project['maturity']} | "
            result += f"状态: {project['status']}\n"
            result += f"   描述: {project['description'][:100]}{'...' if len(project['description']) > 100 else ''}\n"
            result += f"   创建: {project['created_date']}\n\n"
        
        return result
    except requests.exceptions.RequestException as e:
        return f"❌ 获取项目列表失败: {str(e)}"

@mcp.tool()
def search_projects(query: str) -> str:
    """搜索项目记录
    
    Args:
        query: 搜索关键词
    """
    try:
        response = requests.get(f"{API_BASE_URL}/api/projects")
        response.raise_for_status()
        
        projects = response.json()
        query_lower = query.lower()
        
        # 简单的关键词搜索
        filtered_projects = []
        for project in projects:
            if (query_lower in project["name"].lower() or 
                query_lower in project["description"].lower() or
                query_lower in project["project_type"].lower()):
                filtered_projects.append(project)
        
        if not filtered_projects:
            return f"🔍 没有找到包含 '{query}' 的项目"
        
        result = f"🔍 **搜索结果 (关键词: {query})**\n\n"
        for project in filtered_projects:
            result += f"**{project['id']}. {project['name']}**\n"
            result += f"   类型: {project['project_type']} | "
            result += f"成熟度: {project['maturity']} | "
            result += f"状态: {project['status']}\n"
            result += f"   描述: {project['description'][:100]}{'...' if len(project['description']) > 100 else ''}\n\n"
        
        return result
    except requests.exceptions.RequestException as e:
        return f"❌ 搜索失败: {str(e)}"

@mcp.tool()
def get_project(project_id: int) -> str:
    """获取特定项目的详细信息
    
    Args:
        project_id: 项目ID
    """
    try:
        response = requests.get(f"{API_BASE_URL}/api/projects/{project_id}")
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
        
        return result
    except requests.exceptions.RequestException as e:
        if "404" in str(e):
            return f"❌ 项目 ID {project_id} 不存在"
        return f"❌ 获取项目详情失败: {str(e)}"

@mcp.tool()
def update_project_status(project_id: int, new_status: str) -> str:
    """更新项目状态
    
    Args:
        project_id: 项目ID
        new_status: 新状态 (✅ 完成, 🔍 研究中, 📋 规划中, 📚 已归档)
    """
    try:
        # 先获取项目信息
        get_response = requests.get(f"{API_BASE_URL}/api/projects/{project_id}")
        get_response.raise_for_status()
        project = get_response.json()
        
        # 更新状态
        project["status"] = new_status
        
        update_response = requests.put(
            f"{API_BASE_URL}/api/projects/{project_id}", 
            json=project
        )
        update_response.raise_for_status()
        
        return f"✅ 项目状态更新成功！\n\n项目: {project['name']}\n新状态: {new_status}"
    except requests.exceptions.RequestException as e:
        if "404" in str(e):
            return f"❌ 项目 ID {project_id} 不存在"
        return f"❌ 更新项目状态失败: {str(e)}"

@mcp.resource("project://navigator/summary")
def get_projects_summary() -> str:
    """获取项目导航系统的总体统计信息"""
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

def main():
    """主函数"""
    # 检查API服务器连接
    try:
        response = requests.get(f"{API_BASE_URL}/api/projects", timeout=5)
        response.raise_for_status()
        print(f"✅ 成功连接到API服务器: {API_BASE_URL}", file=sys.stderr)
    except Exception as e:
        print(f"⚠️  警告: 无法连接到API服务器 ({API_BASE_URL}): {e}", file=sys.stderr)
        print("请确保navigator服务器正在运行: uvicorn navigator.app.main:app --reload --port 8000", file=sys.stderr)
    
    # 启动FastMCP服务器
    print("🚀 启动FastMCP服务器...", file=sys.stderr)
    mcp.run()

if __name__ == "__main__":
    main()