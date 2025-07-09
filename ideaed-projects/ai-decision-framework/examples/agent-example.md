# 智能体架构示例与最佳实践

本文档提供智能体架构的具体实现示例、设计模式和最佳实践，帮助开发者构建智能、自主的AI代理系统。

## 🤖 基础智能体框架

### 核心智能体类

```python
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import json
import logging
from datetime import datetime
from abc import ABC, abstractmethod

class AgentState(Enum):
    """智能体状态"""
    IDLE = "idle"
    THINKING = "thinking"
    ACTING = "acting"
    WAITING = "waiting"
    ERROR = "error"

@dataclass
class AgentMemory:
    """智能体记忆"""
    short_term: List[Dict[str, Any]]  # 短期记忆
    long_term: Dict[str, Any]        # 长期记忆
    working_memory: Dict[str, Any]   # 工作记忆
    episodic_memory: List[Dict[str, Any]]  # 情节记忆

@dataclass
class AgentAction:
    """智能体动作"""
    action_type: str
    parameters: Dict[str, Any]
    timestamp: datetime
    reasoning: str
    confidence: float

class Tool(ABC):
    """工具基类"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    def execute(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """执行工具"""
        pass
    
    @abstractmethod
    def get_schema(self) -> Dict[str, Any]:
        """获取工具参数模式"""
        pass

class BaseAgent:
    """基础智能体类"""
    
    def __init__(self, name: str, role: str, llm_client, tools: List[Tool] = None):
        self.name = name
        self.role = role
        self.llm_client = llm_client
        self.tools = {tool.name: tool for tool in (tools or [])}
        self.state = AgentState.IDLE
        self.memory = AgentMemory(
            short_term=[],
            long_term={},
            working_memory={},
            episodic_memory=[]
        )
        self.logger = logging.getLogger(f"agent.{name}")
        self.conversation_history = []
        self.max_iterations = 10
    
    def process_request(self, request: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """处理请求的主入口"""
        self.state = AgentState.THINKING
        
        try:
            # 更新工作记忆
            self.memory.working_memory.update(context or {})
            
            # 添加到对话历史
            self.conversation_history.append({
                'role': 'user',
                'content': request,
                'timestamp': datetime.now()
            })
            
            # 执行推理循环
            result = self.reasoning_loop(request)
            
            # 更新记忆
            self.update_memory(request, result)
            
            self.state = AgentState.IDLE
            return result
            
        except Exception as e:
            self.state = AgentState.ERROR
            self.logger.error(f"处理请求时出错: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'response': '抱歉，处理您的请求时遇到了问题。'
            }
    
    def reasoning_loop(self, request: str) -> Dict[str, Any]:
        """推理循环 - ReAct模式"""
        iteration = 0
        
        while iteration < self.max_iterations:
            iteration += 1
            
            # 思考阶段
            thought = self.think(request)
            
            # 决策阶段
            decision = self.decide(thought)
            
            if decision['type'] == 'final_answer':
                return {
                    'success': True,
                    'response': decision['content'],
                    'reasoning_steps': len(self.memory.short_term),
                    'tools_used': self.get_tools_used()
                }
            
            elif decision['type'] == 'use_tool':
                # 执行工具
                tool_result = self.use_tool(
                    decision['tool_name'],
                    decision['parameters']
                )
                
                # 观察结果
                self.observe(tool_result)
            
            elif decision['type'] == 'need_clarification':
                return {
                    'success': False,
                    'response': decision['content'],
                    'need_clarification': True
                }
        
        return {
            'success': False,
            'response': '抱歉，我无法在合理的步骤内完成这个任务。',
            'max_iterations_reached': True
        }
    
    def think(self, request: str) -> str:
        """思考阶段"""
        # 构建思考提示
        thinking_prompt = self.build_thinking_prompt(request)
        
        # 获取LLM响应
        thought = self.llm_client.complete(thinking_prompt)
        
        # 记录思考过程
        self.memory.short_term.append({
            'type': 'thought',
            'content': thought,
            'timestamp': datetime.now()
        })
        
        return thought
    
    def decide(self, thought: str) -> Dict[str, Any]:
        """决策阶段"""
        decision_prompt = self.build_decision_prompt(thought)
        
        decision_text = self.llm_client.complete(decision_prompt)
        
        # 解析决策
        decision = self.parse_decision(decision_text)
        
        # 记录决策
        self.memory.short_term.append({
            'type': 'decision',
            'content': decision,
            'timestamp': datetime.now()
        })
        
        return decision
    
    def use_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """使用工具"""
        self.state = AgentState.ACTING
        
        if tool_name not in self.tools:
            return {
                'success': False,
                'error': f'工具 {tool_name} 不存在'
            }
        
        try:
            tool = self.tools[tool_name]
            result = tool.execute(parameters)
            
            self.logger.info(f"使用工具 {tool_name}: {parameters}")
            
            return {
                'success': True,
                'tool_name': tool_name,
                'parameters': parameters,
                'result': result
            }
            
        except Exception as e:
            return {
                'success': False,
                'tool_name': tool_name,
                'error': str(e)
            }
    
    def observe(self, tool_result: Dict[str, Any]):
        """观察工具执行结果"""
        self.memory.short_term.append({
            'type': 'observation',
            'content': tool_result,
            'timestamp': datetime.now()
        })
    
    def build_thinking_prompt(self, request: str) -> str:
        """构建思考提示"""
        # 获取相关记忆
        relevant_memory = self.retrieve_relevant_memory(request)
        
        # 获取可用工具
        available_tools = self.get_available_tools_description()
        
        # 获取对话历史
        recent_history = self.get_recent_conversation_history()
        
        prompt = f"""
你是一个名为 {self.name} 的AI助手，角色是 {self.role}。

当前任务: {request}

相关记忆:
{relevant_memory}

对话历史:
{recent_history}

可用工具:
{available_tools}

当前思考过程:
{self.format_short_term_memory()}

请仔细思考如何处理这个任务。考虑:
1. 我是否需要更多信息？
2. 我应该使用哪些工具？
3. 下一步应该做什么？

思考:
"""
        
        return prompt
    
    def build_decision_prompt(self, thought: str) -> str:
        """构建决策提示"""
        prompt = f"""
基于以下思考，请做出决策：

思考内容: {thought}

请选择以下行动之一：

1. 使用工具:
```json
{{
    "type": "use_tool",
    "tool_name": "工具名称",
    "parameters": {{"参数名": "参数值"}},
    "reasoning": "使用此工具的原因"
}}
```

2. 提供最终答案:
```json
{{
    "type": "final_answer",
    "content": "最终回答内容",
    "reasoning": "得出此答案的原因"
}}
```

3. 需要澄清:
```json
{{
    "type": "need_clarification",
    "content": "需要用户澄清的问题",
    "reasoning": "为什么需要澄清"
}}
```

决策:
"""
        
        return prompt
    
    def parse_decision(self, decision_text: str) -> Dict[str, Any]:
        """解析决策文本"""
        try:
            # 尝试提取JSON
            import re
            json_match = re.search(r'```json\s*({.*?})\s*```', decision_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1))
            
            # 如果没有找到JSON，尝试直接解析
            return json.loads(decision_text)
            
        except json.JSONDecodeError:
            # 解析失败，返回默认决策
            return {
                'type': 'final_answer',
                'content': decision_text,
                'reasoning': '无法解析决策格式，直接返回内容'
            }
    
    def update_memory(self, request: str, result: Dict[str, Any]):
        """更新记忆"""
        # 添加到情节记忆
        episode = {
            'request': request,
            'result': result,
            'timestamp': datetime.now(),
            'reasoning_steps': self.memory.short_term.copy()
        }
        self.memory.episodic_memory.append(episode)
        
        # 清理短期记忆
        self.memory.short_term = []
        
        # 更新长期记忆（提取重要信息）
        self.extract_to_long_term_memory(episode)
    
    def get_available_tools_description(self) -> str:
        """获取可用工具描述"""
        if not self.tools:
            return "无可用工具"
        
        descriptions = []
        for tool_name, tool in self.tools.items():
            schema = tool.get_schema()
            descriptions.append(f"- {tool_name}: {tool.description}\n  参数: {schema}")
        
        return "\n".join(descriptions)
```

