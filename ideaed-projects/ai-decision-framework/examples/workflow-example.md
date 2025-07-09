# 工作流架构示例与最佳实践

本文档提供工作流架构的具体实现示例、设计模式和最佳实践，帮助开发者快速构建可靠的AI工作流系统。

## 🏗️ 基础工作流模板

### 简单线性工作流

```python
from typing import Dict, Any, Optional
from dataclasses import dataclass
import logging
from datetime import datetime

@dataclass
class WorkflowResult:
    """工作流执行结果"""
    success: bool
    data: Any
    error_message: Optional[str] = None
    execution_time: Optional[float] = None
    step_results: Optional[Dict[str, Any]] = None

class BaseWorkflow:
    """基础工作流类"""
    
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(f"workflow.{name}")
        self.step_results = {}
    
    def execute(self, input_data: Dict[str, Any]) -> WorkflowResult:
        """执行工作流"""
        start_time = datetime.now()
        
        try:
            self.logger.info(f"开始执行工作流: {self.name}")
            
            # 输入验证
            validated_input = self.validate_input(input_data)
            
            # 执行工作流步骤
            result = self.run_workflow(validated_input)
            
            # 输出验证
            validated_output = self.validate_output(result)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            self.logger.info(f"工作流执行成功: {self.name}, 耗时: {execution_time}s")
            
            return WorkflowResult(
                success=True,
                data=validated_output,
                execution_time=execution_time,
                step_results=self.step_results
            )
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            error_msg = f"工作流执行失败: {str(e)}"
            self.logger.error(error_msg)
            
            return WorkflowResult(
                success=False,
                data=None,
                error_message=error_msg,
                execution_time=execution_time,
                step_results=self.step_results
            )
    
    def validate_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """输入验证 - 子类需要实现"""
        return input_data
    
    def run_workflow(self, input_data: Dict[str, Any]) -> Any:
        """工作流主逻辑 - 子类需要实现"""
        raise NotImplementedError
    
    def validate_output(self, output_data: Any) -> Any:
        """输出验证 - 子类需要实现"""
        return output_data
    
    def execute_step(self, step_name: str, step_func, *args, **kwargs):
        """执行单个步骤并记录结果"""
        try:
            self.logger.debug(f"执行步骤: {step_name}")
            result = step_func(*args, **kwargs)
            self.step_results[step_name] = {
                'success': True,
                'result': result,
                'timestamp': datetime.now().isoformat()
            }
            return result
        except Exception as e:
            self.step_results[step_name] = {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            raise
```

## 📝 实际应用示例

### 示例1：客户服务工作流

