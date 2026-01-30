"""
Autonomous AI Swarm Orchestrator

A sophisticated orchestrator that handles high-level requests within boundaries
(budgets, ethics) while building a holistic understanding of user intent.
"""

from .orchestrator import SwarmOrchestrator
from .models import (
    UserFramework,
    ClarificationQuestion,
    Decision,
    Boundary,
    KnowledgeGap,
)

__all__ = [
    "SwarmOrchestrator",
    "UserFramework",
    "ClarificationQuestion",
    "Decision",
    "Boundary",
    "KnowledgeGap",
]
