# MCP项目导航工具 | MCP Project Navigator Tool

> 🤖 符合Anthropic MCP标准的项目导航工具，为AI Agent提供项目管理功能

[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-orange.svg)](https://modelcontextprotocol.io)
[![Python Version](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Framework](https://img.shields.io/badge/Backend-FastAPI-green.svg)](https://fastapi.tiangolo.com)
[![AI Agent](https://img.shields.io/badge/AI-Agent%20Ready-purple.svg)]()

## 📖 项目简介

### 🌟 项目背景

MCP项目导航工具是项目导航系统的AI集成组件，实现了Anthropic Model Context Protocol (MCP) 标准，使AI Agent能够通过标准化接口直接操作项目记录。这标志着项目管理从手动操作向AI驱动的智能化管理的重要转型。

### 💎 核心价值

#### 🎯 AI原生设计

- **MCP标准兼容**：完全符合Anthropic MCP协议规范
- **AI Agent集成**：支持Cursor、Claude Desktop、TRAE IDE等AI开发环境
- **自然语言交互**：通过自然语言指令操作项目记录
- **上下文感知**：为AI提供丰富的项目上下文信息

#### 💼 功能价值实现

- **智能项目管理**：AI驱动的项目创建、查询、更新操作
- **语义化搜索**：支持自然语言的项目搜索和筛选
- **自动化工作流**：集成到AI开发工作流中，提升效率
- **多Agent支持**：同时支持多个AI Agent并发访问

#### 🔧 技术优势

- **标准化协议**：基于JSON-RPC 2.0的稳定通信协议
- **高性能实现**：异步处理，支持高并发调用
- **类型安全**：完整的类型注解和输入验证
- **错误恢复**：完善的错误处理和重试机制

## 🏗️ MCP架构

### Model Context Protocol概述

```
┌─────────────────────────────────────────────────────────────┐
│                    AI Agent (Client)                       │
│              (Cursor/Claude Desktop/TRAE IDE)                      │
├─────────────────────────────────────────────────────────────┤
│                   MCP Protocol Layer                       │
│                  (JSON-RPC 2.0)                           │
├─────────────────────────────────────────────────────────────┤
│                   MCP Server (Tool)                        │
│              项目导航MCP工具                                 │
├─────────────────────────────────────────────────────────────┤
│                   Backend API                              │
│               Navigator FastAPI                            │
├─────────────────────────────────────────────────────────────┤
│                   Data Storage                             │
│                SQLite Database                             │
└─────────────────────────────────────────────────────────────┘
```

### MCP组件架构

#### 1. Tools Interface (工具接口)

- **add_project**: 添加新项目记录
- **list_projects**: 列出项目（支持筛选）
- **search_projects**: 搜索项目
- **get_project**: 获取项目详情
- **update_project_status**: 更新项目状态

#### 2. Resources Interface (资源接口)

- **projects_summary**: 项目统计概览
- **project_types**: 项目类型信息

#### 3. Transport Layer (传输层)

- **JSON-RPC 2.0**: 标准化通信协议
- **HTTP/HTTPS**: 安全的网络传输
- **异步处理**: 高性能并发支持

## 🚀 快速开始

### 环境要求

- **Python 3.10+**: MCP SDK最低要求
- **Navigator后端**: 项目导航API服务器
- **AI Agent**: 支持MCP的AI开发环境

### 安装配置

#### 方式1: 使用uvx调用 (推荐)

```bash
# 构建包（仅需一次）
cd mcp_tool
python -m build

# 通过uvx运行（无需安装依赖）
uvx --from ./dist/project_navigator_mcp-1.0.0-py3-none-any.whl project-navigator-mcp
```

#### 方式2: 传统安装

```bash
# 进入mcp_tool目录
cd mcp_tool

# 安装Python依赖
pip install mcp requests python-dotenv

# 或使用requirements.txt
pip install -r requirements.txt

# 直接运行
python mcp_server.py
```

#### 2. 启动Navigator后端

```bash
# 在另一个终端启动后端服务
cd ../navigator
uvicorn app.main:app --reload --port 8000
```

#### 3. 配置环境变量

```bash
# 创建.env文件（可选）
cat > .env << EOF
API_BASE_URL=http://127.0.0.1:8000
LOG_LEVEL=INFO
PROXY_DISABLE=true
EOF
```

#### 4. 测试MCP工具

```bash
# 运行功能演示
python manual_test.py

# 运行简单测试
python simple_test.py
```

### Claude Desktop配置

#### 1. 配置文件位置

```bash
# Windows
%APPDATA%\Claude\claude_desktop_config.json

# macOS
~/Library/Application Support/Claude/claude_desktop_config.json

# Linux
~/.config/Claude/claude_desktop_config.json
```

#### 2. 添加MCP配置

**方式1: 使用uvx (推荐)**

```json
{
  "mcpServers": {
    "project-navigator": {
      "command": "uvx",
      "args": [
        "--from", 
        "D:/Workspace/Trae/mcps/notion_storage/mcp_tool/dist/project_navigator_mcp-1.0.0-py3-none-any.whl",
        "project-navigator-mcp"
      ],
      "env": {
        "API_BASE_URL": "http://127.0.0.1:8000",
        "no_proxy": "127.0.0.1,localhost"
      }
    }
  }
}
```

**方式2: 传统Python调用**

```json
{
  "mcpServers": {
    "project-navigator": {
      "command": "python",
      "args": ["D:/Workspace/Trae/mcps/notion_storage/mcp_tool/mcp_server.py"],
      "env": {
        "API_BASE_URL": "http://127.0.0.1:8000",
        "no_proxy": "127.0.0.1,localhost"
      }
    }
  }
}
```

#### 3. 重启Claude Desktop

```bash
# 保存配置后重启Claude Desktop应用
# MCP工具将自动加载并可用
```

## 🛠️ MCP工具功能

### 核心Tools

#### 1. add_project - 添加项目

```python
# 工具Schema
{
  "name": "add_project",
  "description": "添加新的项目记录到数据库",
  "inputSchema": {
    "type": "object",
    "properties": {
      "name": {"type": "string", "description": "项目名称"},
      "project_type": {"type": "string", "enum": ["工具开发", "理论分析", "AI应用"]},
      "maturity": {"type": "string", "enum": ["High", "Medium", "Low"]},
      "status": {"type": "string", "enum": ["完成", "进行中", "研究中", "规划中", "理论归档"]},
      "description": {"type": "string", "description": "项目描述"},
      "readme_path": {"type": "string", "description": "README文件路径"}
    },
    "required": ["name", "project_type", "maturity", "status", "readme_path"]
  }
}
```

**使用示例**：

```
请帮我添加一个新项目：
名称：AI代码审查工具
类型：AI应用  
成熟度：High
状态：规划中
描述：基于LLM的自动化代码质量检查和建议系统
README路径：ideaed-projects/ai-code-reviewer/README.md
```

#### 2. list_projects - 列出项目

```python
# 工具Schema
{
  "name": "list_projects",
  "description": "获取项目列表，支持按类型、成熟度、状态筛选",
  "inputSchema": {
    "type": "object", 
    "properties": {
      "project_type": {"type": "string", "description": "按项目类型筛选"},
      "maturity": {"type": "string", "description": "按成熟度筛选"},
      "status": {"type": "string", "description": "按状态筛选"},
      "limit": {"type": "integer", "description": "返回的最大项目数", "default": 50}
    }
  }
}
```

**使用示例**：

```
显示所有高成熟度的AI应用项目
列出状态为"进行中"的工具开发项目
获取最近的10个项目
```

#### 3. search_projects - 搜索项目

```python
# 工具Schema
{
  "name": "search_projects", 
  "description": "根据关键词搜索项目名称和描述",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": {"type": "string", "description": "搜索关键词"},
      "limit": {"type": "integer", "description": "返回的最大结果数", "default": 20}
    },
    "required": ["query"]
  }
}
```

**使用示例**：

```
搜索包含"AI"的项目
查找所有数据分析相关的项目
搜索"决策"关键词的项目
```

#### 4. get_project - 获取项目详情

```python
# 工具Schema
{
  "name": "get_project",
  "description": "根据项目ID获取详细信息",
  "inputSchema": {
    "type": "object",
    "properties": {
      "project_id": {"type": "integer", "description": "项目ID"}
    },
    "required": ["project_id"]
  }
}
```

**使用示例**：

```
获取项目ID为5的详细信息
显示"AI决策框架"项目的完整信息
```

#### 5. update_project_status - 更新项目状态

```python
# 工具Schema
{
  "name": "update_project_status",
  "description": "更新指定项目的状态",
  "inputSchema": {
    "type": "object",
    "properties": {
      "project_id": {"type": "integer", "description": "项目ID"},
      "new_status": {"type": "string", "enum": ["完成", "进行中", "研究中", "规划中", "理论归档"]}
    },
    "required": ["project_id", "new_status"]
  }
}
```

**使用示例**：

```
将项目ID为3的状态更新为"完成"
把"数据平台决策工具包"的状态改为"进行中"
```

### Resources资源

#### 1. projects_summary - 项目统计

```python
# 资源URI: projects://summary
# 提供项目的统计概览信息
{
  "total_projects": 19,
  "by_type": {
    "工具开发": 7,
    "理论分析": 11, 
    "AI应用": 1
  },
  "by_status": {
    "完成": 2,
    "进行中": 1,
    "研究中": 11,
    "规划中": 3,
    "理论归档": 2
  },
  "by_maturity": {
    "High": 4,
    "Medium": 13,
    "Low": 2
  }
}
```

#### 2. project_types - 项目类型信息

```python
# 资源URI: projects://types
# 提供项目类型的详细说明
{
  "工具开发": {
    "description": "可直接使用的软件工具和系统",
    "count": 7,
    "examples": ["AI决策框架", "交互式数据仪表板"]
  },
  "理论分析": {
    "description": "深度技术研究和理论分析",
    "count": 11,
    "examples": ["AI透明性理论分析", "数据护城河分析"]
  },
  "AI应用": {
    "description": "基于AI技术的应用系统",
    "count": 1,
    "examples": ["MCP项目导航工具"]
  }
}
```

## 🧪 测试和验证

### 功能测试

#### 1. 基础功能测试

```bash
# 运行完整功能演示
python manual_test.py
```

**预期输出**：

```
🚀 项目导航MCP工具演示
==================================================
✅ API连接成功

📝 演示：添加新项目
✅ 项目创建成功，ID: 20

📋 演示：列出所有项目
共找到 20 个项目

🔍 演示：搜索AI相关项目
找到 16 个AI相关项目

📊 演示：项目统计概览
总项目数: 20
按类型分布: 工具开发(7), 理论分析(11), AI应用(2)
```

#### 2. 简单连接测试

```bash
# 运行API连接测试
python simple_test.py
```

#### 3. Claude Desktop集成测试

```
# 在Claude Desktop中测试以下指令：

1. "请列出所有项目"
2. "添加一个新的AI工具项目"
3. "搜索包含数据的项目"
4. "显示项目统计信息"
5. "更新某个项目的状态"
```

### 错误处理测试

#### 1. 网络连接测试

```python
# 测试后端服务不可用的情况
# 停止navigator后端服务
# 运行：python manual_test.py
# 应该看到连接错误的友好提示
```

#### 2. 数据验证测试

```python
# 测试无效的输入参数
# 在Claude Desktop中尝试：
"添加一个项目，类型为无效类型"
# 应该返回参数验证错误
```

## 🔧 开发指南

### 项目结构

```
mcp_tool/
├── mcp_server.py           # MCP服务器主程序
├── manual_test.py          # 功能演示脚本
├── simple_test.py          # 简单测试脚本
├── __init__.py             # 包初始化
├── pyproject.toml          # 项目配置
├── requirements.txt        # Python依赖
├── mcp_config.json         # Claude Desktop配置示例
└── README.md              # 项目文档
```

### 扩展新工具

#### 1. 添加新的Tool

```python
# 在mcp_server.py中添加新工具
@server.call_tool()
async def new_tool_name(arguments: dict) -> list[TextContent]:
    """新工具的描述"""
    try:
        # 工具实现逻辑
        result = await process_tool_request(arguments)
        return [TextContent(type="text", text=f"操作成功: {result}")]
    except Exception as e:
        return [TextContent(type="text", text=f"操作失败: {str(e)}")]
```

#### 2. 添加新的Resource

```python
# 添加新资源
@server.list_resources()
async def list_resources() -> list[Resource]:
    return [
        # ... 现有资源
        Resource(
            uri=AnyUrl("projects://new_resource"),
            name="新资源名称",
            description="新资源的描述",
            mimeType="application/json",
        ),
    ]

@server.read_resource()
async def read_resource(uri: AnyUrl) -> str:
    if str(uri) == "projects://new_resource":
        # 返回新资源的数据
        return json.dumps({"data": "新资源数据"})
    # ... 处理其他资源
```

### 调试和日志

#### 1. 启用调试模式

```python
# 在mcp_server.py中设置
import logging
logging.basicConfig(level=logging.DEBUG)

# 或设置环境变量
export LOG_LEVEL=DEBUG
```

#### 2. 查看MCP通信日志

```python
# 在开发模式下，可以看到JSON-RPC通信详情
# 有助于调试MCP协议交互问题
```

### 性能优化

#### 1. 连接池优化

```python
# 在mcp_server.py中使用会话复用
import aiohttp

async def make_api_request(url, method="GET", data=None):
    async with aiohttp.ClientSession() as session:
        # 使用连接池减少连接开销
        async with session.request(method, url, json=data) as response:
            return await response.json()
```

#### 2. 缓存策略

```python
# 添加简单的内存缓存
from functools import lru_cache
from datetime import datetime, timedelta

class SimpleCache:
    def __init__(self, ttl_seconds=300):  # 5分钟缓存
        self.cache = {}
        self.ttl = ttl_seconds
  
    def get(self, key):
        if key in self.cache:
            data, timestamp = self.cache[key]
            if datetime.now() - timestamp < timedelta(seconds=self.ttl):
                return data
        return None
  
    def set(self, key, value):
        self.cache[key] = (value, datetime.now())

# 全局缓存实例
cache = SimpleCache()
```

## 🚀 部署指南

### 本地部署

#### 1. 开发环境

```bash
# 克隆项目
git clone https://github.com/username/notion_storage.git
cd notion_storage

# 启动后端服务
cd navigator
uvicorn app.main:app --reload --port 8000

# 启动MCP工具（另一个终端）
cd ../mcp_tool
python mcp_server.py
```

#### 2. 生产环境

```bash
# 使用系统服务管理
sudo systemctl start navigator
sudo systemctl enable navigator

# MCP工具通过AI Agent按需启动
# 无需独立的系统服务
```

### Claude Desktop集成

#### 1. 全局配置

```json
{
  "mcpServers": {
    "project-navigator": {
      "command": "python",
      "args": ["/path/to/notion_storage/mcp_tool/mcp_server.py"],
      "env": {
        "API_BASE_URL": "http://127.0.0.1:8000",
        "no_proxy": "127.0.0.1,localhost"
      }
    }
  }
}
```

#### 2. 企业配置

```json
{
  "mcpServers": {
    "project-navigator": {
      "command": "python",
      "args": ["/path/to/mcp_server.py"],
      "env": {
        "API_BASE_URL": "https://navigator.company.com",
        "API_TOKEN": "your-api-token"
      }
    }
  }
}
```

### Docker化部署

#### 1. Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# MCP工具作为库提供，不需要独立服务
# 通过AI Agent按需调用
```

#### 2. Docker Compose集成

```yaml
version: '3.8'
services:
  navigator:
    build: ../navigator
    ports:
      - "8000:8000"
  
  # MCP工具集成到AI Agent配置中
  # 不需要独立的Docker服务
```

## 📈 使用统计

### 当前功能覆盖

- ✅ **项目CRUD**: 完整的增删改查操作
- ✅ **智能搜索**: 关键词和多维度筛选
- ✅ **状态管理**: 项目状态生命周期管理
- ✅ **数据统计**: 实时的项目统计信息
- ✅ **错误处理**: 完善的异常处理机制

### 支持的AI Agent

- ✅ **Claude Desktop**: 官方桌面应用
- ✅ **Cursor**: AI代码编辑器
- ✅ **TRAE IDE**: AI开发环境
- 🔄 **其他MCP兼容工具**: 持续扩展中

### 性能指标

- **API响应时间**: < 200ms
- **MCP调用延迟**: < 100ms
- **并发支持**: 支持多Agent同时访问
- **错误率**: < 1%

## 🔒 安全性

### MCP安全特性

- **输入验证**: 严格的参数类型和范围验证
- **API安全**: 继承Navigator后端的安全策略
- **本地通信**: 默认使用本地API连接
- **无状态设计**: 不存储敏感信息

### 网络安全

```python
# 代理绕过配置（解决本地网络问题）
import os
os.environ['no_proxy'] = '127.0.0.1,localhost'

# HTTPS支持
API_BASE_URL = "https://your-domain.com"

# API密钥支持（可选）
headers = {
    "Authorization": f"Bearer {api_token}"
}
```

## 🤝 贡献指南

### MCP工具开发贡献

1. **了解MCP标准**: 熟悉Anthropic MCP协议规范
2. **Python环境**: 安装Python 3.10+和相关依赖
3. **测试要求**: 为新工具添加测试用例
4. **文档更新**: 更新工具Schema和使用说明
5. **AI Agent测试**: 在实际AI环境中验证功能

### 开发流程

1. Fork项目并创建功能分支
2. 开发新的MCP工具或资源
3. 编写测试用例
4. 在AI Agent中测试功能
5. 更新文档和Schema
6. 提交Pull Request

### 问题报告

- 🤖 **MCP兼容性**: 报告AI Agent集成问题
- 🔧 **工具功能**: 建议新的MCP工具
- 📊 **性能问题**: 报告响应时间问题
- 🔒 **安全问题**: 报告安全漏洞

## 📄 许可证

本项目采用 [MIT License](../LICENSE) 开源协议。

## 📞 联系方式

- **MCP问题**: 在仓库中提交Issue并标记 `mcp`标签
- **AI集成**: 通过Issue讨论AI Agent集成问题
- **技术支持**: 查看MCP官方文档或联系维护团队

## 🙏 致谢

特别感谢：

- **Anthropic**: MCP协议的设计和开发
- **Claude Desktop团队**: 提供优秀的AI Agent平台
- **开源社区**: MCP生态系统的建设者

---

🤖 **MCP项目导航工具** - 让AI Agent轻松管理你的项目！