## 🛠️ 实用工具实现

### 网络搜索工具

```python
import requests
from bs4 import BeautifulSoup

class WebSearchTool(Tool):
    """网络搜索工具"""
    
    def __init__(self, api_key: str):
        super().__init__("web_search", "搜索互联网获取最新信息")
        self.api_key = api_key
    
    def execute(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        query = parameters.get('query', '')
        max_results = parameters.get('max_results', 5)
        
        try:
            # 使用搜索API（这里以Google Custom Search为例）
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                'key': self.api_key,
                'cx': 'your_search_engine_id',
                'q': query,
                'num': max_results
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            results = []
            for item in data.get('items', []):
                results.append({
                    'title': item.get('title', ''),
                    'snippet': item.get('snippet', ''),
                    'link': item.get('link', '')
                })
            
            return {
                'query': query,
                'results': results,
                'total_results': len(results)
            }
            
        except Exception as e:
            return {
                'error': f'搜索失败: {str(e)}',
                'query': query,
                'results': []
            }
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            'query': {'type': 'string', 'description': '搜索查询'},
            'max_results': {'type': 'integer', 'description': '最大结果数', 'default': 5}
        }

class WebScrapeTool(Tool):
    """网页抓取工具"""
    
    def __init__(self):
        super().__init__("web_scrape", "抓取指定网页的内容")
    
    def execute(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        url = parameters.get('url', '')
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 提取主要内容
            title = soup.find('title')
            title_text = title.get_text().strip() if title else ''
            
            # 移除脚本和样式
            for script in soup(["script", "style"]):
                script.decompose()
            
            # 获取文本内容
            text_content = soup.get_text()
            
            # 清理文本
            lines = (line.strip() for line in text_content.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return {
                'url': url,
                'title': title_text,
                'content': text[:5000],  # 限制长度
                'content_length': len(text)
            }
            
        except Exception as e:
            return {
                'error': f'抓取失败: {str(e)}',
                'url': url
            }
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            'url': {'type': 'string', 'description': '要抓取的网页URL'}
        }
```

