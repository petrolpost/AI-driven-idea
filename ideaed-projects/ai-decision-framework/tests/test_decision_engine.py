"""AI决策引擎测试"""

import pytest
from datetime import datetime
from main import (
    AIDecisionEngine,
    DecisionRequest,
    ProjectRequirements,
    ResourceConstraints,
    BusinessScenario
)


class TestAIDecisionEngine:
    """AI决策引擎测试类"""
    
    def setup_method(self):
        """测试前置设置"""
        self.engine = AIDecisionEngine()
    
    def test_workflow_recommendation(self):
        """测试工作流架构推荐"""
        # 创建低复杂度项目请求
        request = DecisionRequest(
            project_name="简单数据处理",
            description="批量处理CSV文件",
            requirements=ProjectRequirements(
                task_complexity=2,
                structure_level=1,
                creativity_need=1
            ),
            resources=ResourceConstraints(
                budget_level=2,
                time_urgency=3,
                team_expertise=2
            ),
            scenario=BusinessScenario(
                user_interaction=2
            )
        )
        
        result = self.engine.evaluate_project(request)
        
        assert result.recommendation == "工作流架构"
        assert result.confidence == 0.9
        assert result.total_score <= 15
        assert "工作流" in result.reasoning
    
    def test_agent_recommendation(self):
        """测试智能体架构推荐"""
        # 创建高复杂度项目请求
        request = DecisionRequest(
            project_name="创意内容生成",
            description="AI驱动的创意写作助手",
            requirements=ProjectRequirements(
                task_complexity=5,
                structure_level=5,
                creativity_need=5
            ),
            resources=ResourceConstraints(
                budget_level=4,
                time_urgency=3,
                team_expertise=5
            ),
            scenario=BusinessScenario(
                user_interaction=5
            )
        )
        
        result = self.engine.evaluate_project(request)
        
        assert result.recommendation == "智能体架构"
        assert result.confidence == 0.85
        assert result.total_score >= 25
        assert "智能体" in result.reasoning
    
    def test_hybrid_recommendation(self):
        """测试混合架构推荐"""
        # 创建中等复杂度项目请求
        request = DecisionRequest(
            project_name="智能客服系统",
            description="结合规则和AI的客服系统",
            requirements=ProjectRequirements(
                task_complexity=3,
                structure_level=3,
                creativity_need=3
            ),
            resources=ResourceConstraints(
                budget_level=3,
                time_urgency=3,
                team_expertise=3
            ),
            scenario=BusinessScenario(
                user_interaction=3
            )
        )
        
        result = self.engine.evaluate_project(request)
        
        assert result.recommendation == "混合架构"
        assert result.confidence == 0.8
        assert 15 < result.total_score < 25
        assert "混合" in result.reasoning
    
    def test_suggestions_generation(self):
        """测试建议生成"""
        request = DecisionRequest(
            project_name="测试项目",
            description="测试描述",
            requirements=ProjectRequirements(
                task_complexity=1,
                structure_level=1,
                creativity_need=1
            ),
            resources=ResourceConstraints(
                budget_level=1,  # 低预算
                time_urgency=5,  # 高紧迫性
                team_expertise=1  # 低专业度
            ),
            scenario=BusinessScenario(
                user_interaction=1
            )
        )
        
        result = self.engine.evaluate_project(request)
        
        # 检查是否包含针对性建议
        suggestions_text = " ".join(result.suggestions)
        assert "开源" in suggestions_text  # 低预算建议
        assert "快速" in suggestions_text  # 高紧迫性建议
        assert "培训" in suggestions_text  # 低专业度建议
    
    def test_response_structure(self):
        """测试响应结构完整性"""
        request = DecisionRequest(
            project_name="结构测试",
            description="测试响应结构",
            requirements=ProjectRequirements(
                task_complexity=3,
                structure_level=3,
                creativity_need=3
            ),
            resources=ResourceConstraints(
                budget_level=3,
                time_urgency=3,
                team_expertise=3
            ),
            scenario=BusinessScenario(
                user_interaction=3
            )
        )
        
        result = self.engine.evaluate_project(request)
        
        # 检查响应结构
        assert hasattr(result, 'project_name')
        assert hasattr(result, 'total_score')
        assert hasattr(result, 'recommendation')
        assert hasattr(result, 'confidence')
        assert hasattr(result, 'reasoning')
        assert hasattr(result, 'detailed_scores')
        assert hasattr(result, 'suggestions')
        assert hasattr(result, 'timestamp')
        
        # 检查数据类型
        assert isinstance(result.project_name, str)
        assert isinstance(result.total_score, int)
        assert isinstance(result.recommendation, str)
        assert isinstance(result.confidence, float)
        assert isinstance(result.reasoning, str)
        assert isinstance(result.detailed_scores, dict)
        assert isinstance(result.suggestions, list)
        assert isinstance(result.timestamp, datetime)
        
        # 检查详细得分
        assert "项目需求" in result.detailed_scores
        assert "资源约束" in result.detailed_scores
        assert "业务场景" in result.detailed_scores
    
    def test_score_calculation(self):
        """测试得分计算准确性"""
        request = DecisionRequest(
            project_name="得分测试",
            description="测试得分计算",
            requirements=ProjectRequirements(
                task_complexity=2,
                structure_level=3,
                creativity_need=4
            ),
            resources=ResourceConstraints(
                budget_level=1,
                time_urgency=2,
                team_expertise=3
            ),
            scenario=BusinessScenario(
                user_interaction=5
            )
        )
        
        result = self.engine.evaluate_project(request)
        
        # 验证得分计算
        expected_req_score = 2 + 3 + 4  # 9
        expected_res_score = 1 + 2 + 3  # 6
        expected_scenario_score = 5     # 5
        expected_total = 9 + 6 + 5      # 20
        
        assert result.detailed_scores["项目需求"] == expected_req_score
        assert result.detailed_scores["资源约束"] == expected_res_score
        assert result.detailed_scores["业务场景"] == expected_scenario_score
        assert result.total_score == expected_total


if __name__ == "__main__":
    pytest.main([__file__])