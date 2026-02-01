"""
Preference Learning Engine - Learns from decision patterns to understand WHY user makes choices
"""

from typing import List, Dict, Any, Optional, Tuple
from collections import defaultdict
from datetime import datetime, timedelta

from .learning_models import (
    DecisionOutcome,
    DecisionContext,
    ReasoningPattern,
    PreferenceHypothesis,
    EnhancedKnowledgeGap,
    GapRootCause,
    FrameworkCompleteness,
)


class PreferenceLearner:
    """
    Learns user preferences from decision history.
    
    This is where the "black box" AI learning happens - it uses pattern recognition
    and inference to understand WHY the user makes decisions, not just what they decide.
    """
    
    def __init__(self):
        self.decision_history: List[DecisionOutcome] = []
        self.reasoning_patterns: List[ReasoningPattern] = []
        self.preference_hypotheses: List[PreferenceHypothesis] = []
        
        # Internal learning state (not exposed to user)
        self._value_weights: Dict[str, float] = {}  # Inferred importance of each value
        self._goal_priorities: Dict[str, float] = {}  # Inferred goal priorities
        self._tradeoff_functions: Dict[str, Any] = {}  # How user trades off competing factors
        
    def record_decision(self, outcome: DecisionOutcome):
        """Record a decision to learn from"""
        self.decision_history.append(outcome)
        
        # Immediately learn from this decision
        self._update_patterns(outcome)
        self._update_hypotheses(outcome)
        self._infer_value_weights(outcome)
    
    def _update_patterns(self, outcome: DecisionOutcome):
        """Identify and update reasoning patterns"""
        # Look for patterns in the decision
        
        # Pattern: Risk tolerance
        if "risk" in outcome.context.situation.lower():
            self._update_pattern(
                "risk_tolerance",
                f"User chose '{outcome.chosen_option}' in risky situation",
                outcome
            )
        
        # Pattern: Cost vs quality preference
        if any(opt for opt in outcome.rejected_options if "cheap" in opt.lower()):
            if "quality" in outcome.chosen_option.lower():
                self._update_pattern(
                    "quality_over_cost",
                    "User prefers quality over lower cost",
                    outcome
                )
        
        # Pattern: Speed vs thoroughness
        if "quick" in outcome.chosen_option.lower():
            self._update_pattern(
                "speed_preference",
                "User values speed",
                outcome
            )
        elif "thorough" in outcome.chosen_option.lower() or "careful" in outcome.chosen_option.lower():
            self._update_pattern(
                "thoroughness_preference",
                "User values thoroughness over speed",
                outcome
            )
    
    def _update_pattern(self, pattern_type: str, description: str, outcome: DecisionOutcome):
        """Update or create a reasoning pattern"""
        # Find existing pattern
        existing = None
        for p in self.reasoning_patterns:
            if p.pattern_type == pattern_type:
                existing = p
                break
        
        if existing:
            # Add evidence
            decision_id = f"{outcome.timestamp.isoformat()}_{outcome.chosen_option}"
            if decision_id not in existing.evidence:
                existing.evidence.append(decision_id)
            # Increase confidence with more examples
            existing.confidence = min(0.95, existing.confidence + 0.05)
        else:
            # Create new pattern
            decision_id = f"{outcome.timestamp.isoformat()}_{outcome.chosen_option}"
            self.reasoning_patterns.append(ReasoningPattern(
                pattern_type=pattern_type,
                pattern_description=description,
                confidence=0.3,  # Start with low confidence
                evidence=[decision_id]
            ))
    
    def _update_hypotheses(self, outcome: DecisionOutcome):
        """Update preference hypotheses based on new decision"""
        # Generate hypotheses from explicit reasoning if provided
        if outcome.explicit_reasoning:
            self._generate_hypothesis_from_reasoning(outcome)
        
        # Update existing hypotheses
        for hypothesis in self.preference_hypotheses:
            if self._decision_supports_hypothesis(outcome, hypothesis):
                decision_id = f"{outcome.timestamp.isoformat()}_{outcome.chosen_option}"
                hypothesis.supporting_evidence.append(decision_id)
                hypothesis.update_confidence()
            elif self._decision_contradicts_hypothesis(outcome, hypothesis):
                decision_id = f"{outcome.timestamp.isoformat()}_{outcome.chosen_option}"
                hypothesis.contradicting_evidence.append(decision_id)
                hypothesis.update_confidence()
    
    def _generate_hypothesis_from_reasoning(self, outcome: DecisionOutcome):
        """Generate new hypothesis from user's explicit reasoning"""
        if not outcome.explicit_reasoning:
            return
        
        # Extract key phrases
        reasoning = outcome.explicit_reasoning.lower()
        
        # Pattern: "because X"
        if "because" in reasoning:
            parts = reasoning.split("because", 1)
            if len(parts) == 2:
                reason = parts[1].strip()
                hypothesis_text = f"User prioritizes: {reason}"
                
                # Check if we already have this hypothesis
                existing = None
                for h in self.preference_hypotheses:
                    if reason in h.hypothesis.lower():
                        existing = h
                        break
                
                if existing:
                    decision_id = f"{outcome.timestamp.isoformat()}_{outcome.chosen_option}"
                    existing.supporting_evidence.append(decision_id)
                    existing.update_confidence()
                else:
                    decision_id = f"{outcome.timestamp.isoformat()}_{outcome.chosen_option}"
                    self.preference_hypotheses.append(PreferenceHypothesis(
                        hypothesis=hypothesis_text,
                        confidence=0.5,
                        supporting_evidence=[decision_id],
                        domain="general"
                    ))
    
    def _decision_supports_hypothesis(self, outcome: DecisionOutcome, hypothesis: PreferenceHypothesis) -> bool:
        """Check if a decision supports a hypothesis"""
        # Simple keyword matching for now (in production, use more sophisticated NLP)
        hypothesis_keywords = set(hypothesis.hypothesis.lower().split())
        decision_keywords = set(outcome.chosen_option.lower().split())
        
        if outcome.explicit_reasoning:
            decision_keywords.update(outcome.explicit_reasoning.lower().split())
        
        # If there's significant overlap, consider it supporting
        overlap = hypothesis_keywords & decision_keywords
        return len(overlap) >= 2
    
    def _decision_contradicts_hypothesis(self, outcome: DecisionOutcome, hypothesis: PreferenceHypothesis) -> bool:
        """Check if a decision contradicts a hypothesis"""
        # Look for contradictory keywords
        if "not" in hypothesis.hypothesis.lower() or "avoid" in hypothesis.hypothesis.lower():
            # Hypothesis is negative - check if decision violates it
            negative_terms = [w for w in hypothesis.hypothesis.lower().split() 
                            if w not in ["not", "avoid", "user", "prefers"]]
            if any(term in outcome.chosen_option.lower() for term in negative_terms):
                return True
        
        return False
    
    def _infer_value_weights(self, outcome: DecisionOutcome):
        """Infer relative importance of different values from decisions"""
        # This is internal "black box" learning
        
        # Extract values from context
        for key, value in outcome.context.constraints.items():
            if key not in self._value_weights:
                self._value_weights[key] = 0.5  # Start neutral
            
            # If this constraint was satisfied in chosen option, increase weight
            # (Simplified - in production, use more sophisticated inference)
            self._value_weights[key] = min(1.0, self._value_weights[key] + 0.1)
    
    def predict_preference(self, situation: str, options: List[str]) -> Tuple[str, float, str]:
        """
        Predict which option user would prefer and why.
        
        Returns:
            (predicted_option, confidence, reasoning)
        """
        if not self.decision_history:
            return options[0] if options else "", 0.0, "No decision history to learn from"
        
        # Score each option based on learned patterns
        option_scores: Dict[str, float] = {}
        reasoning_parts = []
        
        for option in options:
            score = 0.5  # Start neutral
            option_reasoning = []
            
            # Apply reasoning patterns
            for pattern in self.reasoning_patterns:
                if pattern.pattern_type in option.lower():
                    score += pattern.strength() * 0.3
                    option_reasoning.append(f"Matches {pattern.pattern_description}")
            
            # Apply preference hypotheses
            for hypothesis in self.preference_hypotheses:
                if hypothesis.confidence > 0.6:  # Only use confident hypotheses
                    keywords = set(hypothesis.hypothesis.lower().split())
                    option_keywords = set(option.lower().split())
                    if keywords & option_keywords:
                        score += hypothesis.confidence * 0.2
                        option_reasoning.append(f"Aligns with: {hypothesis.hypothesis}")
            
            option_scores[option] = score
            reasoning_parts.append(f"{option}: {', '.join(option_reasoning) if option_reasoning else 'No specific match'}")
        
        # Find best option
        best_option = max(option_scores.items(), key=lambda x: x[1])
        
        # Calculate confidence
        scores = list(option_scores.values())
        if len(scores) > 1:
            second_best = sorted(scores, reverse=True)[1]
            confidence = (best_option[1] - second_best) / 2
        else:
            confidence = best_option[1]
        
        reasoning = f"Based on {len(self.decision_history)} past decisions. " + "; ".join(reasoning_parts)
        
        return best_option[0], min(confidence, 1.0), reasoning
    
    def get_framework_completeness(self) -> FrameworkCompleteness:
        """Assess how complete our understanding is"""
        # Calculate dimension scores
        dimensions = {}
        
        # Goal clarity - based on decision consistency
        if self.decision_history:
            dimensions["goal_clarity"] = min(1.0, len(self.decision_history) / 20)
        else:
            dimensions["goal_clarity"] = 0.0
        
        # Value hierarchy - based on identified patterns
        dimensions["value_hierarchy"] = min(1.0, len(self.reasoning_patterns) / 10)
        
        # Pattern confidence - average of pattern strengths
        if self.reasoning_patterns:
            dimensions["pattern_confidence"] = sum(p.strength() for p in self.reasoning_patterns) / len(self.reasoning_patterns)
        else:
            dimensions["pattern_confidence"] = 0.0
        
        # Hypothesis quality - based on confident hypotheses
        confident_hypotheses = [h for h in self.preference_hypotheses if h.confidence > 0.7]
        dimensions["hypothesis_quality"] = min(1.0, len(confident_hypotheses) / 5)
        
        # Overall score
        overall = sum(dimensions.values()) / len(dimensions) if dimensions else 0.0
        
        # Recommendations
        recommendations = []
        if dimensions.get("goal_clarity", 0) < 0.5:
            recommendations.append("Need more examples of user decisions to understand goals")
        if dimensions.get("value_hierarchy", 0) < 0.5:
            recommendations.append("Need to observe more decision patterns")
        if dimensions.get("pattern_confidence", 0) < 0.6:
            recommendations.append("Current patterns have low confidence - need more consistent examples")
        
        return FrameworkCompleteness(
            overall_score=overall,
            dimension_scores=dimensions,
            identified_patterns=len(self.reasoning_patterns),
            decision_history_size=len(self.decision_history),
            critical_gaps=0,  # Will be set by meta-reasoning
            recommendations=recommendations
        )