```python
from enum import Enum
from typing import List

class MessageType(Enum):
    BILLING = "billing"
    TECHNICAL = "technical"
    GENERAL = "general"
    COMPLAINT = "complaint"

class CustomerServiceWorkflow(BaseWorkflow):
    """客户服务工作流"""
    
    def __init__(self):
        super().__init__("customer_service")
        self.llm_client = LLMClient()
        self.knowledge_base = KnowledgeBase()
        self.ticket_system = TicketSystem()
    
    def validate_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """验证输入数据"""
        required_fields = ['customer_id', 'message', 'channel']
        for field in required_fields:
            if field not in input_data:
                raise ValueError(f"缺少必需字段: {field}")
        
        # 数据清洗
        input_data['message'] = input_data['message'].strip()
        if len(input_data['message']) == 0:
            raise ValueError("消息内容不能为空")
        
        return input_data
    
    def run_workflow(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """客户服务工作流主逻辑"""
        
        # 步骤1: 获取客户信息
        customer_info = self.execute_step(
            "get_customer_info",
            self.get_customer_info,
            input_data['customer_id']
        )
        
        # 步骤2: 消息分类
        message_type = self.execute_step(
            "classify_message",
            self.classify_message,
            input_data['message']
        )
        
        # 步骤3: 路由处理
        if message_type == MessageType.BILLING:
            response = self.execute_step(
                "handle_billing",
                self.handle_billing_inquiry,
                input_data['message'],
                customer_info
            )
        elif message_type == MessageType.TECHNICAL:
            response = self.execute_step(
                "handle_technical",
                self.handle_technical_inquiry,
                input_data['message'],
                customer_info
            )
        elif message_type == MessageType.COMPLAINT:
            response = self.execute_step(
                "handle_complaint",
                self.handle_complaint,
                input_data['message'],
                customer_info
            )
        else:
            response = self.execute_step(
                "handle_general",
                self.handle_general_inquiry,
                input_data['message']
            )
        
        # 步骤4: 质量检查
        quality_score = self.execute_step(
            "quality_check",
            self.check_response_quality,
            response,
            input_data['message']
        )
        
        # 步骤5: 记录交互
        interaction_id = self.execute_step(
            "log_interaction",
            self.log_customer_interaction,
            input_data['customer_id'],
            message_type,
            response,
            quality_score
        )
        
        return {
            'response': response,
            'message_type': message_type.value,
            'quality_score': quality_score,
            'interaction_id': interaction_id,
            'customer_tier': customer_info.get('tier', 'standard')
        }
    
    def classify_message(self, message: str) -> MessageType:
        """消息分类"""
        classification_prompt = f"""
        请将以下客户消息分类到合适的类别中：
        
        消息: {message}
        
        类别选项:
        - billing: 账单、付款、费用相关
        - technical: 技术问题、产品使用
        - complaint: 投诉、不满
        - general: 一般咨询
        
        只返回类别名称，不要其他内容。
        """
        
        result = self.llm_client.complete(classification_prompt)
        
        # 映射到枚举
        type_mapping = {
            'billing': MessageType.BILLING,
            'technical': MessageType.TECHNICAL,
            'complaint': MessageType.COMPLAINT,
            'general': MessageType.GENERAL
        }
        
        return type_mapping.get(result.strip().lower(), MessageType.GENERAL)
    
    def handle_billing_inquiry(self, message: str, customer_info: Dict) -> str:
        """处理账单咨询"""
        # 获取账单信息
        billing_data = self.get_billing_data(customer_info['customer_id'])
        
        response_prompt = f"""
        客户咨询: {message}
        
        客户信息:
        - 客户ID: {customer_info['customer_id']}
        - 客户等级: {customer_info.get('tier', 'standard')}
        
        账单信息:
        {billing_data}
        
        请提供专业、准确的回复，语气友好。
        """
        
        return self.llm_client.complete(response_prompt)
    
    def handle_technical_inquiry(self, message: str, customer_info: Dict) -> str:
        """处理技术咨询"""
        # 搜索知识库
        relevant_docs = self.knowledge_base.search(message)
        
        response_prompt = f"""
        客户技术问题: {message}
        
        相关文档:
        {relevant_docs}
        
        请基于文档内容提供准确的技术支持回复。
        """
        
        return self.llm_client.complete(response_prompt)
    
    def handle_complaint(self, message: str, customer_info: Dict) -> str:
        """处理投诉"""
        # 创建投诉工单
        ticket_id = self.ticket_system.create_complaint_ticket(
            customer_info['customer_id'],
            message
        )
        
        response_prompt = f"""
        客户投诉: {message}
        
        请提供同理心强、专业的回复，表达歉意并说明后续处理流程。
        工单号: {ticket_id}
        """
        
        return self.llm_client.complete(response_prompt)
    
    def check_response_quality(self, response: str, original_message: str) -> float:
        """检查回复质量"""
        quality_prompt = f"""
        评估以下客服回复的质量（0-1分）：
        
        客户问题: {original_message}
        客服回复: {response}
        
        评估标准:
        - 相关性 (是否回答了问题)
        - 准确性 (信息是否正确)
        - 专业性 (语言是否专业)
        - 友好性 (语气是否友好)
        
        只返回数字分数，如: 0.85
        """
        
        result = self.llm_client.complete(quality_prompt)
        try:
            return float(result.strip())
        except ValueError:
            return 0.5  # 默认分数
```

### 示例2：内容生成工作流

