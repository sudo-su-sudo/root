"""
Real-world example: The exact use case from the requirements

This demonstrates the autonomous orchestrator handling the full request:
- Research and purchase domain
- Set up work email
- Research AI platform
- All within budget constraints
"""

from orchestrator.autonomous import AutonomousOrchestrator
from orchestrator.models import Boundary, BoundaryType


def main():
    """
    Demonstrate the autonomous orchestrator with the real-world use case
    """
    
    print("=" * 80)
    print("AUTONOMOUS AI SWARM ORCHESTRATOR - Real-World Example")
    print("=" * 80)
    print()
    
    # Create the orchestrator
    orchestrator = AutonomousOrchestrator()
    
    print("Step 1: Setting up the orchestrator with boundaries...")
    print("-" * 80)
    
    # Set up boundaries as specified in the request
    orchestrator.add_boundary(Boundary(
        type=BoundaryType.BUDGET,
        description="Total domain and email budget",
        value=15.0,
        is_hard_limit=True
    ))
    
    orchestrator.add_boundary(Boundary(
        type=BoundaryType.BUDGET,
        description="AI platform monthly cost limit",
        value=50.0,
        is_hard_limit=True
    ))
    
    orchestrator.add_boundary(Boundary(
        type=BoundaryType.ETHICAL,
        description="Security and privacy requirements",
        value="end_to_end_encryption_preferred",
        is_hard_limit=False
    ))
    
    print("✓ Boundaries configured:")
    print("  - Domain + Email budget: $15 (hard limit)")
    print("  - AI Platform budget: $50/month (hard limit)")
    print("  - Ethics: End-to-end encryption preferred")
    print()
    
    # The actual user request from the requirements
    request = """
    Research and purchase at least one year ownership of a web domain which fits 
    with the concepts described in my Google docs/drive/workspace folder, as well 
    as my conversation and project history with Gemini, and set up a work email 
    account with that domain for at least one year. Ensure the total cost is less 
    than $15. Then research the most versatile and secure AI developer platform 
    for an AI security research/development company, which includes maximum control 
    of safety settings, with the option to encrypt all account activity, project 
    files, and AI use through end to end encryption between my company and the AI, 
    so that security can be maintained even from rogue employees of the platform 
    itself. Determine the best value services with the most development and agentic 
    AI features, and if you can secure a platform account for under $50/month (at 
    the regular rate, before factoring in introductory bonuses or discounts) then 
    set up an account with the most suitable one, based on your best judgement.
    """
    
    print("Step 2: Processing the autonomous request...")
    print("-" * 80)
    print(f"Request: {request[:150]}...")
    print()
    
    # Process the request autonomously
    result = orchestrator.process_autonomous_request(request)
    
    print(f"Status: {result['status']}")
    print()
    
    # Handle different outcomes
    if result['status'] == 'needs_clarification':
        print("⚠ NEEDS CLARIFICATION")
        print("=" * 80)
        print()
        print("The orchestrator identified knowledge gaps and needs clarification:")
        print()
        
        for i, question in enumerate(result.get('questions', []), 1):
            print(f"Question {i}:")
            print(f"  {question['question']}")
            print(f"  Context: {question['context']}")
            print()
        
        print("After you answer these questions, the orchestrator can proceed with")
        print("confident autonomous execution.")
        
    elif result['status'] == 'completed':
        print("✓ SIMULATION COMPLETED")
        print("=" * 80)
        print()
        
        print("Workflow Steps Completed:")
        for step in result.get('steps', []):
            print(f"  ✓ {step}")
        print()
        
        print("Execution Results (SIMULATION MODE):")
        print("-" * 80)
        
        execution = result.get('execution_results', {})
        
        for task_result in execution.get('tasks', []):
            print(f"\nTask: {task_result['name']}")
            print(f"Description: {task_result['description']}")
            
            outcome = task_result.get('estimated_outcome', {})
            
            if 'steps' in outcome:
                print("  Steps that would be executed:")
                for step in outcome['steps']:
                    print(f"    • {step}")
            
            if 'estimated_cost' in outcome:
                print(f"  Estimated cost: ${outcome['estimated_cost']:.2f}")
            
            if 'top_matches' in outcome:
                print("  Top platform recommendations:")
                for i, platform in enumerate(outcome['top_matches'][:3], 1):
                    print(f"    {i}. {platform['name']}")
                    print(f"       Cost: ${platform['estimated_monthly_cost']}/month")
                    print(f"       Score: {platform['match_score']:.1f}")
                    print(f"       E2E Encryption: {platform['security'].get('end_to_end_encryption', False)}")
            
            if 'recommendation' in outcome:
                print(f"  Recommended: {outcome['recommendation']}")
            
            if 'note' in outcome:
                print(f"  ⚠ Note: {outcome['note']}")
        
        print()
        print("=" * 80)
        print("IMPORTANT: This is a SIMULATION")
        print("=" * 80)
        print()
        print("To enable real execution, you would need to:")
        print("  1. Configure payment methods for domain/email services")
        print("  2. Provide Google Workspace API credentials")
        print("  3. Provide Gemini API key for context gathering")
        print("  4. Enable real service integrations")
        print("  5. Review and approve the execution plan")
        print()
        print("The orchestrator has demonstrated it can:")
        print("  ✓ Understand complex multi-part requests")
        print("  ✓ Decompose into executable tasks")
        print("  ✓ Respect budget boundaries")
        print("  ✓ Prioritize security requirements")
        print("  ✓ Make informed recommendations")
        print()
    
    elif result['status'] == 'boundary_violation':
        print("⚠ BOUNDARY VIOLATION")
        print("=" * 80)
        print()
        print("The proposed actions would violate your boundaries:")
        for violation in result.get('boundary_violations', []):
            print(f"  • {violation}")
        print()
    
    elif result['status'] == 'low_confidence':
        print("⚠ LOW CONFIDENCE")
        print("=" * 80)
        print()
        print(result.get('message', 'Cannot proceed with confidence'))
        print()


def demonstrate_clarification_flow():
    """
    Demonstrate how the orchestrator asks clarifying questions
    """
    print("\n")
    print("=" * 80)
    print("DEMONSTRATION: Clarification Question Flow")
    print("=" * 80)
    print()
    
    # Create orchestrator without user framework
    orchestrator = AutonomousOrchestrator()
    
    # Vague request
    request = "I need help with my online business"
    
    print(f"Request: {request}")
    print()
    
    result = orchestrator.process_autonomous_request(request)
    
    print("The orchestrator identifies that it needs more information:")
    print()
    
    for i, question in enumerate(result.get('questions', []), 1):
        print(f"{i}. {question['question']}")
        print(f"   Why: {question['context']}")
        print()
    
    print("This ensures the orchestrator builds a complete mental model")
    print("before taking any autonomous actions.")
    print()


if __name__ == "__main__":
    # Run main example
    main()
    
    # Show clarification flow
    demonstrate_clarification_flow()
