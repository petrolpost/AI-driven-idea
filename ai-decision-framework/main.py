#!/usr/bin/env python3
"""
AI决策框架主应用
基于FastAPI的Web服务，提供AI工作流vs智能体的决策支持

作者: AI决策框架项目组
版本: 1.0.0
许可: MIT
"""

import os
import logging
from typing import Dict, Any, Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel, Field, ConfigDict
from pydantic_settings import BaseSettings

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 应用配置
class Settings(BaseSettings):
    """应用设置"""
    app_name: str = "AI Decision Framework"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = True
    host: str = "localhost"
    port: int = 8000
    
    # LLM配置
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4"
    openai_temperature: float = 0.7
    
    # 混合处理器配置
    auto_mode_enabled: bool = True
    quality_threshold: float = 0.8
    max_retries: int = 2
    max_parallel_workers: int = 4
    task_timeout_seconds: int = 60
    
    # 监控配置
    enable_monitoring: bool = True
    alert_success_rate_threshold: float = 0.9
    alert_quality_threshold: float = 0.7
    alert_response_time_threshold: float = 30.0
    
    model_config = ConfigDict(env_file=".env", extra="ignore")

settings = Settings()

# 创建FastAPI应用
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI工作流vs智能体决策框架 - 帮助选择最适合的AI架构",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.debug else ["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件（如果存在）
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# 数据模型
class ProjectRequirements(BaseModel):
    """项目需求模型"""
    task_complexity: int = Field(..., ge=1, le=5, description="任务复杂度 (1-5)")
    structure_level: int = Field(..., ge=1, le=5, description="结构化程度 (1-5)")
    creativity_need: int = Field(..., ge=1, le=5, description="创造性需求 (1-5)")
    
class ResourceConstraints(BaseModel):
    """资源约束模型"""
    budget_level: int = Field(..., ge=1, le=5, description="预算水平 (1-5)")
    time_urgency: int = Field(..., ge=1, le=5, description="时间紧迫性 (1-5)")
    team_expertise: int = Field(..., ge=1, le=5, description="团队专业度 (1-5)")
    
class BusinessScenario(BaseModel):
    """业务场景模型"""
    user_interaction: int = Field(..., ge=1, le=5, description="用户交互复杂度 (1-5)")
    
class DecisionRequest(BaseModel):
    """决策请求模型"""
    project_name: str = Field(..., description="项目名称")
    description: str = Field(..., description="项目描述")
    requirements: ProjectRequirements
    resources: ResourceConstraints
    scenario: BusinessScenario
    
class DecisionResponse(BaseModel):
    """决策响应模型"""
    project_name: str
    total_score: int
    recommendation: str
    confidence: float
    reasoning: str
    detailed_scores: Dict[str, int]
    suggestions: list[str]
    timestamp: datetime

# 决策引擎
class AIDecisionEngine:
    """AI决策引擎"""
    
    def __init__(self):
        self.workflow_threshold = 15  # 工作流推荐阈值
        self.agent_threshold = 25     # 智能体推荐阈值
        
    def evaluate_project(self, request: DecisionRequest) -> DecisionResponse:
        """评估项目并给出建议"""
        
        # 计算各维度得分
        req_score = (
            request.requirements.task_complexity +
            request.requirements.structure_level +
            request.requirements.creativity_need
        )
        
        res_score = (
            request.resources.budget_level +
            request.resources.time_urgency +
            request.resources.team_expertise
        )
        
        scenario_score = request.scenario.user_interaction
        
        total_score = req_score + res_score + scenario_score
        
        # 决策逻辑
        if total_score <= self.workflow_threshold:
            recommendation = "工作流架构"
            confidence = 0.9
            reasoning = "项目具有高度结构化特征，适合使用可预测的工作流架构"
        elif total_score >= self.agent_threshold:
            recommendation = "智能体架构"
            confidence = 0.85
            reasoning = "项目需要高度灵活性和创造性，适合使用自主智能体架构"
        else:
            recommendation = "混合架构"
            confidence = 0.8
            reasoning = "项目特征介于两者之间，建议采用混合架构以平衡稳定性和灵活性"
        
        # 生成建议
        suggestions = self._generate_suggestions(request, recommendation)
        
        return DecisionResponse(
            project_name=request.project_name,
            total_score=total_score,
            recommendation=recommendation,
            confidence=confidence,
            reasoning=reasoning,
            detailed_scores={
                "项目需求": req_score,
                "资源约束": res_score,
                "业务场景": scenario_score
            },
            suggestions=suggestions,
            timestamp=datetime.now()
        )
    
    def _generate_suggestions(self, request: DecisionRequest, recommendation: str) -> list[str]:
        """生成具体建议"""
        suggestions = []
        
        if recommendation == "工作流架构":
            suggestions.extend([
                "使用标准化的步骤和流程",
                "重点关注错误处理和重试机制",
                "建立清晰的输入输出规范",
                "考虑使用现有的工作流引擎"
            ])
        elif recommendation == "智能体架构":
            suggestions.extend([
                "设计灵活的推理和决策机制",
                "提供丰富的工具和API接口",
                "建立有效的监控和调试系统",
                "考虑多智能体协作模式"
            ])
        else:  # 混合架构
            suggestions.extend([
                "为标准化任务使用工作流",
                "为复杂决策使用智能体",
                "建立智能路由机制",
                "设计统一的监控和管理界面"
            ])
        
        # 基于具体评分添加建议
        if request.resources.budget_level <= 2:
            suggestions.append("考虑使用开源解决方案以控制成本")
        
        if request.resources.time_urgency >= 4:
            suggestions.append("优先考虑快速部署和迭代")
        
        if request.resources.team_expertise <= 2:
            suggestions.append("建议提供充分的培训和文档支持")
        
        return suggestions

