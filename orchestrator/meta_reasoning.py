"""
Meta-Reasoning Engine - Analyzes gaps in understanding at a deeper level

This identifies not just "what's missing" but "why we don't know" and "what would help us know"
"""

from typing import List, Dict, Any, Optional, Tuple
from collections import defaultdict

from .learning_models import (
    EnhancedKnowledgeGap,
    GapRootCause,
    ReasoningPattern,
    PreferenceHypothesis,
    ProgressUpdate,
)
from .models import UserFramework


class MetaReasoningEngine:
    """
    Performs meta-reasoning about the orchestrator's own understanding.
    
    Answers questions like:
    - Why don't I know what the user would choose?
    - What specific information would resolve this uncertainty?
    - Which aspect of my mental model is incomplete?
    """
    
    def __init__(self):
        self.gap_history: List[EnhancedKnowledgeGap] = []
        self.resolution_strategies: Dict[GapRootCause, str] = {
            GapRootCause.MISSING_VALUE_PRIORITY: "Ask user to rank values in order of importance",
            GapRootCause.MISSING_GOAL_CONTEXT: "Ask user why this goal matters to them",
            GapRootCause.CONFLICTING_PATTERNS: "Present conflicting examples and ask for clarification",
            GapRootCause.INSUFFICIENT_EXAMPLES: "Observe more decisions in similar contexts",
            GapRootCause.AMBIGUOUS_TRADEOFF: "Ask user how they balance these competing factors",
            GapRootCause.MISSING_CONSTRAINT_IMPORTANCE: "Ask if this boundary is flexible and under what conditions",
            GapRootCause.UNCLEAR_SUCCESS_METRIC: "Ask user how they define success for this goal",
            GapRootCause.CONTEXT_DEPENDENCY: "Identify contexts where preference differs and ask about the pattern",
        }
    
    def analyze_uncertainty(
        self,
        decision_context: str,
        available_options: List[str],
        user_framework: UserFramework,
        reasoning_patterns: List[ReasoningPattern],
        preference_hypotheses: List[PreferenceHypothesis]
    ) -> List[EnhancedKnowledgeGap]:
        """
        Perform deep analysis of why we're uncertain about a decision.
        
        This is the core meta-reasoning: understanding what's missing in our understanding.
        """
        gaps = []
        
        # Analyze each dimension of understanding
        
        # 1. Check for value priority gaps
        value_gap = self._analyze_value_understanding(
            user_framework, reasoning_patterns, decision_context
        )
        if value_gap:
            gaps.append(value_gap)
        
        # 2. Check for goal context gaps
        goal_gap = self._analyze_goal_understanding(
            user_framework, decision_context
        )
        if goal_gap:
            gaps.append(goal_gap)
        
        # 3. Check for pattern conflicts
        conflict_gap = self._analyze_pattern_conflicts(
            reasoning_patterns, preference_hypotheses, decision_context
        )
        if conflict_gap:
            gaps.append(conflict_gap)
        
        # 4. Check for tradeoff understanding
        tradeoff_gap = self._analyze_tradeoff_understanding(
            available_options, reasoning_patterns, decision_context
        )
        if tradeoff_gap:
            gaps.append(tradeoff_gap)
        
        # 5. Check for context dependency
        context_gap = self._analyze_context_dependency(
            decision_context, reasoning_patterns
        )
        if context_gap:
            gaps.append(context_gap)
        
        # Store for learning
        for gap in gaps:
            self._record_gap(gap)
        
        return gaps
    
    def _analyze_value_understanding(
        self,
        framework: UserFramework,
        patterns: List[ReasoningPattern],
        context: str
    ) -> Optional[EnhancedKnowledgeGap]:
        """Check if we understand value priorities"""
        if not framework.values:
            return EnhancedKnowledgeGap(
                area="value_priorities",
                description="No values defined in user framework",
                root_cause=GapRootCause.MISSING_VALUE_PRIORITY,
                impact_on_decision="Cannot evaluate options against user values",
                priority="high",
                required_for_action=True,
                blocking_decision_types=["all"],
                suggested_resolution=self.resolution_strategies[GapRootCause.MISSING_VALUE_PRIORITY]
            )
        
        # Check if we know relative priorities
        if len(framework.values) > 1:
            # Do we have patterns showing which values win in conflicts?
            value_priority_patterns = [p for p in patterns if "priority" in p.pattern_type.lower()]
            if not value_priority_patterns:
                return EnhancedKnowledgeGap(
                    area="value_priority_ranking",
                    description=f"Have {len(framework.values)} values but don't know relative priorities",
                    root_cause=GapRootCause.MISSING_VALUE_PRIORITY,
                    impact_on_decision="Cannot resolve conflicts when values compete",
                    priority="medium",
                    required_for_action=False,
                    blocking_decision_types=["value_conflicts"],
                    suggested_resolution="Observe decisions where values conflict to learn priorities"
                )
        
        return None
    
    def _analyze_goal_understanding(
        self,
        framework: UserFramework,
        context: str
    ) -> Optional[EnhancedKnowledgeGap]:
        """Check if we understand goal context and motivation"""
        if not framework.goals:
            return EnhancedKnowledgeGap(
                area="goal_definition",
                description="No goals defined",
                root_cause=GapRootCause.MISSING_GOAL_CONTEXT,
                impact_on_decision="Cannot align decisions with user objectives",
                priority="high",
                required_for_action=True,
                blocking_decision_types=["all"],
                suggested_resolution=self.resolution_strategies[GapRootCause.MISSING_GOAL_CONTEXT]
            )
        
        # Check if we understand WHY these goals exist
        if not framework.mental_model.get("goal_motivations"):
            return EnhancedKnowledgeGap(
                area="goal_motivations",
                description="Know user's goals but not why they matter",
                root_cause=GapRootCause.MISSING_GOAL_CONTEXT,
                impact_on_decision="May optimize for stated goal in way that doesn't serve underlying motivation",
                priority="medium",
                required_for_action=False,
                blocking_decision_types=["strategic"],
                suggested_resolution="Ask user about underlying motivations for their goals"
            )
        
        return None
    
    def _analyze_pattern_conflicts(
        self,
        patterns: List[ReasoningPattern],
        hypotheses: List[PreferenceHypothesis],
        context: str
    ) -> Optional[EnhancedKnowledgeGap]:
        """Check for conflicting patterns in understanding"""
        # Look for contradictory patterns
        for i, p1 in enumerate(patterns):
            for p2 in patterns[i+1:]:
                if self._patterns_conflict(p1, p2):
                    return EnhancedKnowledgeGap(
                        area="conflicting_patterns",
                        description=f"Conflicting patterns: '{p1.pattern_description}' vs '{p2.pattern_description}'",
                        root_cause=GapRootCause.CONFLICTING_PATTERNS,
                        impact_on_decision="Uncertain which pattern applies in this context",
                        priority="high",
                        required_for_action=True,
                        blocking_decision_types=["pattern_dependent"],
                        related_patterns=[p1.pattern_type, p2.pattern_type],
                        suggested_resolution=self.resolution_strategies[GapRootCause.CONFLICTING_PATTERNS]
                    )
        
        # Check hypothesis confidence
        low_confidence = [h for h in hypotheses if h.confidence < 0.5]
        if low_confidence and len(hypotheses) > 3:
            return EnhancedKnowledgeGap(
                area="hypothesis_uncertainty",
                description=f"{len(low_confidence)} hypotheses have low confidence",
                root_cause=GapRootCause.INSUFFICIENT_EXAMPLES,
                impact_on_decision="Predictions based on weak evidence",
                priority="medium",
                required_for_action=False,
                suggested_resolution=self.resolution_strategies[GapRootCause.INSUFFICIENT_EXAMPLES]
            )
        
        return None
    
    def _patterns_conflict(self, p1: ReasoningPattern, p2: ReasoningPattern) -> bool:
        """Check if two patterns contradict each other"""
        # Simple heuristic - check for opposing keywords
        opposing_pairs = [
            ("speed", "thoroughness"),
            ("cost", "quality"),
            ("risk", "safety"),
            ("simple", "complex"),
            ("quick", "careful")
        ]
        
        for word1, word2 in opposing_pairs:
            if word1 in p1.pattern_type and word2 in p2.pattern_type:
                return True
            if word2 in p1.pattern_type and word1 in p2.pattern_type:
                return True
        
        return False
    
    def _analyze_tradeoff_understanding(
        self,
        options: List[str],
        patterns: List[ReasoningPattern],
        context: str
    ) -> Optional[EnhancedKnowledgeGap]:
        """Check if we understand how user trades off competing factors"""
        # Detect if options present tradeoffs
        tradeoff_keywords = {
            "cost": ["cheap", "expensive", "price", "cost"],
            "quality": ["quality", "premium", "best"],
            "speed": ["fast", "quick", "immediate"],
            "thoroughness": ["thorough", "careful", "detailed"],
        }
        
        # Check which factors are present
        present_factors = []
        for factor, keywords in tradeoff_keywords.items():
            if any(any(k in opt.lower() for k in keywords) for opt in options):
                present_factors.append(factor)
        
        # If multiple factors, check if we know the tradeoff
        if len(present_factors) >= 2:
            tradeoff_patterns = [p for p in patterns 
                               if any(f in p.pattern_type for f in present_factors)]
            
            if not tradeoff_patterns or all(p.confidence < 0.6 for p in tradeoff_patterns):
                return EnhancedKnowledgeGap(
                    area="tradeoff_function",
                    description=f"Don't know how user trades off {' vs '.join(present_factors)}",
                    root_cause=GapRootCause.AMBIGUOUS_TRADEOFF,
                    impact_on_decision="Cannot predict which factor user prioritizes",
                    priority="high",
                    required_for_action=True,
                    blocking_decision_types=["tradeoff_decisions"],
                    suggested_resolution=self.resolution_strategies[GapRootCause.AMBIGUOUS_TRADEOFF]
                )
        
        return None
    
    def _analyze_context_dependency(
        self,
        context: str,
        patterns: List[ReasoningPattern]
    ) -> Optional[EnhancedKnowledgeGap]:
        """Check if preferences might be context-dependent"""
        # Look for context indicators
        context_indicators = ["urgent", "important", "casual", "critical", "routine"]
        
        if any(ind in context.lower() for ind in context_indicators):
            # Check if we have patterns for this context
            context_specific_patterns = [p for p in patterns 
                                        if any(ind in p.pattern_description.lower() 
                                              for ind in context_indicators)]
            
            if not context_specific_patterns:
                return EnhancedKnowledgeGap(
                    area="context_sensitivity",
                    description="Context suggests preferences might vary, but no context-specific patterns",
                    root_cause=GapRootCause.CONTEXT_DEPENDENCY,
                    impact_on_decision="May apply wrong pattern for this context",
                    priority="medium",
                    required_for_action=False,
                    suggested_resolution=self.resolution_strategies[GapRootCause.CONTEXT_DEPENDENCY]
                )
        
        return None
    
    def _record_gap(self, gap: EnhancedKnowledgeGap):
        """Record gap for tracking patterns"""
        # Check if we've seen this gap before
        for existing in self.gap_history:
            if existing.area == gap.area and existing.root_cause == gap.root_cause:
                existing.times_encountered += 1
                existing.last_encountered = gap.last_encountered
                return
        
        self.gap_history.append(gap)
    
    def generate_progress_report(
        self,
        stage: str,
        framework_completeness: float,
        recent_insights: List[str],
        gaps: List[EnhancedKnowledgeGap]
    ) -> ProgressUpdate:
        """
        Generate high-level progress report for user.
        
        This is what the user sees - big picture, not details.
        """
        # Determine alignment status
        critical_gaps = [g for g in gaps if g.required_for_action]
        
        if not critical_gaps and framework_completeness > 0.7:
            alignment = "✓ Strong alignment - confident in understanding your preferences"
        elif critical_gaps:
            alignment = f"⚠ {len(critical_gaps)} critical gap(s) blocking autonomous decisions"
        else:
            alignment = "→ Building understanding - can make some decisions but not all"
        
        # Key insights
        insights = recent_insights[-5:] if recent_insights else []
        
        # Next steps
        next_steps = []
        if critical_gaps:
            for gap in critical_gaps[:3]:  # Top 3
                next_steps.append(f"Need to understand: {gap.area}")
        else:
            next_steps.append("Ready to execute decisions autonomously")
        
        # Questions for user (from gaps)
        questions = []
        for gap in critical_gaps[:2]:  # Top 2 most important
            if gap.suggested_resolution:
                questions.append(gap.suggested_resolution)
        
        # Summary
        summary = f"Understanding level: {int(framework_completeness * 100)}% - "
        if framework_completeness > 0.8:
            summary += "Can act confidently on your behalf"
        elif framework_completeness > 0.5:
            summary += "Learning your patterns, some decisions need confirmation"
        else:
            summary += "Building initial understanding, need more context"
        
        return ProgressUpdate(
            stage=stage,
            summary=summary,
            key_insights=insights,
            confidence_level="high" if framework_completeness > 0.7 else "medium" if framework_completeness > 0.4 else "low",
            alignment_check=alignment,
            next_steps=next_steps,
            questions_for_user=questions
        )
    
    def recommend_gap_resolution(self, gap: EnhancedKnowledgeGap) -> str:
        """Recommend how to resolve a specific gap"""
        return gap.suggested_resolution or self.resolution_strategies.get(
            gap.root_cause,
            "Observe more examples in similar contexts"
        )
