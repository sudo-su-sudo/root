"""
Example: Learning Orchestrator with Preference Learning and Meta-Reasoning

This demonstrates the enhanced orchestrator that learns WHY you make decisions
and identifies exact gaps in its understanding.
"""

from orchestrator import LearningOrchestrator, Boundary, BoundaryType


def main():
    print("=" * 80)
    print("LEARNING ORCHESTRATOR - Deep Preference Understanding")
    print("=" * 80)
    print()
    
    # Create learning orchestrator
    orch = LearningOrchestrator()
    
    # Set boundaries
    orch.add_boundary(Boundary(
        type=BoundaryType.BUDGET,
        description="Monthly spend limit",
        value=1000.0,
        category="operational"
    ))
    
    print("PHASE 1: Initial State - No Learning Yet")
    print("-" * 80)
    
    # Check initial understanding
    can_act, reason = orch.should_act_autonomously()
    print(f"Can act autonomously: {can_act}")
    print(f"Reason: {reason}")
    print()
    
    # Get initial progress
    progress = orch.get_progress_update("initial_assessment")
    print(f"Stage: {progress.stage}")
    print(f"Summary: {progress.summary}")
    print(f"Alignment: {progress.alignment_check}")
    print()
    
    if progress.questions_for_user:
        print("Questions to accelerate learning:")
        for i, q in enumerate(progress.questions_for_user, 1):
            print(f"  {i}. {q}")
    print()
    
    print("\n" + "=" * 80)
    print("PHASE 2: Learning from Decisions")
    print("=" * 80)
    print()
    
    # Simulate user making decisions (this is where learning happens)
    
    print("Decision 1: Infrastructure choice")
    print("-" * 40)
    orch.record_user_decision(
        situation="Choose cloud infrastructure provider",
        chosen_option="Premium tier with better reliability",
        rejected_options=["Cheap tier with basic features", "Mid-tier balanced option"],
        reasoning="I value reliability over cost savings for critical infrastructure",
        constraints={"budget": 500, "importance": "high"}
    )
    print("✓ Recorded decision - learned that reliability > cost for critical systems")
    print()
    
    print("Decision 2: Feature development priority")
    print("-" * 40)
    orch.record_user_decision(
        situation="Prioritize features for next sprint",
        chosen_option="Security improvements first",
        rejected_options=["New user-facing features", "Performance optimizations"],
        reasoning="Security is foundational - features can wait",
        constraints={"timeline": "2 weeks", "team_size": 5}
    )
    print("✓ Recorded decision - learned that security is top priority")
    print()
    
    print("Decision 3: Deployment approach")
    print("-" * 40)
    orch.record_user_decision(
        situation="Choose deployment strategy",
        chosen_option="Careful staged rollout with monitoring",
        rejected_options=["Quick full deployment", "Beta test with small group"],
        reasoning="Rather be thorough than fast when stability matters",
        constraints={"urgency": "medium"}
    )
    print("✓ Recorded decision - learned preference for thoroughness")
    print()
    
    print("Decision 4: Tool selection")
    print("-" * 40)
    orch.record_user_decision(
        situation="Select monitoring tool",
        chosen_option="Comprehensive solution with all features",
        rejected_options=["Basic free tool", "Mid-range tool"],
        reasoning="Quality tooling pays for itself in saved debugging time",
        constraints={"budget": 200, "importance": "operational"}
    )
    print("✓ Recorded decision - reinforced quality preference")
    print()
    
    print("\n" + "=" * 80)
    print("PHASE 3: Analyzing Learning Progress")
    print("=" * 80)
    print()
    
    # Get learning summary
    summary = orch.get_learning_summary()
    
    print(f"Understanding Level: {summary['understanding_level']}")
    print(f"Decisions Observed: {summary['decision_history_size']}")
    print(f"Patterns Identified: {summary['identified_patterns']}")
    print(f"Can Act Autonomously: {summary['can_act_autonomously']}")
    print()
    
    if summary['strong_patterns']:
        print("Strong Patterns Discovered:")
        for pattern in summary['strong_patterns']:
            print(f"  • {pattern}")
        print()
    
    if summary['confident_hypotheses']:
        print("Confident Hypotheses About Your Preferences:")
        for hyp in summary['confident_hypotheses']:
            print(f"  • {hyp}")
        print()
    
    if summary['dimension_scores']:
        print("Understanding Dimensions:")
        for dimension, score in summary['dimension_scores'].items():
            bars = "█" * int(score * 20)
            print(f"  {dimension:25s} [{bars:20s}] {int(score * 100)}%")
        print()
    
    if summary['recent_insights']:
        print("Recent Insights:")
        for insight in summary['recent_insights']:
            print(f"  • {insight}")
        print()
    
    print("\n" + "=" * 80)
    print("PHASE 4: Making Autonomous Decisions")
    print("=" * 80)
    print()
    
    # Now test if it can make decisions on our behalf
    
    print("Scenario 1: Database selection")
    print("-" * 40)
    options = [
        "Premium managed database with high availability",
        "Cheap self-hosted database",
        "Mid-tier managed service"
    ]
    
    chosen, confidence, reasoning, needs_confirm = orch.make_autonomous_decision(
        "Choose database for production",
        options
    )
    
    print(f"Predicted choice: {chosen}")
    print(f"Confidence: {int(confidence * 100)}%")
    print(f"Needs confirmation: {needs_confirm}")
    print(f"\nReasoning:\n{reasoning}")
    print()
    
    print("\nScenario 2: Code review process")
    print("-" * 40)
    options = [
        "Quick automated checks only",
        "Thorough manual review by team",
        "Minimal review for non-critical changes"
    ]
    
    chosen, confidence, reasoning, needs_confirm = orch.make_autonomous_decision(
        "Establish code review process",
        options
    )
    
    print(f"Predicted choice: {chosen}")
    print(f"Confidence: {int(confidence * 100)}%")
    print(f"Needs confirmation: {needs_confirm}")
    print(f"\nReasoning:\n{reasoning}")
    print()
    
    print("\n" + "=" * 80)
    print("PHASE 5: Meta-Reasoning - Understanding Gaps")
    print("=" * 80)
    print()
    
    # Demonstrate meta-reasoning
    explanation = orch.explain_uncertainty("Decide on marketing budget allocation")
    print(explanation)
    print()
    
    # Get critical gaps
    print("Critical Gaps in Understanding:")
    print("-" * 40)
    gaps = orch.identify_critical_gaps("strategic decision making")
    
    if gaps:
        for gap in gaps[:3]:
            print(f"\nGap: {gap.area}")
            print(f"  Description: {gap.description}")
            print(f"  Root Cause: {gap.root_cause.value}")
            print(f"  Impact: {gap.impact_on_decision}")
            print(f"  Resolution: {gap.suggested_resolution}")
    else:
        print("No critical gaps - ready for autonomous action!")
    print()
    
    print("\n" + "=" * 80)
    print("PHASE 6: Progress Update (High-Level)")
    print("=" * 80)
    print()
    
    # Generate user-facing progress update
    progress = orch.get_progress_update("learning_complete")
    
    print(f"📊 {progress.summary}")
    print()
    print(f"🎯 {progress.alignment_check}")
    print()
    
    if progress.key_insights:
        print("Key Insights:")
        for insight in progress.key_insights[-5:]:
            print(f"  💡 {insight}")
        print()
    
    if progress.next_steps:
        print("Next Steps:")
        for step in progress.next_steps:
            print(f"  → {step}")
        print()
    
    if progress.questions_for_user:
        print("Questions for You:")
        for q in progress.questions_for_user:
            print(f"  ❓ {q}")
        print()
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()
    
    can_act, reason = orch.should_act_autonomously()
    
    if can_act:
        print("✅ READY FOR AUTONOMOUS ACTION")
        print()
        print("The orchestrator has learned your preferences through observing")
        print("your decisions. It understands:")
        print()
        print("  • WHY you make the choices you make")
        print("  • Your value hierarchy (quality > cost, security > features)")
        print("  • Your risk tolerance and decision-making patterns")
        print("  • When you prefer thoroughness vs speed")
        print()
        print("It can now:")
        print("  • Make decisions on your behalf with high confidence")
        print("  • Identify exactly what it doesn't know (meta-reasoning)")
        print("  • Explain root causes of uncertainty")
        print("  • Provide high-level progress updates")
        print()
    else:
        print("⚠ NEEDS MORE LEARNING")
        print()
        print(f"Reason: {reason}")
        print()
        print("Continue making decisions and the orchestrator will learn")
        print("your patterns and preferences.")
    
    print("\n" + "=" * 80)
    print("KEY DIFFERENCES FROM BASIC ORCHESTRATOR")
    print("=" * 80)
    print()
    print("✓ Learns WHY you make decisions, not just what you decide")
    print("✓ Identifies ROOT CAUSES of gaps, not just symptoms")
    print("✓ Provides HIGH-LEVEL updates, not implementation details")
    print("✓ Makes CONFIDENT predictions based on learned patterns")
    print("✓ Performs META-REASONING about its own understanding")
    print("✓ Less transparent internally, but more effective externally")
    print()


if __name__ == "__main__":
    main()