```python
class ContentGenerationWorkflow(BaseWorkflow):
    """内容生成工作流"""
    
    def __init__(self):
        super().__init__("content_generation")
        self.llm_client = LLMClient()
        self.style_guide = StyleGuide()
        self.content_validator = ContentValidator()
    
    def run_workflow(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """内容生成工作流"""
        
        # 步骤1: 内容规划
        content_plan = self.execute_step(
            "plan_content",
            self.plan_content,
            input_data['topic'],
            input_data['target_audience'],
            input_data['content_type']
        )
        
        # 步骤2: 生成初稿
        draft_content = self.execute_step(
            "generate_draft",
            self.generate_draft,
            content_plan
        )
        
        # 步骤3: 风格检查
        style_checked_content = self.execute_step(
            "style_check",
            self.apply_style_guide,
            draft_content,
            input_data.get('brand_voice', 'professional')
        )
        
        # 步骤4: 内容验证
        validation_result = self.execute_step(
            "validate_content",
            self.validate_content,
            style_checked_content
        )
        
        # 步骤5: 最终优化
        final_content = self.execute_step(
            "optimize_content",
            self.optimize_content,
            style_checked_content,
            validation_result
        )
        
        return {
            'content': final_content,
            'word_count': len(final_content.split()),
            'validation_score': validation_result['score'],
            'content_plan': content_plan
        }
    
    def plan_content(self, topic: str, audience: str, content_type: str) -> Dict[str, Any]:
        """内容规划"""
        planning_prompt = f"""
        为以下内容创建详细的写作计划：
        
        主题: {topic}
        目标受众: {audience}
        内容类型: {content_type}
        
        请提供:
        1. 核心要点 (3-5个)
        2. 内容结构
        3. 关键词建议
        4. 预估字数
        
        以JSON格式返回。
        """
        
        result = self.llm_client.complete(planning_prompt)
        return json.loads(result)
```

## 🔧 高级模式与最佳实践

### 条件分支工作流

```python
class ConditionalWorkflow(BaseWorkflow):
    """支持条件分支的工作流"""
    
    def run_workflow(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        # 条件评估
        condition_result = self.execute_step(
            "evaluate_condition",
            self.evaluate_condition,
            input_data
        )
        
        # 根据条件选择不同的处理路径
        if condition_result['priority'] == 'high':
            return self.handle_high_priority(input_data)
        elif condition_result['priority'] == 'medium':
            return self.handle_medium_priority(input_data)
        else:
            return self.handle_low_priority(input_data)
```

### 并行处理工作流

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