# 创建决策引擎实例
decision_engine = AIDecisionEngine()

# 应用统计
app_stats = {
    "total_evaluations": 0,
    "workflow_recommendations": 0,
    "agent_recommendations": 0,
    "hybrid_recommendations": 0,
    "start_time": datetime.now()
}

# API路由
@app.get("/", response_class=HTMLResponse)
async def root():
    """主页 - 返回评分网页"""
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(
            content="<h1>AI决策框架</h1><p>请访问 /docs 查看API文档</p>"
        )

@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "version": settings.app_version,
        "environment": settings.environment
    }

@app.get("/stats")
async def get_stats():
    """获取应用统计信息"""
    uptime = datetime.now() - app_stats["start_time"]
    
    return {
        "uptime_seconds": uptime.total_seconds(),
        "total_evaluations": app_stats["total_evaluations"],
        "recommendations": {
            "workflow": app_stats["workflow_recommendations"],
            "agent": app_stats["agent_recommendations"],
            "hybrid": app_stats["hybrid_recommendations"]
        },
        "settings": {
            "auto_mode_enabled": settings.auto_mode_enabled,
            "quality_threshold": settings.quality_threshold,
            "monitoring_enabled": settings.enable_monitoring
        }
    }

@app.post("/evaluate", response_model=DecisionResponse)
async def evaluate_project(request: DecisionRequest, background_tasks: BackgroundTasks):
    """评估项目并给出AI架构建议"""
    try:
        # 执行决策评估
        result = decision_engine.evaluate_project(request)
        
        # 更新统计信息
        background_tasks.add_task(update_stats, result.recommendation)
        
        logger.info(f"项目评估完成: {request.project_name} -> {result.recommendation}")
        
        return result
        
    except Exception as e:
        logger.error(f"项目评估失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"评估失败: {str(e)}")

@app.get("/recommendations/{recommendation_type}")
async def get_recommendation_details(recommendation_type: str):
    """获取特定架构类型的详细信息"""
    
    details = {
        "workflow": {
            "name": "工作流架构",
            "description": "基于预定义步骤的结构化处理方式",
            "advantages": [
                "高可靠性和可预测性",
                "易于调试和维护",
                "性能稳定",
                "成本可控"
            ],
            "use_cases": [
                "数据处理管道",
                "标准化业务流程",
                "批量任务处理",
                "合规性要求高的场景"
            ],
            "implementation_tips": [
                "明确定义每个步骤的输入输出",
                "设计完善的错误处理机制",
                "使用成熟的工作流引擎",
                "建立监控和告警系统"
            ]
        },
        "agent": {
            "name": "智能体架构",
            "description": "具有自主决策能力的智能系统",
            "advantages": [
                "高度灵活和适应性",
                "能处理复杂和开放性问题",
                "具备学习和推理能力",
                "用户体验更自然"
            ],
            "use_cases": [
                "智能客服和助手",
                "创意内容生成",
                "复杂问题解决",
                "个性化推荐"
            ],
            "implementation_tips": [
                "设计清晰的目标和约束",
                "提供丰富的工具和知识库",
                "建立有效的监控机制",
                "考虑多智能体协作"
            ]
        },
        "hybrid": {
            "name": "混合架构",
            "description": "结合工作流和智能体优势的综合方案",
            "advantages": [
                "平衡稳定性和灵活性",
                "适应多样化需求",
                "风险分散",
                "渐进式优化"
            ],
            "use_cases": [
                "企业级应用系统",
                "多功能平台",
                "复杂业务场景",
                "需要持续演进的系统"
            ],
            "implementation_tips": [
                "建立智能路由机制",
                "设计统一的接口标准",
                "实现无缝的模式切换",
                "建立综合监控体系"
            ]
        }
    }
    
    if recommendation_type not in details:
        raise HTTPException(status_code=404, detail="未找到指定的架构类型")
    
    return details[recommendation_type]

# 后台任务
def update_stats(recommendation: str):
    """更新统计信息"""
    app_stats["total_evaluations"] += 1
    
    if recommendation == "工作流架构":
        app_stats["workflow_recommendations"] += 1
    elif recommendation == "智能体架构":
        app_stats["agent_recommendations"] += 1
    elif recommendation == "混合架构":
        app_stats["hybrid_recommendations"] += 1

# 启动配置
if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"启动 {settings.app_name} v{settings.app_version}")
    logger.info(f"环境: {settings.environment}")
    logger.info(f"调试模式: {settings.debug}")
    
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info" if settings.debug else "warning"
    )