# AI决策框架评分工具

一个基于科学决策框架的AI系统架构选择工具，帮助开发者在工作流(Workflow)和智能体(Agent)之间做出明智选择。

## 📖 项目背景

本项目灵感来源于一篇深度技术文章：

- **原文链接**: [A Developer&#39;s Guide to Building Scalable AI: Workflows vs Agents](https://towardsdatascience.com/a-developers-guide-to-building-scalable-ai-workflows-vs-agents/)
- **中文整理**: [豆包AI整理版本](https://www.doubao.com/desktop/ai-web-read/roG3Jlem3nz)

该文章深入分析了当前AI开发中的一个关键问题：95%的公司在使用生成式AI，79%实施了AI智能体，但只有1%被认为是"成熟"的实施。文章提出了一个科学的决策框架，帮助开发者避免盲目跟风，根据实际需求选择合适的AI架构。

## 🎯 核心价值

### 问题洞察

- **盲目跟风现象**: 大多数团队因新技术魅力而冲动选择智能体
- **隐藏成本**: 智能体的Token消耗、调试难度、维护复杂性常被忽视
- **决策困境**: 缺乏科学的评估框架来指导技术选型

### 解决方案

本工具基于文章提出的多维度评估框架，通过量化评分帮助开发者：

- 🔍 **客观评估**: 7个关键维度的科学评分
- 📊 **数据驱动**: 基于总分提供个性化建议
- ⚖️ **平衡考量**: 在稳定性与创新性之间找到最佳平衡点

## 🛠️ 功能特性

### 评估维度

#### 📋 项目需求评估

- **任务复杂度**: 评估是否需要动态决策和自适应能力
- **可预测性要求**: 系统输出的一致性和可预测性需求
- **调试重要性**: 故障排查和系统维护的重要程度

#### 💰 资源与成本考量

- **成本敏感度**: 对Token消耗和计算资源的敏感程度
- **开发资源**: 可投入的开发和维护资源情况

#### 🎯 业务场景特性

- **创新需求**: 业务对创新性和探索性解决方案的需求
- **错误容忍度**: 业务场景对系统错误的容忍程度

### 智能推荐

| 总分范围 | 推荐方案               | 特点描述                           |
| -------- | ---------------------- | ---------------------------------- |
| ≤25分   | 🔧**工作流**     | 结构化、可预测、成本可控           |
| 26-45分  | ⚖️**混合方案** | 关键路径用工作流，灵活部分用智能体 |
| ≥46分   | 🤖**智能体**     | 高复杂度、创新导向、自主决策       |

## 📁 项目结构

```
ai-decision-framework/
├── README.md                 # 项目说明文档
├── index.html               # 主评分工具页面
├── assets/                  # 静态资源目录
│   ├── css/                # 样式文件
│   ├── js/                 # JavaScript文件
│   └── images/             # 图片资源
├── docs/                   # 文档目录
│   ├── decision-framework.md # 决策框架详细说明
│   └── case-studies.md     # 案例研究
└── examples/               # 示例和模板
    ├── workflow-example.md
    └── agent-example.md
```

## 🚀 快速开始

### 方法一：直接使用网页版

1. **打开评分工具**

   ```bash
   # 在浏览器中打开
   open index.html
   ```
2. **进行评估**

   - 根据项目实际情况调整7个维度的评分
   - 观察实时更新的总分和推荐方案
   - 参考详细说明做出最终决策
3. **查看文档**

   - 阅读 `docs/decision-framework.md` 了解理论基础
   - 参考 `examples/` 中的实际案例

### 方法二：使用uv包管理器（推荐）

#### 1. 安装uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 或使用pip
pip install uv
```

#### 2. 快速启动

```bash
# 一键启动开发环境
make quick-start

# 或手动步骤
uv sync --extra dev    # 安装依赖
uv run python run.py   # 启动服务
```

#### 3. 常用命令

```bash
# 查看所有可用命令
make help

# 安装依赖
make install-dev      # 开发依赖
make install-full     # 完整功能

# 代码质量
make format           # 格式化代码
make lint            # 代码检查
make test            # 运行测试

# 开发服务器
make dev             # 启动开发服务器
make start           # 启动生产服务器
```

### 方法三：传统pip方式

1. **安装依赖**

   ```bash
   # 使用快速启动脚本
   python run.py --install

   # 或手动安装
   pip install -r requirements.txt
   ```
2. **配置环境**

   ```bash
   # 复制环境配置模板
   cp .env.example .env

   # 编辑 .env 文件，配置必要参数（如OpenAI API Key）
   ```
3. **启动服务**

   ```bash
   # 开发模式
   python run.py

   # 生产模式
   python run.py --prod

   # 自定义端口
   python run.py --port 9000
   ```
4. **访问应用**

   - 主页：http://localhost:8000
   - API文档：http://localhost:8000/docs
   - 健康检查：http://localhost:8000/health

## 📚 理论基础

### 工作流 vs 智能体对比

| 特性               | 工作流             | 智能体          |
| ------------------ | ------------------ | --------------- |
| **控制方式** | 开发者定义明确步骤 | LLM自主决策路径 |
| **执行模式** | 结构化管道         | 动态循环推理    |
| **可预测性** | 高度可预测         | 存在不确定性    |
| **调试难度** | 透明易调试         | 复杂难追踪      |
| **成本控制** | 可预测可控         | 可能大幅波动    |
| **适用场景** | 稳定业务流程       | 复杂创新任务    |

### 成功案例

#### 工作流成功案例

- **OneUnited银行**: 结构化客户服务流程
- **Sequoia金融集团**: 标准化金融分析管道

#### 智能体成功案例

- **Klarna**: 智能体处理700个客服代表的工作量
- **BCG**: 多智能体设计系统减少近一半造船工程时间

## 🔄 版本历史

- **v1.0.0** (2024-12): 初始版本，基础评分功能
- **规划中**: 数据持久化、多项目对比、详细报告生成

## 📚 API使用示例

### 评估项目架构

```python
import requests

# 项目评估请求
data = {
    "project_name": "智能客服系统",
    "description": "为电商平台构建智能客服系统",
    "requirements": {
        "task_complexity": 4,
        "structure_level": 3,
        "creativity_need": 3
    },
    "resources": {
        "budget_level": 3,
        "time_urgency": 4,
        "team_expertise": 3
    },
    "scenario": {
        "user_interaction": 4
    }
}

response = requests.post("http://localhost:8000/evaluate", json=data)
result = response.json()

print(f"推荐架构: {result['recommendation']}")
print(f"置信度: {result['confidence']}")
print(f"总分: {result['total_score']}")
```

### 获取架构详细信息

```python
# 获取工作流架构详情
response = requests.get("http://localhost:8000/recommendations/workflow")
workflow_info = response.json()

# 获取智能体架构详情
response = requests.get("http://localhost:8000/recommendations/agent")
agent_info = response.json()

# 获取混合架构详情
response = requests.get("http://localhost:8000/recommendations/hybrid")
hybrid_info = response.json()
```

## 🔧 部署指南

### Docker部署

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "main.py"]
```

```bash
# 构建和运行
docker build -t ai-decision-framework .
docker run -p 8000:8000 ai-decision-framework
```

### 云平台部署

支持部署到各大云平台：

- **Heroku**：使用 `Procfile`
- **AWS Lambda**：使用 Mangum 适配器
- **Google Cloud Run**：容器化部署
- **Azure Container Instances**：快速容器部署

## 🤝 贡献指南

我们欢迎各种形式的贡献：

1. **报告问题**：在GitHub Issues中报告bug或提出功能请求
2. **提交代码**：Fork项目，创建分支，提交Pull Request
3. **改进文档**：帮助完善文档和示例
4. **分享案例**：分享您的使用案例和最佳实践

### 提交规范

- 遵循现有的代码风格
- 添加必要的测试用例
- 更新相关文档
- 提供清晰的提交信息

## 📄 许可证

MIT License

## 🙏 致谢

- 感谢原文作者提供的深刻洞察和科学框架
- 感谢豆包AI提供的中文整理版本
- 感谢所有为AI开发实践贡献经验的开发者们

---

> "不应盲目选择智能体，而要依据实际需求决定，有时可靠的工作流才是更合适的选择。"
>
> —— 摘自原文
