"""
Tests for the AI Swarm Orchestrator
"""

import pytest
from orchestrator import (
    SwarmOrchestrator,
    UserFramework,
    Boundary,
    BoundaryType,
    ConfidenceLevel,
    KnowledgeGap,
)


class TestSwarmOrchestrator:
    """Test suite for SwarmOrchestrator"""
    
    def test_initialization(self):
        """Test orchestrator initializes correctly"""
        orchestrator = SwarmOrchestrator()
        assert orchestrator.user_framework is not None
        assert orchestrator.boundaries == []
        assert orchestrator.knowledge_gaps == []
        assert orchestrator.decisions == []
    
    def test_add_boundary(self):
        """Test adding boundaries"""
        orchestrator = SwarmOrchestrator()
        
        budget_boundary = Boundary(
            type=BoundaryType.BUDGET,
            description="Maximum project budget",
            value=10000,
            is_hard_limit=True
        )
        
        orchestrator.add_boundary(budget_boundary)
        assert len(orchestrator.boundaries) == 1
        assert orchestrator.boundaries[0].type == BoundaryType.BUDGET
    
    def test_update_user_framework(self):
        """Test updating user framework"""
        orchestrator = SwarmOrchestrator()
        
        orchestrator.update_user_framework(
            goals=["Increase efficiency", "Reduce costs"],
            values=["Transparency", "Quality"],
            intent="Optimize business processes"
        )
        
        assert len(orchestrator.user_framework.goals) == 2
        assert "Increase efficiency" in orchestrator.user_framework.goals
        assert len(orchestrator.user_framework.values) == 2
        assert orchestrator.user_framework.intent == "Optimize business processes"
    
    def test_identify_knowledge_gaps_empty_framework(self):
        """Test knowledge gap identification with empty framework"""
        orchestrator = SwarmOrchestrator()
        
        gaps = orchestrator.identify_knowledge_gaps("Build a new application")
        
        # Should identify missing goals, values, and intent
        gap_areas = [g.area for g in gaps]
        assert "goals" in gap_areas
        assert "values" in gap_areas
        assert "intent" in gap_areas
    
    def test_identify_knowledge_gaps_budget_request(self):
        """Test knowledge gap identification for budget-related requests"""
        orchestrator = SwarmOrchestrator()
        
        # Set up basic framework but no budget boundary
        orchestrator.update_user_framework(
            goals=["Test goal"],
            values=["Test value"],
            intent="Test intent"
        )
        
        gaps = orchestrator.identify_knowledge_gaps("How much will this cost?")
        
        # Should identify missing budget boundary
        gap_areas = [g.area for g in gaps]
        assert "budget" in gap_areas
    
    def test_generate_clarification_questions(self):
        """Test generation of clarification questions"""
        orchestrator = SwarmOrchestrator()
        
        gaps = orchestrator.identify_knowledge_gaps("Create a system")
        questions = orchestrator.generate_clarification_questions(gaps)
        
        assert len(questions) > 0
        assert all(q.question for q in questions)
        assert all(q.context for q in questions)
    
    def test_check_boundaries_within_budget(self):
        """Test boundary checking - within budget"""
        orchestrator = SwarmOrchestrator()
        
        orchestrator.add_boundary(Boundary(
            type=BoundaryType.BUDGET,
            description="Project budget",
            value=5000
        ))
        
        within, violations = orchestrator.check_boundaries(
            "Deploy system",
            {"cost": 3000}
        )
        
        assert within is True
        assert len(violations) == 0
    
    def test_check_boundaries_exceeds_budget(self):
        """Test boundary checking - exceeds budget"""
        orchestrator = SwarmOrchestrator()
        
        orchestrator.add_boundary(Boundary(
            type=BoundaryType.BUDGET,
            description="Project budget",
            value=5000
        ))
        
        within, violations = orchestrator.check_boundaries(
            "Deploy system",
            {"cost": 8000}
        )
        
        assert within is False
        assert len(violations) == 1
        assert "exceeds budget" in violations[0].lower()
    
    def test_calculate_confidence_high(self):
        """Test confidence calculation - high confidence"""
        orchestrator = SwarmOrchestrator()
        
        # Set up complete framework
        orchestrator.update_user_framework(
            goals=["Goal 1"],
            values=["Value 1"],
            intent="Clear intent"
        )
        
        orchestrator.add_boundary(Boundary(
            type=BoundaryType.BUDGET,
            description="Budget",
            value=10000
        ))
        
        confidence = orchestrator.calculate_confidence(
            "Execute task",
            {"cost": 5000}
        )
        
        assert confidence == ConfidenceLevel.HIGH
    
    def test_calculate_confidence_low(self):
        """Test confidence calculation - low confidence"""
        orchestrator = SwarmOrchestrator()
        
        # Empty framework
        confidence = orchestrator.calculate_confidence(
            "Execute task",
            {"cost": 5000}
        )
        
        assert confidence == ConfidenceLevel.LOW
    
    def test_make_decision_requires_confirmation(self):
        """Test decision making when confirmation is required"""
        orchestrator = SwarmOrchestrator()
        
        # Incomplete framework should require confirmation
        decision = orchestrator.make_decision(
            "Deploy application",
            "deploy",
            {"cost": 1000}
        )
        
        assert decision.requires_confirmation is True
        assert decision.confidence == ConfidenceLevel.LOW
    
    def test_make_decision_confident(self):
        """Test decision making with high confidence"""
        orchestrator = SwarmOrchestrator()
        
        # Set up complete framework
        orchestrator.update_user_framework(
            goals=["Deploy successfully"],
            values=["Reliability"],
            intent="Launch new feature"
        )
        
        orchestrator.add_boundary(Boundary(
            type=BoundaryType.BUDGET,
            description="Budget",
            value=10000
        ))
        
        decision = orchestrator.make_decision(
            "Deploy application",
            "deploy",
            {"cost": 5000}
        )
        
        assert decision.confidence == ConfidenceLevel.HIGH
        assert decision.framework_alignment["goals_aligned"] is True
        assert decision.framework_alignment["values_aligned"] is True
        assert decision.framework_alignment["intent_clear"] is True
    
    def test_process_request_needs_clarification(self):
        """Test processing request that needs clarification"""
        orchestrator = SwarmOrchestrator()
        
        result = orchestrator.process_request("Build a new system")
        
        assert result["status"] == "needs_clarification"
        assert "knowledge_gaps" in result
        assert "clarification_questions" in result
        assert len(result["clarification_questions"]) > 0
    
    def test_process_request_ready_for_decision(self):
        """Test processing request when ready for decision"""
        orchestrator = SwarmOrchestrator()
        
        # Set up framework
        orchestrator.update_user_framework(
            goals=["Complete project"],
            values=["Quality"],
            intent="Deliver value"
        )
        
        result = orchestrator.process_request("Proceed with development")
        
        assert result["status"] == "ready_for_decision"
        assert "user_framework" in result
    
    def test_can_act_confidently_false(self):
        """Test can_act_confidently returns False with incomplete framework"""
        orchestrator = SwarmOrchestrator()
        
        assert orchestrator.can_act_confidently() is False
    
    def test_can_act_confidently_true(self):
        """Test can_act_confidently returns True with complete framework"""
        orchestrator = SwarmOrchestrator()
        
        orchestrator.update_user_framework(
            goals=["Goal 1"],
            values=["Value 1"],
            intent="Clear intent"
        )
        
        assert orchestrator.can_act_confidently() is True
    
    def test_ethical_boundary_violation(self):
        """Test ethical boundary checking"""
        orchestrator = SwarmOrchestrator()
        
        orchestrator.add_boundary(Boundary(
            type=BoundaryType.ETHICAL,
            description="Ethical guidelines",
            value="no_harm"
        ))
        
        within, violations = orchestrator.check_boundaries(
            "Execute action",
            {"ethical_concerns": ["potential harm to users"]}
        )
        
        assert within is False
        assert len(violations) == 1
        assert "ethical concerns" in violations[0].lower()
    
    def test_temporal_boundary(self):
        """Test temporal boundary checking"""
        orchestrator = SwarmOrchestrator()
        
        orchestrator.add_boundary(Boundary(
            type=BoundaryType.TEMPORAL,
            description="Maximum execution time",
            value=3600  # 1 hour in seconds
        ))
        
        # Within boundary
        within, violations = orchestrator.check_boundaries(
            "Run analysis",
            {"duration": 1800}
        )
        assert within is True
        
        # Exceeds boundary
        within, violations = orchestrator.check_boundaries(
            "Run analysis",
            {"duration": 7200}
        )
        assert within is False
    
    def test_knowledge_gap_priority(self):
        """Test that knowledge gaps have appropriate priority"""
        orchestrator = SwarmOrchestrator()
        
        gaps = orchestrator.identify_knowledge_gaps("Execute critical task")
        
        # Critical gaps should have high priority
        critical_gaps = [g for g in gaps if g.required_for_action]
        assert all(g.priority == "high" for g in critical_gaps)
    
    def test_multiple_boundaries(self):
        """Test checking multiple boundaries simultaneously"""
        orchestrator = SwarmOrchestrator()
        
        orchestrator.add_boundary(Boundary(
            type=BoundaryType.BUDGET,
            description="Budget limit",
            value=5000
        ))
        
        orchestrator.add_boundary(Boundary(
            type=BoundaryType.TEMPORAL,
            description="Time limit",
            value=3600
        ))
        
        # Violates both
        within, violations = orchestrator.check_boundaries(
            "Execute action",
            {"cost": 10000, "duration": 7200}
        )
        
        assert within is False
        assert len(violations) == 2


