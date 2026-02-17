"""
Autonomous AI Swarm Orchestrator

A sophisticated orchestrator that handles high-level requests within boundaries
(budgets, ethics) while building a holistic understanding of user intent.
"""

from .orchestrator import SwarmOrchestrator
from .autonomous import AutonomousOrchestrator
from .learning_orchestrator import LearningOrchestrator
from .models import (
    UserFramework,
    ClarificationQuestion,
    Decision,
    Boundary,
    KnowledgeGap,
    BoundaryType,
    ConfidenceLevel,
)
from .learning_models import (
    DecisionOutcome,
    DecisionContext,
    ReasoningPattern,
    PreferenceHypothesis,
    EnhancedKnowledgeGap,
    GapRootCause,
    ProgressUpdate,
    FrameworkCompleteness,
)
from .executor import TaskExecutor, Task, TaskStatus
from .context import (
    ContextAggregator,
    GoogleWorkspaceContextProvider,
    GeminiContextProvider,
)
from .services import (
    ServiceRegistry,
    DomainRegistrar,
    EmailProvider,
    AIPlatformResearcher,
)
from .persona import (
    Persona,
    PersonaCore,
    PersonaBehavior,
    PersonaKnowledge,
    PersonaType,
    SummoningProtocol,
    create_epiphany_architect,
)
from .persona_persistence import PersonaPersistence

__all__ = [
    "SwarmOrchestrator",
    "AutonomousOrchestrator",
    "LearningOrchestrator",
    "UserFramework",
    "ClarificationQuestion",
    "Decision",
    "Boundary",
    "KnowledgeGap",
    "BoundaryType",
    "ConfidenceLevel",
    "DecisionOutcome",
    "DecisionContext",
    "ReasoningPattern",
    "PreferenceHypothesis",
    "EnhancedKnowledgeGap",
    "GapRootCause",
    "ProgressUpdate",
    "FrameworkCompleteness",
    "TaskExecutor",
    "Task",
    "TaskStatus",
    "ContextAggregator",
    "GoogleWorkspaceContextProvider",
    "GeminiContextProvider",
    "ServiceRegistry",
    "DomainRegistrar",
    "EmailProvider",
    "AIPlatformResearcher",
    "Persona",
    "PersonaCore",
    "PersonaBehavior",
    "PersonaKnowledge",
    "PersonaType",
    "SummoningProtocol",
    "PersonaPersistence",
    "create_epiphany_architect",
]
