"""
Data models for the AI Swarm Orchestrator
"""

from typing import List, Dict, Any, Optional
from enum import Enum
from pydantic import BaseModel, Field


class BoundaryType(str, Enum):
    """Types of boundaries for orchestrator operations"""
    BUDGET = "budget"
    ETHICAL = "ethical"
    TEMPORAL = "temporal"
    SCOPE = "scope"


class ConfidenceLevel(str, Enum):
    """Confidence levels for decisions"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Boundary(BaseModel):
    """Represents a boundary constraint"""
    type: BoundaryType
    description: str
    value: Any
    is_hard_limit: bool = True
    category: Optional[str] = None  # Optional category for more specific matching

    class Config:
        use_enum_values = True



class UserFramework(BaseModel):
    """Holistic user framework capturing goals, values, intent, and mental model"""
    goals: List[str] = Field(default_factory=list, description="User's stated goals")
    values: List[str] = Field(default_factory=list, description="User's values and principles")
    intent: str = Field(default="", description="Understood user intent")
    mental_model: Dict[str, Any] = Field(default_factory=dict, description="User's mental model and preferences")
    context: Dict[str, Any] = Field(default_factory=dict, description="Additional contextual information")


class KnowledgeGap(BaseModel):
    """Represents a gap in the orchestrator's understanding"""
    area: str
    description: str
    priority: str = "medium"  # high, medium, low
    required_for_action: bool = False


class ClarificationQuestion(BaseModel):
    """A targeted question to resolve ambiguity"""
    question: str
    context: str
    related_gap: Optional[str] = None
    options: Optional[List[str]] = None


class Decision(BaseModel):
    """Represents a decision made by the orchestrator"""
    action: str
    confidence: ConfidenceLevel
    rationale: str
    framework_alignment: Dict[str, str] = Field(default_factory=dict)
    boundaries_checked: List[str] = Field(default_factory=list)
    requires_confirmation: bool = False

    class Config:
        use_enum_values = True