class TestUserFramework:
    """Test UserFramework model"""
    
    def test_user_framework_initialization(self):
        """Test UserFramework initializes with defaults"""
        framework = UserFramework()
        assert framework.goals == []
        assert framework.values == []
        assert framework.intent == ""
        assert framework.mental_model == {}
        assert framework.context == {}
    
    def test_user_framework_with_data(self):
        """Test UserFramework with initial data"""
        framework = UserFramework(
            goals=["Goal 1", "Goal 2"],
            values=["Value 1"],
            intent="Test intent",
            mental_model={"preference": "quality"},
            context={"domain": "software"}
        )
        
        assert len(framework.goals) == 2
        assert len(framework.values) == 1
        assert framework.intent == "Test intent"
        assert framework.mental_model["preference"] == "quality"
        assert framework.context["domain"] == "software"


class TestBoundary:
    """Test Boundary model"""
    
    def test_boundary_creation(self):
        """Test creating different types of boundaries"""
        budget = Boundary(
            type=BoundaryType.BUDGET,
            description="Max budget",
            value=10000
        )
        assert budget.type == BoundaryType.BUDGET
        assert budget.is_hard_limit is True
        
        ethical = Boundary(
            type=BoundaryType.ETHICAL,
            description="Ethical guidelines",
            value="privacy_first",
            is_hard_limit=False
        )
        assert ethical.type == BoundaryType.ETHICAL
        assert ethical.is_hard_limit is False


class TestKnowledgeGap:
    """Test KnowledgeGap model"""
    
    def test_knowledge_gap_creation(self):
        """Test creating knowledge gaps"""
        gap = KnowledgeGap(
            area="budget",
            description="Budget not specified",
            priority="high",
            required_for_action=True
        )
        
        assert gap.area == "budget"
        assert gap.priority == "high"
        assert gap.required_for_action is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
