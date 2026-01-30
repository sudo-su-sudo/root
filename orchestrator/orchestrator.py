"""
Main SwarmOrchestrator implementation
"""

from typing import List, Dict, Any, Optional, Tuple
from .models import (
    UserFramework,
    ClarificationQuestion,
    Decision,
    Boundary,
    KnowledgeGap,
    ConfidenceLevel,
    BoundaryType,
)


class SwarmOrchestrator:
    """
    Autonomous AI Swarm Orchestrator that handles high-level requests within boundaries.
    
    This orchestrator:
    - Anticipates ambiguities and asks targeted clarifying questions upfront
    - Builds a holistic user framework (goals/values/intent/mental model)
    - Makes confident decisions where preferences are clear
    - Identifies knowledge gaps in its framework of user mental model
    - Confirms ambiguities before acting
    - Only acts on user's behalf when user values and intent are solidly understood
    """
    
    def __init__(self):
        self.user_framework = UserFramework()
        self.boundaries: List[Boundary] = []
        self.knowledge_gaps: List[KnowledgeGap] = []
        self.pending_questions: List[ClarificationQuestion] = []
        self.decisions: List[Decision] = []
        
    def add_boundary(self, boundary: Boundary) -> None:
        """Add a boundary constraint to the orchestrator"""
        self.boundaries.append(boundary)
    
    def update_user_framework(
        self,
        goals: Optional[List[str]] = None,
        values: Optional[List[str]] = None,
        intent: Optional[str] = None,
        mental_model: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Update the user framework with new information"""
        if goals:
            self.user_framework.goals.extend(goals)
        if values:
            self.user_framework.values.extend(values)
        if intent:
            self.user_framework.intent = intent
        if mental_model:
            self.user_framework.mental_model.update(mental_model)
        if context:
            self.user_framework.context.update(context)
    
    def identify_knowledge_gaps(self, request: str) -> List[KnowledgeGap]:
        """
        Analyze a request and identify gaps in understanding of user's mental model.
        
        This method anticipates ambiguities in the request based on the current
        user framework.
        """
        gaps = []
        
        # Check if we have basic understanding
        if not self.user_framework.goals:
            gaps.append(KnowledgeGap(
                area="goals",
                description="User's goals are not defined",
                priority="high",
                required_for_action=True
            ))
        
        if not self.user_framework.values:
            gaps.append(KnowledgeGap(
                area="values",
                description="User's values and ethical guidelines are not defined",
                priority="high",
                required_for_action=True
            ))
        
        if not self.user_framework.intent:
            gaps.append(KnowledgeGap(
                area="intent",
                description="User's intent for this request is unclear",
                priority="high",
                required_for_action=True
            ))
        
        # Domain-specific gap identification
        request_lower = request.lower()
        
        # Check for budget-related requests without budget boundary
        if any(keyword in request_lower for keyword in ["cost", "budget", "spend", "price"]):
            has_budget = any(b.type == BoundaryType.BUDGET for b in self.boundaries)
            if not has_budget:
                gaps.append(KnowledgeGap(
                    area="budget",
                    description="Request involves costs but no budget boundary is defined",
                    priority="high",
                    required_for_action=True
                ))
        
        # Check for time-related requests without temporal boundary
        if any(keyword in request_lower for keyword in ["deadline", "timeline", "when", "schedule"]):
            has_temporal = any(b.type == BoundaryType.TEMPORAL for b in self.boundaries)
            if not has_temporal:
                gaps.append(KnowledgeGap(
                    area="timeline",
                    description="Request involves timing but no temporal boundary is defined",
                    priority="medium",
                    required_for_action=False
                ))
        
        self.knowledge_gaps.extend(gaps)
        return gaps
    
    def generate_clarification_questions(
        self, knowledge_gaps: Optional[List[KnowledgeGap]] = None
    ) -> List[ClarificationQuestion]:
        """
        Generate targeted clarifying questions based on identified knowledge gaps.
        
        These questions are designed to build a holistic understanding of the user.
        """
        gaps = knowledge_gaps or self.knowledge_gaps
        questions = []
        
        for gap in gaps:
            if gap.area == "goals":
                questions.append(ClarificationQuestion(
                    question="What are your primary goals or objectives?",
                    context="Understanding your goals helps me make decisions aligned with your desired outcomes.",
                    related_gap="goals"
                ))
            
            elif gap.area == "values":
                questions.append(ClarificationQuestion(
                    question="What values or ethical principles should guide my decisions?",
                    context="Knowing your values ensures I operate within your ethical boundaries.",
                    related_gap="values",
                    options=["Cost efficiency", "Quality over speed", "Transparency", "Privacy", "Sustainability"]
                ))
            
            elif gap.area == "intent":
                questions.append(ClarificationQuestion(
                    question="Can you clarify what you're trying to achieve with this request?",
                    context="Understanding your specific intent helps me choose the best approach.",
                    related_gap="intent"
                ))
            
            elif gap.area == "budget":
                questions.append(ClarificationQuestion(
                    question="What is your budget constraint for this request?",
                    context="This helps me make cost-effective decisions within your financial boundaries.",
                    related_gap="budget"
                ))
            
            elif gap.area == "timeline":
                questions.append(ClarificationQuestion(
                    question="What is your timeline or deadline for this request?",
                    context="Knowing the timeline helps me prioritize and plan accordingly.",
                    related_gap="timeline"
                ))
            
            else:
                # Generic question for other gaps
                questions.append(ClarificationQuestion(
                    question=f"Can you provide more information about: {gap.description}?",
                    context=f"This information is needed to proceed with confidence.",
                    related_gap=gap.area
                ))
        
        self.pending_questions.extend(questions)
        return questions
    
    def check_boundaries(self, proposed_action: str, action_details: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Check if a proposed action violates any boundaries.
        
        Returns:
            tuple: (is_within_boundaries, list_of_violations)
        """
        violations = []
        action_category = action_details.get("category", "")
        
        for boundary in self.boundaries:
            # Skip if boundary has a category and it doesn't match the action
            if boundary.category and action_category:
                if boundary.category != action_category:
                    continue
            
            if boundary.type == BoundaryType.BUDGET:
                cost = action_details.get("cost", 0)
                if cost > boundary.value:
                    violations.append(
                        f"Action cost ({cost}) exceeds budget boundary ({boundary.value})"
                    )
            
            elif boundary.type == BoundaryType.ETHICAL:
                # Check if action aligns with ethical guidelines
                ethical_concerns = action_details.get("ethical_concerns", [])
                if ethical_concerns:
                    violations.append(
                        f"Action raises ethical concerns: {', '.join(ethical_concerns)}"
                    )
            
            elif boundary.type == BoundaryType.TEMPORAL:
                duration = action_details.get("duration", 0)
                if duration > boundary.value:
                    violations.append(
                        f"Action duration ({duration}) exceeds temporal boundary ({boundary.value})"
                    )
            
            elif boundary.type == BoundaryType.SCOPE:
                scope = action_details.get("scope", "")
                # Allow if boundary.value is a list and scope contains any keyword from it
                # OR if scope is explicitly in the list
                if boundary.value:
                    if isinstance(boundary.value, list):
                        # Check if scope matches or contains any allowed keyword
                        allowed = False
                        for allowed_scope in boundary.value:
                            # Convert both to lowercase for comparison
                            scope_lower = scope.lower().replace("_", " ")
                            allowed_lower = allowed_scope.lower().replace("_", " ")
                            
                            # Split into keywords and check if any match
                            scope_keywords = set(scope_lower.split())
                            allowed_keywords = set(allowed_lower.split())
                            
                            # If there's any overlap in keywords, it's allowed
                            if scope_keywords & allowed_keywords:
                                allowed = True
                                break
                        
                        if not allowed:
                            violations.append(
                                f"Action scope ({scope}) outside allowed boundaries"
                            )
                    else:
                        # Single value - exact match
                        if scope != boundary.value:
                            violations.append(
                                f"Action scope ({scope}) outside allowed boundaries"
                            )
        
        return len(violations) == 0, violations
    
    def calculate_confidence(
        self, request: str, action_details: Dict[str, Any]
    ) -> ConfidenceLevel:
        """
        Calculate confidence level for a decision based on framework completeness.
        
        Higher confidence when:
        - User framework is well-established
        - No critical knowledge gaps
        - Action aligns with known values and goals
        """
        confidence_score = 0
        max_score = 5
        
        # Check framework completeness
        if self.user_framework.goals:
            confidence_score += 1
        if self.user_framework.values:
            confidence_score += 1
        if self.user_framework.intent:
            confidence_score += 1
        
        # Check for critical knowledge gaps
        critical_gaps = [g for g in self.knowledge_gaps if g.required_for_action]
        if not critical_gaps:
            confidence_score += 1
        
        # Check boundary compliance
        within_boundaries, _ = self.check_boundaries(request, action_details)
        if within_boundaries:
            confidence_score += 1
        
        # Map score to confidence level
        if confidence_score >= 4:
            return ConfidenceLevel.HIGH
        elif confidence_score >= 2:
            return ConfidenceLevel.MEDIUM
        else:
            return ConfidenceLevel.LOW
    
    def make_decision(
        self, request: str, action: str, action_details: Dict[str, Any]
    ) -> Decision:
        """
        Make a decision on whether to proceed with an action.
        
        Only proceeds with high confidence when user values and intent are
        solidly understood.
        """
        # Check boundaries
        within_boundaries, violations = self.check_boundaries(action, action_details)
        
        # Calculate confidence
        confidence = self.calculate_confidence(request, action_details)
        
        # Build rationale
        rationale_parts = []
        
        if not within_boundaries:
            rationale_parts.append(f"Action violates boundaries: {', '.join(violations)}")
        
        if self.user_framework.goals:
            rationale_parts.append(
                f"Aligned with goals: {', '.join(self.user_framework.goals[:2])}"
            )
        
        if self.user_framework.values:
            rationale_parts.append(
                f"Respects values: {', '.join(self.user_framework.values[:2])}"
            )
        
        critical_gaps = [g for g in self.knowledge_gaps if g.required_for_action]
        if critical_gaps:
            rationale_parts.append(
                f"Critical knowledge gaps exist: {', '.join(g.area for g in critical_gaps[:2])}"
            )
        
        rationale = "; ".join(rationale_parts) if rationale_parts else "Proceeding based on current understanding"
        
        # Determine if confirmation is needed
        requires_confirmation = (
            confidence == ConfidenceLevel.LOW or
            not within_boundaries or
            len(critical_gaps) > 0
        )
        
        decision = Decision(
            action=action,
            confidence=confidence,
            rationale=rationale,
            framework_alignment={
                "goals_aligned": "yes" if self.user_framework.goals else "no",
                "values_aligned": "yes" if self.user_framework.values else "no",
                "intent_clear": "yes" if self.user_framework.intent else "no",
            },
            boundaries_checked=[b.type for b in self.boundaries],
            requires_confirmation=requires_confirmation
        )
        
        self.decisions.append(decision)
        return decision
    
    def process_request(self, request: str) -> Dict[str, Any]:
        """
        Main entry point for processing a high-level request.
        
        Returns a comprehensive response including:
        - Identified knowledge gaps
        - Clarification questions (if needed)
        - Proposed decision (if confident enough)
        - Next steps
        """
        # Identify knowledge gaps
        gaps = self.identify_knowledge_gaps(request)
        
        # If critical gaps exist, generate questions instead of making decisions
        critical_gaps = [g for g in gaps if g.required_for_action]
        
        if critical_gaps:
            questions = self.generate_clarification_questions(critical_gaps)
            return {
                "status": "needs_clarification",
                "knowledge_gaps": [g.dict() for g in critical_gaps],
                "clarification_questions": [q.dict() for q in questions],
                "message": "I need to understand your goals, values, and intent better before proceeding confidently."
            }
        
        # If framework is solid, we can proceed with analysis
        return {
            "status": "ready_for_decision",
            "user_framework": self.user_framework.dict(),
            "message": "I have enough context to proceed. Provide action details for decision-making."
        }
    
    def can_act_confidently(self) -> bool:
        """
        Determine if the orchestrator can act confidently on user's behalf.
        
        Returns True only when user values and intent are solidly understood.
        """
        has_goals = bool(self.user_framework.goals)
        has_values = bool(self.user_framework.values)
        has_intent = bool(self.user_framework.intent)
        
        critical_gaps = [g for g in self.knowledge_gaps if g.required_for_action]
        no_critical_gaps = len(critical_gaps) == 0
        
        return has_goals and has_values and has_intent and no_critical_gaps
