#!/usr/bin/env python3
"""
手动测试项目导航工具
演示MCP服务器提供的功能
"""

import requests
import json
import os
from datetime import date

# 设置代理绕过
os.environ['no_proxy'] = '127.0.0.1,localhost'

API_BASE_URL = "http://127.0.0.1:8000"

def test_api_connection():
    """测试API连接"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/projects", timeout=5)
        response.raise_for_status()
        print("✅ API连接成功")
        return True
    except Exception as e:
        print(f"❌ API连接失败: {e}")
        return False

def add_project_demo():
    """演示添加项目"""
    print("\n📝 演示：添加新项目")
    
    project_data = {
        "name": "MCP项目导航工具",
        "project_type": "AI应用",
        "maturity": "🟢 高",
        "status": "✅ 完成",
        "description": "基于Anthropic Model Context Protocol标准的项目导航工具，允许AI Agent通过标准化接口管理项目记录",
        "readme_path": "mcp_tool/README.md",
        "created_date": date.today().isoformat()
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/api/projects", json=project_data)
        response.raise_for_status()
        result = response.json()
        print(f"✅ 项目创建成功! ID: {result.get('id')}")
        print(f"   名称: {project_data['name']}")
        print(f"   类型: {project_data['project_type']}")
        print(f"   成熟度: {project_data['maturity']}")
        print(f"   状态: {project_data['status']}")
        return result.get('id')
    except Exception as e:
        print(f"❌ 项目创建失败: {e}")
        return None

def list_projects_demo():
    """演示列出项目"""
    print("\n📋 演示：列出所有项目")
    
    try:
        response = requests.get(f"{API_BASE_URL}/api/projects")
        response.raise_for_status()
        projects = response.json()
        
        print(f"共找到 {len(projects)} 个项目:")
        for project in projects:
            print(f"  {project['id']}. {project['name']}")
            print(f"     类型: {project['project_type']} | 成熟度: {project['maturity']} | 状态: {project['status']}")
            print(f"     描述: {project['description'][:80]}...")
            print()
    except Exception as e:
        print(f"❌ 获取项目列表失败: {e}")

def search_projects_demo():
    """演示搜索项目"""
    print("\n🔍 演示：搜索AI相关项目")
    
    try:
        response = requests.get(f"{API_BASE_URL}/api/projects")
        response.raise_for_status()
        projects = response.json()
        
        # 搜索包含"AI"的项目
        ai_projects = [p for p in projects if "AI" in p["name"] or "AI" in p["description"]]
        
        print(f"找到 {len(ai_projects)} 个AI相关项目:")
        for project in ai_projects:
            print(f"  {project['id']}. {project['name']}")
            print(f"     类型: {project['project_type']} | 成熟度: {project['maturity']}")
            print()
    except Exception as e:
        print(f"❌ 搜索失败: {e}")

def get_project_stats():
    """获取项目统计信息"""
    print("\n📊 演示：项目统计概览")
    
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
        
        print(f"总项目数: {total}")
        print("\n按类型分布:")
        for ptype, count in by_type.items():
            print(f"  {ptype}: {count}")
        
        print("\n按成熟度分布:")
        for maturity, count in by_maturity.items():
            print(f"  {maturity}: {count}")
        
        print("\n按状态分布:")
        for status, count in by_status.items():
            print(f"  {status}: {count}")
            
    except Exception as e:
        print(f"❌ 获取统计信息失败: {e}")

def main():
    """主函数"""
    print("🚀 项目导航MCP工具演示")
    print("=" * 50)
    
    # 测试API连接
    if not test_api_connection():
        print("请确保navigator服务器正在运行:")
        print("cd navigator && uv run uvicorn app.main:app --reload --port 8000")
        return
    
    # 演示各种功能
    add_project_demo()
    list_projects_demo()
    search_projects_demo()
    get_project_stats()
    
    print("\n🎉 演示完成!")
    print("\n💡 这些功能都可以通过MCP协议供AI Agent调用:")
    print("   - Cursor IDE可以通过这些工具来管理项目记录")
    print("   - Claude Desktop可以直接执行项目操作")
    print("   - 任何支持MCP的AI工具都可以使用这些功能")

if __name__ == "__main__":
    main() 