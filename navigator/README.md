# Navigator后端服务 | Navigator Backend Service

> 🚀 项目导航系统的核心后端服务，基于FastAPI构建的高性能RESTful API服务器

[![Framework](https://img.shields.io/badge/Framework-FastAPI-green.svg)](https://fastapi.tiangolo.com)
[![Python Version](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Database](https://img.shields.io/badge/Database-SQLite-orange.svg)]()
[![ORM](https://img.shields.io/badge/ORM-SQLAlchemy-red.svg)](https://sqlalchemy.org)

## 📖 项目简介

Navigator后端服务是项目导航系统的核心组件，负责提供所有数据操作和业务逻辑。它将传统的手动Markdown文件管理转换为现代化的API驱动系统，为Web前端、CLI工具和MCP协议提供统一的数据访问接口。

### 核心特性
- **FastAPI框架**：高性能异步API服务器
- **SQLite数据库**：轻量级本地数据存储
- **自动文档**：OpenAPI/Swagger自动生成
- **类型安全**：完整的类型注解支持
- **多端服务**：支持Web、CLI、MCP多种客户端

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────┐
│            API接口层 (FastAPI)               │
├─────────────────────────────────────────────┤
│            业务逻辑层 (CRUD)                 │
├─────────────────────────────────────────────┤
│         数据模型层 (SQLAlchemy)              │
├─────────────────────────────────────────────┤
│          数据存储层 (SQLite)                 │
└─────────────────────────────────────────────┘
```

## 🚀 快速开始

### 环境要求
- Python 3.8+
- uv 包管理器（推荐）

### 安装部署

1. **克隆并进入项目目录**
```bash
git clone https://github.com/username/notion_storage.git
cd notion_storage/navigator
```

2. **安装依赖**
```bash
# 使用uv（推荐）
uv install

# 或使用pip
pip install fastapi uvicorn sqlalchemy markdown2 python-multipart
```

3. **启动服务**
```bash
# 开发模式
uv run uvicorn app.main:app --reload --port 8000

# 或直接启动
uvicorn app.main:app --reload --port 8000
```

4. **验证安装**
```bash
# API文档
open http://127.0.0.1:8000/docs

# 获取项目列表
curl http://127.0.0.1:8000/api/projects
```

## 🛠️ API接口

### 核心端点

#### 项目管理
```http
GET    /api/projects           # 获取项目列表
POST   /api/projects           # 创建新项目
GET    /api/projects/{id}      # 获取项目详情
PUT    /api/projects/{id}      # 更新项目
DELETE /api/projects/{id}      # 删除项目
```

#### 文档查看
```http
GET    /view/{file_path}       # 查看Markdown文档
```

#### 系统状态
```http
GET    /health                 # 健康检查
GET    /docs                   # API文档
```

### API示例

**获取项目列表（支持筛选）**
```bash
curl "http://127.0.0.1:8000/api/projects?project_type=工具开发&status=完成"
```

**创建新项目**
```bash
curl -X POST "http://127.0.0.1:8000/api/projects" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "新AI工具",
    "project_type": "AI应用",
    "maturity": "High",
    "status": "规划中",
    "description": "基于LLM的智能工具",
    "readme_path": "ideaed-projects/new-ai-tool/README.md"
  }'
```

## 📊 数据模型

### 项目实体
```python
class Project:
    id: int                    # 主键
    name: str                  # 项目名称
    project_type: str          # 类型："工具开发", "理论分析", "AI应用"
    maturity: str              # 成熟度："High", "Medium", "Low"
    status: str                # 状态："完成", "进行中", "研究中", "规划中", "理论归档"
    description: Optional[str] # 项目描述
    readme_path: str           # README文件路径
    created_date: date         # 创建日期
```

### 支持的枚举值
- **项目类型**: `工具开发`, `理论分析`, `AI应用`
- **成熟度**: `High`, `Medium`, `Low`
- **状态**: `完成`, `进行中`, `研究中`, `规划中`, `理论归档`

## 🔧 项目结构

```
navigator/
├── app/
│   ├── main.py              # FastAPI应用入口
│   ├── models.py            # SQLAlchemy数据模型
│   ├── schemas.py           # Pydantic验证模型
│   ├── crud.py              # 数据库CRUD操作
│   ├── database.py          # 数据库配置
│   └── cli.py               # 命令行工具
├── tests/                   # 测试文件
├── pyproject.toml           # 项目配置
├── navigator.db             # SQLite数据库
└── README.md               # 项目文档
```

## 🧪 开发和测试

### 开发环境
```bash
# 安装开发依赖
uv install --dev

# 代码格式化
black app/
isort app/

# 运行测试
pytest tests/ -v
```

### 数据库操作
```bash
# 初始化数据库
python -c "from app.database import init_db; init_db()"

# 重置数据库
rm navigator.db && python -c "from app.database import init_db; init_db()"
```

## 🐳 Docker部署

```dockerfile
FROM python:3.8-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# 构建和运行
docker build -t navigator-backend .
docker run -p 8000:8000 navigator-backend
```

## 📈 当前状态

### 功能实现
- ✅ 完整的项目CRUD API
- ✅ Markdown文档在线查看
- ✅ 数据验证和错误处理
- ✅ 自动API文档生成
- ✅ SQLite数据持久化
- ✅ 多维度项目筛选和搜索

### 系统指标
- **项目总数**: 19个
- **API响应时间**: < 100ms
- **数据库查询**: < 50ms
- **支持的客户端**: Web前端、CLI工具、MCP协议

## 🔒 安全性

- **输入验证**: Pydantic自动数据验证
- **SQL注入防护**: SQLAlchemy ORM参数化查询
- **路径安全**: 文件访问路径验证
- **错误处理**: 统一的异常处理机制

## 🤝 贡献指南

1. **设置开发环境**: 安装Python 3.8+和uv
2. **代码规范**: 遵循PEP 8和类型注解
3. **测试要求**: 为新功能添加测试用例
4. **文档更新**: 更新API文档和注释

### 问题报告
- 🐛 Bug报告：详细描述重现步骤
- 💡 功能建议：提出API改进建议
- 📊 性能问题：报告响应时间问题

## 📄 许可证

本项目采用 [MIT License](../LICENSE) 开源协议。

## 📞 联系方式

- **API文档**: http://127.0.0.1:8000/docs
- **技术问题**: 在仓库中提交Issue
- **开发讨论**: 通过Issue或Discussion参与

---

🚀 **Navigator后端服务** - 为项目导航系统提供强大的API支持！
