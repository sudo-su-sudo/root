# Autonomous AI Swarm Orchestrator

A sophisticated AI orchestrator that handles high-level requests within defined boundaries (budgets, ethics, time) while building a holistic understanding of user intent.

## Features

- **Anticipates Ambiguities**: Proactively identifies gaps in understanding before taking action
- **Targeted Clarification**: Asks focused questions to build a complete user mental model
- **Holistic User Framework**: Captures goals, values, intent, and preferences
- **Confident Decision Making**: Only acts when user values and intent are solidly understood
- **Boundary Enforcement**: Respects budget, ethical, temporal, and scope constraints
- **Knowledge Gap Identification**: Explicitly tracks what is unknown before proceeding
- **Confidence Scoring**: Transparent about certainty levels for each decision

## Installation

```bash
pip install -r requirements.txt
```

Or install in development mode:

```bash
pip install -e .
```

## Quick Start

### Basic Usage

```python
from orchestrator import SwarmOrchestrator

# Create an orchestrator
orchestrator = SwarmOrchestrator()

# Process a request (will ask for clarification if needed)
result = orchestrator.process_request("Build a new customer management system")

if result['status'] == 'needs_clarification':
    for question in result['clarification_questions']:
        print(question['question'])
```

### Complete Workflow

```python
from orchestrator import SwarmOrchestrator, Boundary, BoundaryType

# Create orchestrator
orchestrator = SwarmOrchestrator()

# Build user framework
orchestrator.update_user_framework(
    goals=["Improve customer satisfaction", "Reduce costs"],
    values=["Data privacy", "Transparency", "Quality"],
    intent="Build a robust CRM that respects user privacy"
)

# Set boundaries
orchestrator.add_boundary(Boundary(
    type=BoundaryType.BUDGET,
    description="Project budget",
    value=50000,
    is_hard_limit=True
))

orchestrator.add_boundary(Boundary(
    type=BoundaryType.ETHICAL,
    description="Privacy-first approach",
    value="no_data_sharing"
))

# Make a decision
decision = orchestrator.make_decision(
    request="Deploy CRM system",
    action="deploy_system",
    action_details={"cost": 30000, "duration": 60}
)

print(f"Confidence: {decision.confidence}")
print(f"Requires confirmation: {decision.requires_confirmation}")
print(f"Rationale: {decision.rationale}")
```

## Core Concepts

### User Framework

The orchestrator builds a holistic understanding of the user through:

- **Goals**: What the user wants to achieve
- **Values**: Principles and ethical guidelines
- **Intent**: The specific purpose of the current request
- **Mental Model**: Preferences and domain knowledge
- **Context**: Additional situational information

### Boundaries

Constraints that the orchestrator must respect:

- **BUDGET**: Financial limits
- **ETHICAL**: Ethical and moral guidelines
- **TEMPORAL**: Time constraints
- **SCOPE**: Domain or operational scope

### Knowledge Gaps

The orchestrator explicitly tracks what it doesn't know:

- **Area**: Which aspect is unclear (goals, values, budget, etc.)
- **Priority**: How critical the gap is (high/medium/low)
- **Required for Action**: Whether this must be resolved before acting

### Confidence Levels

Every decision has an associated confidence level:

- **HIGH**: Complete framework, all boundaries checked, clear alignment
- **MEDIUM**: Partial framework or minor gaps
- **LOW**: Significant gaps or boundary violations

## Architecture

### Key Components

1. **SwarmOrchestrator**: Main class that coordinates all operations
2. **UserFramework**: Stores user goals, values, intent, and mental model
3. **Boundary**: Defines operational constraints
4. **KnowledgeGap**: Tracks what is unknown
5. **ClarificationQuestion**: Targeted questions to resolve ambiguities
6. **Decision**: Records actions with confidence and rationale

### Decision Flow

```
Request → Identify Gaps → Generate Questions
                             ↓
                    Framework Complete?
                             ↓
              Check Boundaries → Calculate Confidence
                             ↓
                    Make Decision with Rationale
                             ↓
              Requires Confirmation? → Act or Confirm
```

## API Reference

### SwarmOrchestrator

#### Methods

- `add_boundary(boundary: Boundary)`: Add a constraint
- `update_user_framework(...)`: Update user goals, values, intent
- `identify_knowledge_gaps(request: str)`: Find what's unclear
- `generate_clarification_questions(gaps)`: Create targeted questions
- `check_boundaries(action, details)`: Verify constraints
- `calculate_confidence(request, details)`: Determine certainty level
- `make_decision(request, action, details)`: Make an informed decision
- `process_request(request: str)`: Main entry point
- `can_act_confidently()`: Check if ready to act

## Examples

See `examples.py` for comprehensive usage examples including:

1. Basic usage with clarification flow
2. Complete framework setup
3. Decision making with boundaries
4. Knowledge gap identification
5. Confidence level calculations

Run examples:

```bash
python examples.py
```

## Testing

Run the test suite:

```bash
pytest tests/ -v
```

Run with coverage:

```bash
pytest tests/ --cov=orchestrator --cov-report=html
```

## Design Principles

1. **Transparency**: Always explain decisions and confidence levels
2. **Safety First**: Never act without sufficient understanding
3. **User-Centric**: Build deep understanding of user mental model
4. **Proactive**: Anticipate issues before they arise
5. **Bounded**: Respect all defined constraints
6. **Iterative**: Continuously refine understanding through interaction

## Use Cases

- **Project Planning**: Ensure alignment with goals and budgets
- **Resource Allocation**: Make decisions within financial/ethical bounds
- **Task Delegation**: Understand intent before assigning work
- **Risk Assessment**: Identify gaps before committing to actions
- **Autonomous Systems**: Enable AI to act responsibly on user's behalf

## Contributing

Contributions are welcome! Please ensure:

1. Tests pass: `pytest tests/`
2. Code follows existing style
3. Documentation is updated
4. Changes are minimal and focused

## License

MIT License - See LICENSE file for details

## Philosophy

This orchestrator embodies the principle that AI should:

- **Ask before assuming**: Clarify ambiguities upfront
- **Understand holistically**: Build complete mental models
- **Act confidently only when justified**: Know when certainty is sufficient
- **Respect boundaries**: Honor user constraints absolutely
- **Be transparent**: Explain reasoning and confidence levels

The goal is confident, autonomous action grounded in solid understanding of user values and intent.