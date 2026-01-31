"""
Enhanced Learning Orchestrator with preference learning and meta-reasoning

This orchestrator focuses on deep understanding over transparency.
It learns WHY you make decisions, not just what you decide.
"""

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

from .orchestrator import SwarmOrchestrator
from .models import Boundary, Decision, ConfidenceLevel
from .learning_models import (
    DecisionOutcome,
    DecisionContext,
    ProgressUpdate,
    FrameworkCompleteness,
    EnhancedKnowledgeGap,
)
from .preference_learner import PreferenceLearner
from .meta_reasoning import MetaReasoningEngine


class LearningOrchestrator(SwarmOrchestrator):
    """
    Enhanced orchestrator with preference learning and meta-reasoning.
    
    Key differences from base orchestrator:
    - Learns from decision history to understand WHY you choose things
    - Performs meta-reasoning to identify exact gaps in understanding
    - Provides high-level progress updates, not granular details
    - Can make confident decisions based on learned patterns
    - Identifies root causes of uncertainty, not just symptoms
    """
    
    def __init__(self):
        super().__init__()
        
        # Learning systems (these are the "black box" AI components)
        self.preference_learner = PreferenceLearner()
        self.meta_reasoner = MetaReasoningEngine()
        
        # Track insights gained
        self.insights: List[str] = []
        
        # Progress tracking
        self.last_progress_update: Optional[ProgressUpdate] = None
    
    def record_user_decision(
        self,
        situation: str,
        chosen_option: str,
        rejected_options: List[str],
        reasoning: Optional[str] = None,
        constraints: Optional[Dict[str, Any]] = None
    ):
        """
        Record a decision the user made to learn from it.
        
        This is how the system learns your preferences - by observing
        what you choose and (optionally) why you chose it.
        """
        outcome = DecisionOutcome(
            chosen_option=chosen_option,
            rejected_options=rejected_options,
            context=DecisionContext(
                situation=situation,
                available_options=[chosen_option] + rejected_options,
                constraints=constraints or {}
            ),
            explicit_reasoning=reasoning
        )
        
        # Learn from this decision
        self.preference_learner.record_decision(outcome)
        
        # Extract insights
        self._extract_insights_from_decision(outcome)
    
    def _extract_insights_from_decision(self, outcome: DecisionOutcome):
        """Extract learnings from a decision"""
        if outcome.explicit_reasoning:
            insight = f"Learned: User chose '{outcome.chosen_option}' because {outcome.explicit_reasoning}"
            self.insights.append(insight)
        
        # Check if this reveals a pattern
        patterns = self.preference_learner.reasoning_patterns
        new_patterns = [p for p in patterns if len(p.evidence) == 1]  # Just created
        for pattern in new_patterns:
            insight = f"Discovered pattern: {pattern.pattern_description}"
            self.insights.append(insight)
    
    def make_autonomous_decision(
        self,
        situation: str,
        options: List[str],
        require_high_confidence: bool = True
    ) -> Tuple[str, float, str, bool]:
        """
        Make a decision on user's behalf based on learned preferences.
        
        Returns:
            (chosen_option, confidence, reasoning, needs_confirmation)
        """
        # Use preference learner to predict
        predicted, confidence, reasoning = self.preference_learner.predict_preference(
            situation, options
        )
        
        # Determine if confirmation needed
        needs_confirmation = False
        if require_high_confidence:
            needs_confirmation = confidence < 0.7
        else:
            needs_confirmation = confidence < 0.5
        
        # Analyze uncertainty if confidence is low
        if confidence < 0.6:
            gaps = self.meta_reasoner.analyze_uncertainty(
                situation,
                options,
                self.user_framework,
                self.preference_learner.reasoning_patterns,
                self.preference_learner.preference_hypotheses
            )
            
            if gaps:
                # Add gap reasoning to explanation
                critical_gaps = [g for g in gaps if g.required_for_action]
                if critical_gaps:
                    reasoning += f"\n\nUncertainty because: {critical_gaps[0].description}"
                    reasoning += f"\nRoot cause: {critical_gaps[0].root_cause.value}"
                    reasoning += f"\nTo resolve: {critical_gaps[0].suggested_resolution}"
                    needs_confirmation = True
        
        return predicted, confidence, reasoning, needs_confirmation
    
    def analyze_understanding(self) -> FrameworkCompleteness:
        """
        Assess how well we understand the user's preferences.
        
        This is the meta-reasoning: understanding what we don't know.
        """
        return self.preference_learner.get_framework_completeness()
    
    def identify_critical_gaps(self, decision_context: str) -> List[EnhancedKnowledgeGap]:
        """
        Identify what's blocking confident decisions.
        
        This goes deeper than basic gap identification - it finds ROOT CAUSES.
        """
        gaps = self.meta_reasoner.analyze_uncertainty(
            decision_context,
            [],  # Options not needed for gap analysis
            self.user_framework,
            self.preference_learner.reasoning_patterns,
            self.preference_learner.preference_hypotheses
        )
        
        # Add insights about gaps
        for gap in gaps:
            if gap.required_for_action:
                insight = f"Critical gap identified: {gap.area} - {gap.root_cause.value}"
                self.insights.append(insight)
        
        return gaps
    
    def get_progress_update(self, stage: str = "learning") -> ProgressUpdate:
        """
        Generate a high-level progress update.
        
        This is what you see - big picture, not implementation details.
        """
        completeness = self.analyze_understanding()
        
        # Get recent gaps
        recent_gaps = self.meta_reasoner.gap_history[-5:] if self.meta_reasoner.gap_history else []
        
        update = self.meta_reasoner.generate_progress_report(
            stage=stage,
            framework_completeness=completeness.overall_score,
            recent_insights=self.insights[-10:],  # Last 10 insights
            gaps=recent_gaps
        )
        
        self.last_progress_update = update
        return update
    
    def explain_uncertainty(self, decision_context: str) -> str:
        """
        Explain WHY we're uncertain about a decision.
        
        This is the meta-reasoning explanation - not just "I don't know"
        but "I don't know because X is missing from my model of you".
        """
        gaps = self.identify_critical_gaps(decision_context)
        
        if not gaps:
            return "No significant uncertainty - understanding is sufficient for confident action."
        
        # Build explanation
        explanation_parts = []
        
        for gap in gaps[:3]:  # Top 3 gaps
            explanation_parts.append(
                f"• {gap.area}: {gap.description}\n"
                f"  Root cause: {gap.root_cause.value}\n"
                f"  Impact: {gap.impact_on_decision}\n"
                f"  Resolution: {gap.suggested_resolution}"
            )
        
        return "Uncertainty analysis:\n\n" + "\n\n".join(explanation_parts)
    
    def should_act_autonomously(self, decision_type: str = "general") -> Tuple[bool, str]:
        """
        Determine if we understand you well enough to act autonomously.
        
        Returns:
            (can_act, reason)
        """
        completeness = self.analyze_understanding()
        
        # Check if we have sufficient understanding
        if completeness.is_sufficient_for_autonomous_action():
            return True, f"Understanding level at {int(completeness.overall_score * 100)}% - confident to act autonomously"
        
        # Identify what's blocking
        gaps = self.identify_critical_gaps(f"decision type: {decision_type}")
        critical_gaps = [g for g in gaps if g.required_for_action]
        
        if critical_gaps:
            return False, f"Cannot act autonomously: {critical_gaps[0].description}"
        
        # Medium confidence - can act but should check in
        return True, f"Can act with check-ins - understanding at {int(completeness.overall_score * 100)}%"
    
    def get_learning_summary(self) -> Dict[str, Any]:
        """
        Get a summary of what the system has learned.
        
        For high-level review, not implementation details.
        """
        completeness = self.analyze_understanding()
        
        return {
            "understanding_level": f"{int(completeness.overall_score * 100)}%",
            "decision_history_size": len(self.preference_learner.decision_history),
            "identified_patterns": len(self.preference_learner.reasoning_patterns),
            "strong_patterns": [
                p.pattern_description 
                for p in self.preference_learner.reasoning_patterns 
                if p.strength() > 0.7
            ],
            "confident_hypotheses": [
                h.hypothesis 
                for h in self.preference_learner.preference_hypotheses 
                if h.confidence > 0.7
            ],
            "dimension_scores": completeness.dimension_scores,
            "can_act_autonomously": completeness.is_sufficient_for_autonomous_action(),
            "recent_insights": self.insights[-5:],
            "recommendations": completeness.recommendations
        }
    
    def interactive_learning_session(self) -> List[str]:
        """
        Generate questions to accelerate learning.
        
        Returns questions that would most improve understanding.
        """
        # Identify gaps
        gaps = self.identify_critical_gaps("general learning")
        
        # Prioritize gaps
        critical = [g for g in gaps if g.required_for_action]
        important = [g for g in gaps if g.priority == "high" and not g.required_for_action]
        
        # Generate questions
        questions = []
        
        for gap in (critical + important)[:5]:  # Top 5
            questions.append(gap.suggested_resolution)
        
        # Add pattern-based questions
        weak_patterns = [p for p in self.preference_learner.reasoning_patterns if p.strength() < 0.5]
        if weak_patterns:
            pattern = weak_patterns[0]
            questions.append(
                f"I've noticed a possible pattern: {pattern.pattern_description}. "
                f"Is this accurate?"
            )
        
        return questions