### 文件操作工具

```python
import os
import json
from pathlib import Path

class FileOperationTool(Tool):
    """文件操作工具"""
    
    def __init__(self, allowed_paths: List[str] = None):
        super().__init__("file_operation", "读取、写入和管理文件")
        self.allowed_paths = allowed_paths or []
    
    def execute(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        operation = parameters.get('operation', '')
        file_path = parameters.get('file_path', '')
        
        # 安全检查
        if not self._is_path_allowed(file_path):
            return {'error': '文件路径不被允许'}
        
        try:
            if operation == 'read':
                return self._read_file(file_path)
            elif operation == 'write':
                content = parameters.get('content', '')
                return self._write_file(file_path, content)
            elif operation == 'list':
                return self._list_directory(file_path)
            elif operation == 'exists':
                return {'exists': os.path.exists(file_path)}
            else:
                return {'error': f'不支持的操作: {operation}'}
                
        except Exception as e:
            return {'error': f'文件操作失败: {str(e)}'}
    
    def _is_path_allowed(self, file_path: str) -> bool:
        """检查路径是否被允许"""
        if not self.allowed_paths:
            return True
        
        abs_path = os.path.abspath(file_path)
        return any(abs_path.startswith(allowed) for allowed in self.allowed_paths)
    
    def _read_file(self, file_path: str) -> Dict[str, Any]:
        """读取文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return {
            'file_path': file_path,
            'content': content,
            'size': len(content)
        }
    
    def _write_file(self, file_path: str, content: str) -> Dict[str, Any]:
        """写入文件"""
        # 确保目录存在
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return {
            'file_path': file_path,
            'bytes_written': len(content.encode('utf-8'))
        }
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            'operation': {
                'type': 'string',
                'enum': ['read', 'write', 'list', 'exists'],
                'description': '文件操作类型'
            },
            'file_path': {'type': 'string', 'description': '文件路径'},
            'content': {'type': 'string', 'description': '写入的内容（仅write操作需要）'}
        }
```

## 🎯 专业智能体实现

### 研究助手智能体

```python
class ResearchAssistantAgent(BaseAgent):
    """研究助手智能体"""
    
    def __init__(self, llm_client, search_api_key: str):
        tools = [
            WebSearchTool(search_api_key),
            WebScrapeTool(),
            FileOperationTool(['/research_data']),
            CitationTool(),
            SummaryTool()
        ]
        
        super().__init__(
            name="ResearchAssistant",
            role="专业研究助手，擅长信息收集、分析和总结",
            llm_client=llm_client,
            tools=tools
        )
        
        # 专业化配置
        self.research_methodology = [
            "确定研究问题",
            "制定搜索策略",
            "收集相关资料",
            "分析和筛选信息",
            "综合总结发现",
            "提供引用和来源"
        ]
    
    def conduct_research(self, topic: str, depth: str = "medium") -> Dict[str, Any]:
        """进行研究"""
        research_plan = self.create_research_plan(topic, depth)
        
        results = {
            'topic': topic,
            'research_plan': research_plan,
            'findings': [],
            'sources': [],
            'summary': '',
            'recommendations': []
        }
        
        # 执行研究计划
        for step in research_plan['steps']:
            step_result = self.execute_research_step(step)
            results['findings'].append(step_result)
        
        # 生成综合报告
        results['summary'] = self.generate_research_summary(results['findings'])
        results['recommendations'] = self.generate_recommendations(results)
        
        return results
    
    def create_research_plan(self, topic: str, depth: str) -> Dict[str, Any]:
        """创建研究计划"""
        planning_prompt = f"""
        为以下研究主题制定详细的研究计划：
        
        主题: {topic}
        深度: {depth}
        
        请提供:
        1. 关键研究问题
        2. 搜索关键词
        3. 信息来源类型
        4. 研究步骤
        
        以JSON格式返回计划。
        """
        
        plan_text = self.llm_client.complete(planning_prompt)
        return json.loads(plan_text)
```

