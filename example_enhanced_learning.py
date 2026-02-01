"""
Enhanced Example: Complete Learning Workflow

Shows the full cycle of learning, meta-reasoning, and autonomous decision-making.
"""

from orchestrator import LearningOrchestrator, Boundary, BoundaryType


def main():
    print("=" * 80)
    print("ENHANCED LEARNING ORCHESTRATOR")
    print("Understanding YOUR Reasoning, Not Just Your Choices")
    print("=" * 80)
    print()
    
    orch = LearningOrchestrator()
    
    # Step 1: Set some basic context
    print("STEP 1: Initial Setup")
    print("-" * 80)
    
    # Add some framework - but deliberately incomplete
    orch.update_user_framework(
        goals=["Build successful startup", "Maintain work-life balance"],
        values=["Quality", "Security", "Efficiency"],
        intent="Create sustainable tech company"
    )
    
    orch.add_boundary(Boundary(
        type=BoundaryType.BUDGET,
        description="Monthly operational budget",
        value=5000.0
    ))
    
    print("✓ Basic framework established (goals, some values, boundary)")
    print()
    
    # Step 2: Learn from decisions
    print("\nSTEP 2: Learning from Your Decisions")
    print("=" * 80)
    print()
    
    decisions = [
        {
            "situation": "Hiring first engineer - salary negotiation",
            "chosen": "Offered $120K (higher than budget) for excellent candidate",
            "rejected": ["Offered $90K (within budget)", "Kept searching for cheaper candidate"],
            "reasoning": "Quality of team is more important than strict budget adherence for key hires"
        },
        {
            "situation": "Security audit - comprehensive vs basic",
            "chosen": "Full comprehensive security audit ($3K)",
            "rejected": ["Basic audit ($500)", "Skip audit for now"],
            "reasoning": "Security failures are too expensive - invest upfront"
        },
        {
            "situation": "Office space decision",
            "chosen": "Remote-first with coworking budget",
            "rejected": ["Expensive downtown office", "Fully remote with no budget"],
            "reasoning": "Work-life balance matters, flexibility over prestige"
        },
        {
            "situation": "Development tools and software",
            "chosen": "Premium development tools ($200/month)",
            "rejected": ["Free/open source only", "Mix of free and paid"],
            "reasoning": "Efficiency of team is worth the investment"
        },
        {
            "situation": "Customer support vs new features",
            "chosen": "Improve existing features based on customer feedback",
            "rejected": ["Build new flashy features", "Focus only on support"],
            "reasoning": "Quality of existing features matters more than quantity"
        }
    ]
    
    for i, dec in enumerate(decisions, 1):
        print(f"Decision {i}: {dec['situation']}")
        orch.record_user_decision(
            situation=dec['situation'],
            chosen_option=dec['chosen'],
            rejected_options=dec['rejected'],
            reasoning=dec['reasoning']
        )
        print(f"  ✓ Chose: {dec['chosen']}")
        print(f"  💭 Because: {dec['reasoning']}")
        print()
    
    # Step 3: Analyze what was learned
    print("\nSTEP 3: What the Orchestrator Learned")
    print("=" * 80)
    print()
    
    summary = orch.get_learning_summary()
    
    print(f"📊 Understanding Level: {summary['understanding_level']}")
    print(f"📚 Decisions Analyzed: {summary['decision_history_size']}")
    print(f"🎯 Patterns Identified: {summary['identified_patterns']}")
    print()
    
    if summary['strong_patterns']:
        print("🔍 Discovered Strong Patterns:")
        for pattern in summary['strong_patterns']:
            print(f"   • {pattern}")
        print()
    
    if summary['confident_hypotheses']:
        print("💡 Confident Hypotheses About You:")
        for hyp in summary['confident_hypotheses']:
            print(f"   • {hyp}")
        print()
    
    print("📈 Understanding Dimensions:")
    for dim, score in summary['dimension_scores'].items():
        bar = "█" * int(score * 30)
        print(f"   {dim:20s} [{bar:30s}] {int(score*100):3d}%")
    print()
    
    # Step 4: Test autonomous decision-making
    print("\nSTEP 4: Making Decisions on Your Behalf")
    print("=" * 80)
    print()
    
    scenarios = [
        {
            "context": "New server infrastructure needed",
            "options": [
                "Premium cloud with 99.99% uptime ($800/month)",
                "Standard cloud with 99.9% uptime ($300/month)",
                "Cheap VPS ($50/month)"
            ]
        },
        {
            "context": "Code quality tooling decision",
            "options": [
                "Comprehensive suite with all tools ($400/month)",
                "Basic linting only (free)",
                "Mid-range tools ($150/month)"
            ]
        },
        {
            "context": "Hiring strategy for next role",
            "options": [
                "Hire senior engineer at $140K",
                "Hire junior engineer at $70K",
                "Use contractor temporarily at $100/hour"
            ]
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\nScenario {i}: {scenario['context']}")
        print("-" * 60)
        
        chosen, confidence, reasoning, needs_confirm = orch.make_autonomous_decision(
            scenario['context'],
            scenario['options'],
            require_high_confidence=False  # Allow medium confidence
        )
        
        print(f"🤖 Predicted Choice: {chosen}")
        print(f"📊 Confidence: {int(confidence * 100)}%")
        print(f"{'❓ Needs Confirmation: YES' if needs_confirm else '✅ Can Proceed Autonomously'}")
        print()
        print(f"💭 Reasoning Summary:")
        # Show just the key parts
        lines = reasoning.split(". ")
        for line in lines[:3]:  # First 3 sentences
            if line.strip():
                print(f"   {line.strip()}")
        print()
    
    # Step 5: Meta-Reasoning - Understanding Gaps
    print("\nSTEP 5: Meta-Reasoning - What's Still Uncertain")
    print("=" * 80)
    print()
    
    gaps = orch.identify_critical_gaps("strategic long-term planning")
    
    if gaps:
        print("🔍 Identified Gaps in Understanding:")
        for gap in gaps[:3]:
            print(f"\n   Area: {gap.area}")
            print(f"   Root Cause: {gap.root_cause.value}")
            print(f"   Impact: {gap.impact_on_decision}")
            print(f"   How to Resolve: {gap.suggested_resolution}")
    else:
        print("✅ No critical gaps - ready for fully autonomous operation!")
    print()
    
    # Step 6: High-Level Progress Report
    print("\nSTEP 6: High-Level Progress Report")
    print("=" * 80)
    print()
    
    progress = orch.get_progress_update("operational")
    
    print(f"📍 Current Stage: {progress.stage}")
    print(f"📊 {progress.summary}")
    print()
    print(f"🎯 Alignment Status:")
    print(f"   {progress.alignment_check}")
    print()
    
    if progress.key_insights:
        print("💡 Recent Key Insights:")
        for insight in progress.key_insights[-3:]:
            print(f"   • {insight}")
        print()
    
    if progress.next_steps:
        print("⏭️  Next Steps:")
        for step in progress.next_steps:
            print(f"   → {step}")
        print()
    
    # Step 7: Can it act autonomously?
    print("\nSTEP 7: Autonomous Action Readiness")
    print("=" * 80)
    print()
    
    can_act, reason = orch.should_act_autonomously("operational")
    
    if can_act:
        print("✅ READY FOR AUTONOMOUS OPERATION")
        print()
        print(f"   {reason}")
        print()
        print("   The orchestrator can now:")
        print("   • Make operational decisions without asking")
        print("   • Understand WHY you would choose each option")
        print("   • Identify exactly what it doesn't know")
        print("   • Provide high-level check-ins about direction")
        print()
    else:
        print("⚠️  STILL LEARNING")
        print()
        print(f"   {reason}")
        print()
        print("   Continue making decisions and providing reasoning.")
        print("   The system will continue learning your patterns.")
    
    # Step 8: Demonstrate meta-reasoning
    print("\nSTEP 8: Deep Dive - Meta-Reasoning Example")
    print("=" * 80)
    print()
    
    explanation = orch.explain_uncertainty("Decide between growth vs profitability focus")
    print("Question: How should we balance growth vs profitability?")
    print()
    print(explanation)
    print()
    
    # Final summary
    print("\n" + "=" * 80)
    print("COMPARISON: Traditional vs Learning Orchestrator")
    print("=" * 80)
    print()
    
    print("Traditional Orchestrator:")
    print("  • Asks: 'What are your values?'")
    print("  • You tell it: 'Quality, Security'")
    print("  • It checks: 'Does this violate values?' → Yes/No")
    print()
    
    print("Learning Orchestrator:")
    print("  • Observes: You chose expensive but reliable option")
    print("  • Learns: 'User prioritizes reliability over cost for critical systems'")
    print("  • Predicts: 'For server infrastructure, choose premium tier'")
    print("  • Meta-reasons: 'I don't know how they balance growth vs profit'")
    print("  • Identifies: 'Missing: tradeoff function for strategic decisions'")
    print("  • Suggests: 'Ask about long-term goals to understand tradeoff'")
    print()
    
    print("Key Advantage:")
    print("  ✓ Understands the WHY behind your decisions")
    print("  ✓ Can extrapolate to new situations")
    print("  ✓ Knows what it doesn't know (meta-reasoning)")
    print("  ✓ Less micromanagement, more strategic alignment")
    print()


if __name__ == "__main__":
    main()
