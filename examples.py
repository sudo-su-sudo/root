"""
Example usage of the Autonomous AI Swarm Orchestrator
"""

from orchestrator import (
    SwarmOrchestrator,
    Boundary,
    BoundaryType,
)


def example_basic_usage():
    """Example: Basic usage with clarification flow"""
    print("=== Example 1: Basic Usage ===\n")
    
    # Create orchestrator
    orchestrator = SwarmOrchestrator()
    
    # Process a request without context
    request = "Build a new customer management system"
    result = orchestrator.process_request(request)
    
    print(f"Request: {request}")
    print(f"Status: {result['status']}\n")
    
    if result['status'] == 'needs_clarification':
        print("Clarification Questions:")
        for i, question in enumerate(result['clarification_questions'], 1):
            print(f"{i}. {question['question']}")
            print(f"   Context: {question['context']}\n")


def example_with_complete_framework():
    """Example: Usage with complete user framework"""
    print("\n=== Example 2: Complete Framework ===\n")
    
    # Create orchestrator
    orchestrator = SwarmOrchestrator()
    
    # Set up user framework
    orchestrator.update_user_framework(
        goals=[
            "Improve customer satisfaction",
            "Reduce operational costs",
            "Scale to 10,000 users"
        ],
        values=[
            "Data privacy",
            "Transparency",
            "Quality over speed"
        ],
        intent="Build a robust CRM system that respects user privacy"
    )
    
    # Add boundaries
    orchestrator.add_boundary(Boundary(
        type=BoundaryType.BUDGET,
        description="Total project budget",
        value=50000,
        is_hard_limit=True
    ))
    
    orchestrator.add_boundary(Boundary(
        type=BoundaryType.TEMPORAL,
        description="Project timeline in days",
        value=90,
        is_hard_limit=False
    ))
    
    orchestrator.add_boundary(Boundary(
        type=BoundaryType.ETHICAL,
        description="Ethical guidelines",
        value="privacy_first",
        is_hard_limit=True
    ))
    
    # Process request
    request = "Deploy the new CRM system"
    result = orchestrator.process_request(request)
    
    print(f"Request: {request}")
    print(f"Status: {result['status']}\n")
    print(f"Can act confidently: {orchestrator.can_act_confidently()}\n")
    
    if result['status'] == 'ready_for_decision':
        print("User Framework:")
        framework = result['user_framework']
        print(f"  Goals: {', '.join(framework['goals'])}")
        print(f"  Values: {', '.join(framework['values'])}")
        print(f"  Intent: {framework['intent']}\n")


def example_decision_making():
    """Example: Making decisions with boundary checking"""
    print("\n=== Example 3: Decision Making ===\n")
    
    orchestrator = SwarmOrchestrator()
    
    # Set up framework
    orchestrator.update_user_framework(
        goals=["Optimize application performance"],
        values=["Cost efficiency", "Scalability"],
        intent="Reduce server costs while maintaining performance"
    )
    
    orchestrator.add_boundary(Boundary(
        type=BoundaryType.BUDGET,
        description="Monthly infrastructure budget",
        value=5000
    ))
    
    # Scenario 1: Action within boundaries
    print("Scenario 1: Action within boundaries")
    decision1 = orchestrator.make_decision(
        request="Upgrade server infrastructure",
        action="upgrade_servers",
        action_details={
            "cost": 3000,
            "duration": 2,
            "scope": "infrastructure"
        }
    )
    
    print(f"  Action: {decision1.action}")
    print(f"  Confidence: {decision1.confidence}")
    print(f"  Requires Confirmation: {decision1.requires_confirmation}")
    print(f"  Rationale: {decision1.rationale}\n")
    
    # Scenario 2: Action exceeds boundaries
    print("Scenario 2: Action exceeds boundaries")
    decision2 = orchestrator.make_decision(
        request="Massive infrastructure expansion",
        action="expand_infrastructure",
        action_details={
            "cost": 15000,
            "duration": 30,
            "scope": "infrastructure"
        }
    )
    
    print(f"  Action: {decision2.action}")
    print(f"  Confidence: {decision2.confidence}")
    print(f"  Requires Confirmation: {decision2.requires_confirmation}")
    print(f"  Rationale: {decision2.rationale}\n")


def example_knowledge_gaps():
    """Example: Identifying and addressing knowledge gaps"""
    print("\n=== Example 4: Knowledge Gap Identification ===\n")
    
    orchestrator = SwarmOrchestrator()
    
    # Partial framework
    orchestrator.update_user_framework(
        goals=["Launch new product"],
        values=["Innovation"]
    )
    
    # Request with budget implications but no budget boundary
    request = "How much will marketing cost for the launch?"
    gaps = orchestrator.identify_knowledge_gaps(request)
    
    print(f"Request: {request}\n")
    print("Identified Knowledge Gaps:")
    for gap in gaps:
        print(f"  - {gap.area}: {gap.description}")
        print(f"    Priority: {gap.priority}")
        print(f"    Required for action: {gap.required_for_action}\n")
    
    # Generate questions
    questions = orchestrator.generate_clarification_questions(gaps)
    print("Generated Questions:")
    for i, q in enumerate(questions, 1):
        print(f"{i}. {q.question}")


def example_confidence_levels():
    """Example: Different confidence levels"""
    print("\n=== Example 5: Confidence Levels ===\n")
    
    # Low confidence (no framework)
    orchestrator1 = SwarmOrchestrator()
    confidence1 = orchestrator1.calculate_confidence("Do something", {})
    print(f"Empty framework confidence: {confidence1}")
    
    # Medium confidence (partial framework)
    orchestrator2 = SwarmOrchestrator()
    orchestrator2.update_user_framework(
        goals=["Goal 1"],
        values=["Value 1"]
    )
    confidence2 = orchestrator2.calculate_confidence("Do something", {})
    print(f"Partial framework confidence: {confidence2}")
    
    # High confidence (complete framework)
    orchestrator3 = SwarmOrchestrator()
    orchestrator3.update_user_framework(
        goals=["Goal 1"],
        values=["Value 1"],
        intent="Clear intent"
    )
    orchestrator3.add_boundary(Boundary(
        type=BoundaryType.BUDGET,
        description="Budget",
        value=10000
    ))
    confidence3 = orchestrator3.calculate_confidence(
        "Do something",
        {"cost": 5000}
    )
    print(f"Complete framework confidence: {confidence3}")


if __name__ == "__main__":
    example_basic_usage()
    example_with_complete_framework()
    example_decision_making()
    example_knowledge_gaps()
    example_confidence_levels()