### 创意写作智能体

```python
class CreativeWritingAgent(BaseAgent):
    """创意写作智能体"""
    
    def __init__(self, llm_client):
        tools = [
            ThesaurusTool(),
            StyleAnalysisTool(),
            PlagiarismCheckTool(),
            GrammarCheckTool()
        ]
        
        super().__init__(
            name="CreativeWriter",
            role="专业创意写作助手，擅长各种文体创作",
            llm_client=llm_client,
            tools=tools
        )
        
        self.writing_styles = {
            'narrative': '叙事性写作',
            'descriptive': '描述性写作',
            'persuasive': '说服性写作',
            'expository': '说明性写作'
        }
    
    def create_content(self, prompt: str, style: str, length: int) -> Dict[str, Any]:
        """创建内容"""
        # 分析写作要求
        requirements = self.analyze_writing_requirements(prompt, style, length)
        
        # 生成大纲
        outline = self.create_outline(requirements)
        
        # 逐段写作
        content_sections = []
        for section in outline['sections']:
            section_content = self.write_section(section, requirements)
            content_sections.append(section_content)
        
        # 整合内容
        full_content = self.integrate_content(content_sections)
        
        # 质量检查和优化
        optimized_content = self.optimize_content(full_content, requirements)
        
        return {
            'content': optimized_content,
            'outline': outline,
            'word_count': len(optimized_content.split()),
            'style_analysis': self.analyze_style(optimized_content),
            'quality_score': self.assess_quality(optimized_content)
        }
```

## 🔄 多智能体协作

### 智能体协调器

```python
class AgentCoordinator:
    """智能体协调器"""
    
    def __init__(self, llm_client):
        self.llm_client = llm_client
        self.agents = {}
        self.task_queue = []
        self.collaboration_history = []
    
    def register_agent(self, agent: BaseAgent):
        """注册智能体"""
        self.agents[agent.name] = agent
    
    def coordinate_task(self, task: str, required_capabilities: List[str]) -> Dict[str, Any]:
        """协调任务执行"""
        # 分析任务需求
        task_analysis = self.analyze_task(task, required_capabilities)
        
        # 选择合适的智能体
        selected_agents = self.select_agents(task_analysis)
        
        # 制定协作计划
        collaboration_plan = self.create_collaboration_plan(task_analysis, selected_agents)
        
        # 执行协作任务
        result = self.execute_collaboration(collaboration_plan)
        
        return result
    
    def analyze_task(self, task: str, capabilities: List[str]) -> Dict[str, Any]:
        """分析任务"""
        analysis_prompt = f"""
        分析以下任务，确定需要的能力和执行步骤：
        
        任务: {task}
        所需能力: {capabilities}
        
        可用智能体:
        {self.get_agent_descriptions()}
        
        请提供:
        1. 任务分解
        2. 所需智能体
        3. 执行顺序
        4. 协作方式
        
        以JSON格式返回分析结果。
        """
        
        analysis_text = self.llm_client.complete(analysis_prompt)
        return json.loads(analysis_text)
    
    def execute_collaboration(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """执行协作计划"""
        results = []
        shared_context = {}
        
        for step in plan['steps']:
            agent_name = step['agent']
            task_description = step['task']
            
            if agent_name not in self.agents:
                continue
            
            agent = self.agents[agent_name]
            
            # 更新智能体的上下文
            step_context = {**shared_context, **step.get('context', {})}
            
            # 执行任务
            step_result = agent.process_request(task_description, step_context)
            
            # 更新共享上下文
            shared_context.update(step_result.get('context_updates', {}))
            
            results.append({
                'step': step,
                'agent': agent_name,
                'result': step_result
            })
        
        # 整合最终结果
        final_result = self.integrate_results(results, plan)
        
        return final_result
```

## 📊 智能体监控与优化

### 性能监控

