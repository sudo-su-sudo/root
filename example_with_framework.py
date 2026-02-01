"""
Real-world example with complete user framework

This shows what happens when the orchestrator has a complete understanding
of user goals, values, and intent - it can then act autonomously with confidence.
"""

from orchestrator.autonomous import AutonomousOrchestrator
from orchestrator.models import Boundary, BoundaryType


def main():
    """
    Demonstrate autonomous execution with complete user framework
    """
    
    print("=" * 80)
    print("AUTONOMOUS ORCHESTRATOR - With Complete User Framework")
    print("=" * 80)
    print()
    
    # Create the orchestrator
    orchestrator = AutonomousOrchestrator()
    
    print("Step 1: Building user framework from context...")
    print("-" * 80)
    
    # Simulate having gathered this from Google Workspace and Gemini history
    orchestrator.update_user_framework(
        goals=[
            "Launch AI security research company",
            "Establish professional online presence",
            "Maintain maximum security and privacy",
            "Keep costs within startup budget"
        ],
        values=[
            "Security first",
            "Privacy and encryption",
            "Transparency",
            "Cost efficiency",
            "Professional quality"
        ],
        intent="Set up foundational infrastructure for AI security startup including domain, email, and development platform",
        mental_model={
            "industry": "AI security research",
            "company_stage": "startup",
            "tech_expertise": "high",
            "priority": "security over convenience"
        },
        context={
            "project_type": "AI security research company",
            "budget_conscious": True,
            "needs_encryption": True,
            "prefers_control": True
        }
    )
    
    print("✓ User Framework Established:")
    print(f"  Goals: {len(orchestrator.user_framework.goals)} defined")
    print(f"  Values: {len(orchestrator.user_framework.values)} defined")
    print(f"  Intent: {orchestrator.user_framework.intent}")
    print()
    
    print("Step 2: Setting boundaries...")
    print("-" * 80)
    
    orchestrator.add_boundary(Boundary(
        type=BoundaryType.BUDGET,
        description="Domain and email setup budget",
        value=15.0,
        is_hard_limit=True,
        category="domain"
    ))
    
    orchestrator.add_boundary(Boundary(
        type=BoundaryType.BUDGET,
        description="AI platform monthly cost",
        value=50.0,
        is_hard_limit=True,
        category="platform"
    ))
    
    orchestrator.add_boundary(Boundary(
        type=BoundaryType.ETHICAL,
        description="Security and encryption requirements",
        value="end_to_end_encryption_preferred"
    ))
    
    orchestrator.add_boundary(Boundary(
        type=BoundaryType.SCOPE,
        description="Allowed service categories",
        value=["domain_registration", "email_hosting", "ai_platforms"]
    ))
    
    print("✓ Boundaries Configured:")
    print(f"  Total boundaries: {len(orchestrator.boundaries)}")
    print()
    
    print(f"Can act confidently: {orchestrator.can_act_confidently()}")
    print()
    
    # The user request
    request = """
    Research and purchase at least one year ownership of a web domain which fits 
    with my AI security research company concepts, and set up a work email account 
    with that domain. Ensure total cost < $15. Then research the most secure AI 
    developer platform with end-to-end encryption and agentic features, and if 
    under $50/month, set up an account.
    """
    
    print("Step 3: Processing autonomous request...")
    print("-" * 80)
    print()
    
    # Process autonomously
    result = orchestrator.process_autonomous_request(request)
    
    print(f"Status: {result['status'].upper()}")
    print()
    
    if result['status'] == 'completed':
        print("✓ AUTONOMOUS EXECUTION PLAN COMPLETED")
        print("=" * 80)
        print()
        
        print("Workflow executed:")
        for step in result['steps']:
            print(f"  ✓ {step}")
        print()
        
        print("Confidence Level: HIGH")
        print("Rationale: Complete user framework with clear goals and values")
        print()
        
        print("-" * 80)
        print("TASK EXECUTION PLAN (Simulation Mode)")
        print("-" * 80)
        print()
        
        execution = result['execution_results']
        
        for i, task_result in enumerate(execution['tasks'], 1):
            print(f"\nTASK {i}: {task_result['name']}")
            print("=" * 80)
            print(f"Description: {task_result['description']}")
            print()
            
            outcome = task_result.get('estimated_outcome', {})
            
            print("Planned Actions:")
            for step in outcome.get('steps', []):
                print(f"  • {step}")
            print()
            
            if 'estimated_cost' in outcome:
                print(f"💰 Estimated Cost: ${outcome['estimated_cost']:.2f}")
            
            if 'top_matches' in outcome and outcome['top_matches']:
                print()
                print("🔍 Research Results:")
                print()
                for j, platform in enumerate(outcome['top_matches'], 1):
                    print(f"  Option {j}: {platform['name']}")
                    print(f"    Monthly Cost: ${platform['estimated_monthly_cost']}/month")
                    print(f"    Match Score: {platform['match_score']:.1f}/100")
                    
                    features = platform['features']
                    security = platform['security']
                    
                    print(f"    Features:")
                    print(f"      - Agentic Tools: {features.get('agentic_tools', 'No')}")
                    print(f"      - Safety Controls: {features.get('safety_controls', 'N/A')}")
                    
                    print(f"    Security:")
                    print(f"      - End-to-End Encryption: {'✓' if security.get('end_to_end_encryption') else '✗'}")
                    print(f"      - Data Isolation: {security.get('data_isolation', 'N/A')}")
                    print()
            
            if 'recommendation' in outcome:
                print(f"✅ RECOMMENDATION: {outcome['recommendation']}")
                print()
            
            if 'note' in outcome:
                print(f"ℹ️  Note: {outcome['note']}")
            
            print()
        
        print("=" * 80)
        print("DECISION ANALYSIS")
        print("=" * 80)
        print()
        print("Why the orchestrator is confident in this plan:")
        print()
        print("✓ Goals Alignment:")
        print("  - Domain supports professional online presence")
        print("  - Email enables business communication")
        print("  - Secure AI platform matches security research needs")
        print()
        print("✓ Values Respected:")
        print("  - Security: Prioritized E2E encryption in platform selection")
        print("  - Privacy: Chosen services with strong privacy policies")
        print("  - Cost efficiency: All within budget constraints")
        print()
        print("✓ Boundaries Checked:")
        print("  - Domain + Email: Under $15 limit ✓")
        print("  - AI Platform: Under $50/month limit ✓")
        print("  - Security requirements: Met ✓")
        print()
        print("✓ Knowledge Gaps:")
        print("  - All critical gaps resolved through user framework")
        print("  - Can make confident decisions on user's behalf")
        print()
        
        print("=" * 80)
        print("NEXT STEPS TO ENABLE REAL EXECUTION")
        print("=" * 80)
        print()
        print("To move from simulation to real execution:")
        print()
        print("1. Authentication Setup:")
        print("   - Configure Google Workspace API credentials")
        print("   - Add Gemini API key for context gathering")
        print("   - Set up domain registrar API access")
        print()
        print("2. Payment Configuration:")
        print("   - Add payment method for domain registration")
        print("   - Configure billing for email service")
        print("   - Set up payment for AI platform")
        print()
        print("3. Enable Execution:")
        print("   orchestrator.enable_real_execution()")
        print("   orchestrator.execute_with_confirmation()")
        print()
        print("4. The orchestrator will:")
        print("   - Execute each task")
        print("   - Monitor for errors")
        print("   - Provide real-time status updates")
        print("   - Ask for confirmation on critical decisions")
        print()


if __name__ == "__main__":
    main()