class ParallelWorkflow(BaseWorkflow):
    """支持并行处理的工作流"""
    
    def __init__(self, name: str, max_workers: int = 4):
        super().__init__(name)
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
    
    async def run_parallel_steps(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """并行执行多个步骤"""
        
        # 创建并行任务
        tasks = [
            self.async_step("process_text", self.process_text, input_data['text']),
            self.async_step("analyze_sentiment", self.analyze_sentiment, input_data['text']),
            self.async_step("extract_keywords", self.extract_keywords, input_data['text'])
        ]
        
        # 等待所有任务完成
        results = await asyncio.gather(*tasks)
        
        return {
            'processed_text': results[0],
            'sentiment': results[1],
            'keywords': results[2]
        }
    
    async def async_step(self, step_name: str, func, *args):
        """异步执行步骤"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, func, *args)
```

### 错误处理与重试机制

```python
import time
from functools import wraps

def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """重试装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries:
                        time.sleep(delay * (2 ** attempt))  # 指数退避
                        continue
                    else:
                        raise last_exception
            
        return wrapper
    return decorator

class RobustWorkflow(BaseWorkflow):
    """具有错误处理和重试机制的工作流"""
    
    @retry_on_failure(max_retries=3)
    def call_external_api(self, data):
        """调用外部API（带重试）"""
        # API调用逻辑
        pass
    
    def run_workflow(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # 主要处理逻辑
            result = self.main_processing(input_data)
            return result
        
        except CriticalError as e:
            # 关键错误，立即失败
            raise e
        
        except RetryableError as e:
            # 可重试错误，使用降级策略
            self.logger.warning(f"使用降级策略: {str(e)}")
            return self.fallback_processing(input_data)
        
        except Exception as e:
            # 未知错误，记录并使用默认响应
            self.logger.error(f"未知错误: {str(e)}")
            return self.default_response(input_data)
```

## 📊 监控与可观测性

### 工作流监控

```python
import time
from dataclasses import dataclass
from typing import List

@dataclass
class WorkflowMetrics:
    """工作流指标"""
    workflow_name: str
    execution_time: float
    success_rate: float
    step_timings: Dict[str, float]
    error_count: int
    throughput: float

class MonitoredWorkflow(BaseWorkflow):
    """带监控的工作流"""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.metrics_collector = MetricsCollector()
        self.alerting = AlertingSystem()
    
    def execute(self, input_data: Dict[str, Any]) -> WorkflowResult:
        # 记录开始时间
        start_time = time.time()
        
        # 执行工作流
        result = super().execute(input_data)
        
        # 记录指标
        execution_time = time.time() - start_time
        self.metrics_collector.record_execution(
            workflow_name=self.name,
            execution_time=execution_time,
            success=result.success,
            step_results=result.step_results
        )
        
        # 检查告警条件
        if execution_time > self.get_sla_threshold():
            self.alerting.send_alert(
                f"工作流 {self.name} 执行时间超过SLA: {execution_time}s"
            )
        
        return result
    
    def get_metrics(self) -> WorkflowMetrics:
        """获取工作流指标"""
        return self.metrics_collector.get_metrics(self.name)
```

## 🚀 部署与运维

### 配置管理

```python
from pydantic import BaseSettings

class WorkflowConfig(BaseSettings):
    """工作流配置"""
    llm_api_key: str
    llm_model: str = "gpt-3.5-turbo"
    max_retries: int = 3
    timeout_seconds: int = 30
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"

# 使用配置
config = WorkflowConfig()
workflow = CustomerServiceWorkflow(config)
```

### 健康检查

```python
class WorkflowHealthChecker:
    """工作流健康检查"""
    
    def __init__(self, workflow: BaseWorkflow):
        self.workflow = workflow
    
    def health_check(self) -> Dict[str, Any]:
        """执行健康检查"""
        checks = {
            'workflow_status': self.check_workflow_status(),
            'dependencies': self.check_dependencies(),
            'performance': self.check_performance()
        }
        
        overall_health = all(check['healthy'] for check in checks.values())
        
        return {
            'healthy': overall_health,
            'checks': checks,
            'timestamp': datetime.now().isoformat()
        }
    
    def check_workflow_status(self) -> Dict[str, Any]:
        """检查工作流状态"""
        try:
            # 执行简单的测试
            test_result = self.workflow.execute({'test': True})
            return {
                'healthy': test_result.success,
                'message': 'Workflow responding normally'
            }
        except Exception as e:
            return {
                'healthy': False,
                'message': f'Workflow error: {str(e)}'
            }
```

## 📋 总结

### 工作流架构的优势

1. **可预测性**: 明确的执行路径和结果
2. **可调试性**: 清晰的步骤和错误追踪
3. **可维护性**: 模块化设计，易于修改
4. **成本可控**: 可预测的资源消耗
5. **稳定性**: 经过验证的执行模式

### 最佳实践总结

1. **输入输出验证**: 确保数据质量
2. **错误处理**: 完善的异常处理机制
3. **监控告警**: 实时监控系统状态
4. **配置管理**: 灵活的配置系统
5. **测试覆盖**: 全面的单元测试和集成测试

### 适用场景

- 标准化业务流程
- 高可靠性要求
- 成本敏感应用
- 合规性要求严格
- 团队AI经验有限

---

> 工作流架构虽然看起来不如智能体"智能"，但在大多数实际业务场景中，它提供了更好的可靠性、可维护性和成本效益。选择合适的架构，而不是最新的架构，才是明智的决策。