```python
class AgentMonitor:
    """智能体监控系统"""
    
    def __init__(self):
        self.metrics = {}
        self.performance_history = []
        self.alerts = []
    
    def track_agent_performance(self, agent: BaseAgent, task_result: Dict[str, Any]):
        """跟踪智能体性能"""
        agent_name = agent.name
        
        if agent_name not in self.metrics:
            self.metrics[agent_name] = {
                'total_tasks': 0,
                'successful_tasks': 0,
                'average_response_time': 0,
                'tool_usage': {},
                'error_count': 0
            }
        
        metrics = self.metrics[agent_name]
        metrics['total_tasks'] += 1
        
        if task_result.get('success', False):
            metrics['successful_tasks'] += 1
        else:
            metrics['error_count'] += 1
        
        # 更新响应时间
        if 'response_time' in task_result:
            current_avg = metrics['average_response_time']
            new_time = task_result['response_time']
            metrics['average_response_time'] = (
                (current_avg * (metrics['total_tasks'] - 1) + new_time) / metrics['total_tasks']
            )
        
        # 跟踪工具使用
        tools_used = task_result.get('tools_used', [])
        for tool in tools_used:
            metrics['tool_usage'][tool] = metrics['tool_usage'].get(tool, 0) + 1
        
        # 检查告警条件
        self.check_alerts(agent_name, metrics)
    
    def get_performance_report(self, agent_name: str = None) -> Dict[str, Any]:
        """获取性能报告"""
        if agent_name:
            return self.metrics.get(agent_name, {})
        else:
            return self.metrics
    
    def check_alerts(self, agent_name: str, metrics: Dict[str, Any]):
        """检查告警条件"""
        success_rate = metrics['successful_tasks'] / metrics['total_tasks']
        
        if success_rate < 0.8:  # 成功率低于80%
            self.alerts.append({
                'agent': agent_name,
                'type': 'low_success_rate',
                'value': success_rate,
                'timestamp': datetime.now()
            })
        
        if metrics['average_response_time'] > 30:  # 响应时间超过30秒
            self.alerts.append({
                'agent': agent_name,
                'type': 'slow_response',
                'value': metrics['average_response_time'],
                'timestamp': datetime.now()
            })
```

## 🚀 部署与扩展

### 智能体服务化

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

class TaskRequest(BaseModel):
    task: str
    agent_name: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    priority: Optional[str] = "normal"

class AgentService:
    """智能体服务"""
    
    def __init__(self):
        self.app = FastAPI(title="AI Agent Service")
        self.coordinator = AgentCoordinator(llm_client)
        self.monitor = AgentMonitor()
        self.setup_routes()
    
    def setup_routes(self):
        """设置API路由"""
        
        @self.app.post("/agents/{agent_name}/tasks")
        async def execute_task(agent_name: str, request: TaskRequest):
            """执行任务"""
            try:
                if agent_name not in self.coordinator.agents:
                    raise HTTPException(status_code=404, detail="Agent not found")
                
                agent = self.coordinator.agents[agent_name]
                result = agent.process_request(request.task, request.context)
                
                # 记录性能指标
                self.monitor.track_agent_performance(agent, result)
                
                return result
                
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/agents")
        async def list_agents():
            """列出所有智能体"""
            return {
                'agents': [
                    {
                        'name': agent.name,
                        'role': agent.role,
                        'state': agent.state.value,
                        'tools': list(agent.tools.keys())
                    }
                    for agent in self.coordinator.agents.values()
                ]
            }
        
        @self.app.get("/agents/{agent_name}/metrics")
        async def get_agent_metrics(agent_name: str):
            """获取智能体指标"""
            metrics = self.monitor.get_performance_report(agent_name)
            if not metrics:
                raise HTTPException(status_code=404, detail="Agent metrics not found")
            return metrics
    
    def run(self, host: str = "0.0.0.0", port: int = 8000):
        """运行服务"""
        import uvicorn
        uvicorn.run(self.app, host=host, port=port)
```

## 📋 总结

### 智能体架构的优势

1. **自主性**: 能够独立思考和决策
2. **适应性**: 可以处理复杂和变化的任务
3. **创造性**: 能够产生创新的解决方案
4. **学习能力**: 从经验中不断改进
5. **协作能力**: 多个智能体可以协同工作

### 最佳实践

1. **清晰的角色定义**: 为每个智能体定义明确的职责
2. **工具集成**: 提供丰富的工具来扩展能力
3. **记忆管理**: 有效管理短期和长期记忆
4. **错误处理**: 优雅地处理异常情况
5. **性能监控**: 持续监控和优化性能

### 适用场景

- 复杂问题解决
- 创意内容生成
- 研究和分析任务
- 个性化服务
- 动态环境适应

---

> 智能体架构虽然复杂，但在处理开放性、创造性任务时展现出强大的能力。关键是要在复杂性和实用性之间找到平衡，确保系统既智能又可靠。