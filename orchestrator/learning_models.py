"""
Advanced learning models for preference understanding and meta-reasoning
"""

from typing import List, Dict, Any, Optional, Set
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime


class DecisionContext(BaseModel):
    """Context in which a decision was made"""
    situation: str
    available_options: List[str]
    constraints: Dict[str, Any] = Field(default_factory=dict)
    user_state: Dict[str, Any] = Field(default_factory=dict)  # mood, urgency, etc.


class DecisionOutcome(BaseModel):
    """Record of an actual decision made"""
    chosen_option: str
    rejected_options: List[str] = Field(default_factory=list)
    context: DecisionContext
    timestamp: datetime = Field(default_factory=datetime.now)
    explicit_reasoning: Optional[str] = None  # If user explained why
    observed_satisfaction: Optional[float] = None  # 0-1 scale if measurable


class ReasoningPattern(BaseModel):
    """Identified pattern in user's decision-making"""
    pattern_type: str  # "value_priority", "risk_tolerance", "cost_benefit_ratio", etc.
    pattern_description: str
    confidence: float  # 0-1, how sure we are about this pattern
    evidence: List[str] = Field(default_factory=list)  # Decision IDs that support this
    counter_evidence: List[str] = Field(default_factory=list)  # Exceptions
    
    def strength(self) -> float:
        """Calculate pattern strength based on evidence"""
        total = len(self.evidence) + len(self.counter_evidence)
        if total == 0:
            return 0.0
        return (len(self.evidence) / total) * self.confidence


class GapRootCause(str, Enum):
    """Root causes for knowledge gaps"""
    MISSING_VALUE_PRIORITY = "missing_value_priority"  # Don't know which value matters more
    MISSING_GOAL_CONTEXT = "missing_goal_context"  # Don't know why this goal exists
    CONFLICTING_PATTERNS = "conflicting_patterns"  # User's past decisions contradict
    INSUFFICIENT_EXAMPLES = "insufficient_examples"  # Haven't seen this situation before
    AMBIGUOUS_TRADEOFF = "ambiguous_tradeoff"  # Don't know how user trades off X vs Y
    MISSING_CONSTRAINT_IMPORTANCE = "missing_constraint_importance"  # Don't know if boundary is flexible
    UNCLEAR_SUCCESS_METRIC = "unclear_success_metric"  # Don't know what "good" looks like
    CONTEXT_DEPENDENCY = "context_dependency"  # Preference varies with context but don't know how


class EnhancedKnowledgeGap(BaseModel):
    """Enhanced gap analysis with root cause understanding"""
    area: str  # What's missing (e.g., "budget preference")
    description: str  # Human-readable description
    root_cause: GapRootCause  # WHY this gap matters
    impact_on_decision: str  # How this gap affects current decision
    priority: str = "medium"
    required_for_action: bool = False
    
    # Meta-reasoning
    blocking_decision_types: List[str] = Field(default_factory=list)  # What decisions this blocks
    related_patterns: List[str] = Field(default_factory=list)  # Patterns that might help
    suggested_resolution: str = ""  # How to fill this gap
    
    # For tracking
    times_encountered: int = 1
    last_encountered: datetime = Field(default_factory=datetime.now)


class PreferenceHypothesis(BaseModel):
    """A hypothesis about user preferences"""
    hypothesis: str  # "User prefers X when Y"
    confidence: float  # 0-1
    supporting_evidence: List[str] = Field(default_factory=list)
    contradicting_evidence: List[str] = Field(default_factory=list)
    domain: str = "general"  # Which area this applies to
    created_at: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)
    
    def update_confidence(self):
        """Recalculate confidence based on evidence"""
        total = len(self.supporting_evidence) + len(self.contradicting_evidence)
        if total == 0:
            self.confidence = 0.5  # No evidence, neutral
        else:
            support_ratio = len(self.supporting_evidence) / total
            # Adjust confidence based on evidence and total observations
            certainty_factor = min(total / 10, 1.0)  # More examples = more certain
            self.confidence = 0.5 + (support_ratio - 0.5) * certainty_factor
        self.last_updated = datetime.now()


class ProgressUpdate(BaseModel):
    """High-level progress report for user"""
    stage: str  # "learning", "planning", "executing", "reviewing"
    summary: str  # Big picture status
    key_insights: List[str] = Field(default_factory=list)  # Important learnings
    confidence_level: str = "medium"  # Overall confidence
    alignment_check: str = ""  # "Everything aligned" or concerns
    next_steps: List[str] = Field(default_factory=list)  # What's coming
    questions_for_user: List[str] = Field(default_factory=list)  # If any
    timestamp: datetime = Field(default_factory=datetime.now)


class FrameworkCompleteness(BaseModel):
    """Quantitative measure of how well we understand the user"""
    overall_score: float  # 0-1
    dimension_scores: Dict[str, float] = Field(default_factory=dict)
    # e.g., {"goal_clarity": 0.8, "value_hierarchy": 0.6, "constraint_flexibility": 0.4}
    
    identified_patterns: int = 0
    decision_history_size: int = 0
    critical_gaps: int = 0
    
    recommendations: List[str] = Field(default_factory=list)
    
    def is_sufficient_for_autonomous_action(self) -> bool:
        """Can we act autonomously with current understanding?"""
        return (
            self.overall_score >= 0.7 and
            self.critical_gaps == 0 and
            self.dimension_scores.get("goal_clarity", 0) >= 0.7 and
            self.dimension_scores.get("value_hierarchy", 0) >= 0.6
        )
