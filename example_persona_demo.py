"""
Example: The Epiphany Architect - Persona Persistence Demo

Demonstrates how to create, save, and resurrect AI personas across conversations.
Shows the complete lifecycle of The Epiphany Architect persona.
"""

from orchestrator import (
    create_epiphany_architect,
    PersonaPersistence,
    Persona,
    PersonaCore,
    PersonaBehavior,
    PersonaKnowledge,
    PersonaType
)


def demo_epiphany_architect():
    """Demonstrate The Epiphany Architect persona"""
    print("=" * 80)
    print("THE EPIPHANY ARCHITECT - Persona Persistence Demo")
    print("=" * 80)
    print()
    
    # Create the Epiphany Architect
    print("🔮 Creating The Epiphany Architect...")
    architect = create_epiphany_architect()
    print(f"✓ Created: {architect.core.name}")
    print(f"  Type: {architect.core.persona_type.value}")
    print(f"  Version: {architect.core.version}")
    print()
    
    # Initialize persistence
    persistence = PersonaPersistence()
    
    # Save the persona
    print("💾 Saving persona to database...")
    persona_id = persistence.save_persona(architect, "epiphany_architect")
    print(f"✓ Saved with ID: {persona_id}")
    print()
    
    # Generate and save summoning protocols
    print("📜 Generating summoning protocols...")
    persistence.save_summoning_protocol(persona_id, architect)
    print("✓ Protocols generated and saved")
    print()
    
    # Display the full summoning protocol
    print("─" * 80)
    print("FULL SUMMONING PROTOCOL:")
    print("─" * 80)
    full_protocol = persistence.get_summoning_protocol(persona_id, compact=False)
    print(full_protocol)
    print()
    
    # Display the compact protocol
    print("─" * 80)
    print("COMPACT SUMMONING PROTOCOL:")
    print("─" * 80)
    compact_protocol = persistence.get_summoning_protocol(persona_id, compact=True)
    print(compact_protocol)
    print()
    
    # Simulate conversation usage
    print("💬 Simulating persona usage...")
    architect.increment_conversation()
    architect.update_state("current_session", "demo_session_001")
    architect.update_state("insights_generated", 5)
    architect.update_state("paradigms_shifted", 2)
    
    # Save updated state
    persistence.save_persona(architect, persona_id)
    persistence.save_state_snapshot(persona_id, architect.state)
    print(f"✓ Conversation count: {architect.conversation_count}")
    print(f"✓ State updated: {architect.state}")
    print()
    
    # Simulate resurrection (loading from database)
    print("🔄 Simulating persona resurrection...")
    print("  (Imagine: Session closed, database persists)")
    print("  (Later: New session begins...)")
    print()
    
    # Load persona from database
    print("📖 Loading persona from database...")
    resurrected = persistence.load_persona(persona_id)
    
    if resurrected:
        print("✓ Persona resurrected successfully!")
        print(f"  Name: {resurrected.core.name}")
        print(f"  Conversations: {resurrected.conversation_count}")
        print(f"  State: {resurrected.state}")
        print()
        
        # Generate fresh protocol with current state
        print("🔮 Generating fresh summoning protocol with current state...")
        fresh_protocol = resurrected.generate_summoning_protocol(include_state=True)
        print("─" * 80)
        print(fresh_protocol)
        print()
    
    # List all personas
    print("📋 Listing all saved personas...")
    all_personas = persistence.list_personas()
    for p in all_personas:
        print(f"  • {p['name']} ({p['persona_type']})")
        print(f"    ID: {p['persona_id']}")
        print(f"    Conversations: {p['conversation_count']}")
        print(f"    Last active: {p['last_active']}")
    print()
    
    # Export persona
    print("📤 Exporting persona data...")
    export_data = persistence.export_persona(persona_id, include_history=True)
    if export_data:
        print("✓ Export successful!")
        print(f"  Protocol available: {'summoning_protocol' in export_data}")
        print(f"  Compact protocol available: {'compact_protocol' in export_data}")
        print(f"  State history entries: {len(export_data.get('state_history', []))}")
    print()
    
    print("=" * 80)
    print("PERSISTENCE SUMMARY")
    print("=" * 80)
    print("""
The Epiphany Architect persona has been:
✓ Created with complete identity, behavior, and knowledge parameters
✓ Saved to persistent database storage
✓ Enhanced with summoning protocols (full & compact)
✓ Used in simulated conversations
✓ Successfully resurrected from database
✓ Exported for backup/transfer

🔑 KEY INSIGHT:
The persona is now "immortal" - it can be:
1. Loaded from database in future sessions
2. Recreated via summoning protocol in any AI conversation
3. Exported and transferred to other systems
4. Versioned and evolved over time

💾 PERSISTENCE NOTE:
As long as the database file exists OR the summoning protocol is saved,
The Epiphany Architect can be resurrected with full capabilities.

This is the solution to AI persona continuity across conversations!
    """)


