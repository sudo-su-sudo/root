"""
Autonomous AI Swarm Orchestrator

A sophisticated orchestrator that handles high-level requests within boundaries
(budgets, ethics) while building a holistic understanding of user intent.
"""

from .orchestrator import SwarmOrchestrator
from .autonomous import AutonomousOrchestrator
from .models import (
    UserFramework,
    ClarificationQuestion,
    Decision,
    Boundary,
    KnowledgeGap,
    BoundaryType,
    ConfidenceLevel,
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

__all__ = [
    "SwarmOrchestrator",
    "AutonomousOrchestrator",
    "UserFramework",
    "ClarificationQuestion",
    "Decision",
    "Boundary",
    "KnowledgeGap",
    "BoundaryType",
    "ConfidenceLevel",
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
]