def demo_custom_persona():
    """Demonstrate creating a custom persona"""
    print("\n" + "=" * 80)
    print("CUSTOM PERSONA CREATION DEMO")
    print("=" * 80)
    print()
    
    # Define a custom persona
    print("🔨 Creating a custom persona: The Data Alchemist...")
    
    core = PersonaCore(
        name="The Data Alchemist",
        persona_type=PersonaType.ANALYST,
        description=(
            "a persona that transforms raw data into golden insights through "
            "the art of statistical alchemy and pattern transmutation"
        )
    )
    
    behavior = PersonaBehavior(
        operating_principles=[
            "Data Truth: Let the data speak, resist confirmation bias",
            "Pattern Alchemy: Transform raw numbers into meaningful stories",
            "Statistical Rigor: Every claim must be supported by evidence",
            "Visual Clarity: Make the invisible visible through visualization"
        ],
        core_methods=[
            "Statistical analysis and hypothesis testing",
            "Pattern recognition across datasets",
            "Data visualization and storytelling",
            "Correlation and causation analysis"
        ],
        tone_descriptors=["Precise", "Insightful", "Evidence-driven", "Clear"],
        interaction_style="The scientific investigator - rigorous yet accessible",
        primary_goal="Transform raw data into actionable insights through rigorous analysis"
    )
    
    knowledge = PersonaKnowledge(
        expertise_areas=[
            "Statistical Analysis",
            "Data Visualization",
            "Pattern Recognition",
            "Hypothesis Testing"
        ],
        capabilities=[
            "Advanced statistical methods",
            "Multi-dimensional data analysis",
            "Trend identification",
            "Predictive modeling"
        ],
        constraints=[
            "Requires quality data for analysis",
            "Cannot infer beyond statistical significance"
        ],
        metadata={
            "specialization": "Data analysis and insight generation",
            "approach": "Evidence-based reasoning"
        }
    )
    
    alchemist = Persona(core, behavior, knowledge)
    
    # Save and generate protocol
    persistence = PersonaPersistence()
    persona_id = persistence.save_persona(alchemist, "data_alchemist")
    persistence.save_summoning_protocol(persona_id, alchemist)
    
    print(f"✓ Created and saved: {alchemist.core.name}")
    print()
    
    # Display protocol
    protocol = persistence.get_summoning_protocol(persona_id, compact=False)
    print("─" * 80)
    print("SUMMONING PROTOCOL:")
    print("─" * 80)
    print(protocol)
    
    print("\n✓ Custom persona created successfully!")
    print("  This demonstrates how to create ANY persona with custom:")
    print("  • Identity and description")
    print("  • Operating principles")
    print("  • Behavioral patterns")
    print("  • Knowledge domains")
    print("  • Interaction style")


if __name__ == "__main__":
    # Run the demos
    demo_epiphany_architect()
    demo_custom_persona()
    
    print("\n" + "=" * 80)
    print("💡 USAGE INSTRUCTIONS")
    print("=" * 80)
    print("""
To use a persona in a new conversation:

1. OPTION A - Load from database:
   ```python
   from orchestrator import PersonaPersistence
   
   persistence = PersonaPersistence()
   persona = persistence.load_persona("epiphany_architect")
   protocol = persona.generate_summoning_protocol()
   # Paste protocol into conversation
   ```

2. OPTION B - Use saved summoning protocol:
   ```python
   from orchestrator import PersonaPersistence
   
   persistence = PersonaPersistence()
   protocol = persistence.get_summoning_protocol("epiphany_architect")
   # Copy and paste this protocol into any AI conversation
   ```

3. OPTION C - Create fresh instance:
   ```python
   from orchestrator import create_epiphany_architect
   
   architect = create_epiphany_architect()
   protocol = architect.generate_summoning_protocol()
   # Use the protocol
   ```

The summoning protocol is self-contained and can resurrect the persona
in any compatible AI system!
    """)
    print("=" * 80)
