# Autonomous AI Swarm Orchestrator

A sophisticated AI orchestrator that handles high-level requests within defined boundaries (budgets, ethics, time) while building a holistic understanding of user intent. **This system can autonomously execute real-world tasks** like domain registration, email setup, and platform selection.

## Key Capabilities

### Core Features

- ✅ **Anticipates Ambiguities**: Proactively identifies gaps in understanding before taking action
- ✅ **Targeted Clarification**: Asks focused questions upfront to build a complete user mental model
- ✅ **Holistic User Framework**: Captures goals, values, intent, and preferences
- ✅ **Confident Decision Making**: Only acts when user values and intent are solidly understood
- ✅ **Boundary Enforcement**: Respects budget, ethical, temporal, and scope constraints
- ✅ **Knowledge Gap Identification**: Explicitly tracks what is unknown before proceeding
- ✅ **Confidence Scoring**: Transparent about certainty levels for each decision

### Autonomous Execution (NEW!)

- ✅ **Task Decomposition**: Breaks complex requests into manageable executable steps
- ✅ **Context Gathering**: Integrates with Google Workspace and Gemini for user context
- ✅ **Service Integrations**: Domain registrars, email providers, AI platforms
- ✅ **Multi-step Workflows**: Handles dependencies between tasks automatically
- ✅ **Real-world Actions**: Simulates domain purchase, email setup, platform research
- ✅ **Safety First**: Simulation mode by default with explicit confirmation requirements

## Real-World Example

The orchestrator handles complex, multi-part requests like:

> "Research and purchase a web domain matching my project concepts from Google Docs, set up a work email with that domain (total cost < $15), then research the most secure AI platform with end-to-end encryption and agentic features (< $50/month), and set up an account if suitable."

**What the orchestrator does:**

1. **Identifies knowledge gaps** - Do I understand your goals, values, and intent?
2. **Asks clarifying questions** - Builds complete mental model upfront
3. **Decomposes request** - Breaks into: domain research, domain purchase, email setup, AI platform research
4. **Checks boundaries** - Ensures each step respects budget and ethical constraints
5. **Researches options** - Finds platforms matching requirements (encryption, features, cost)
6. **Makes recommendations** - Selects best option based on your value framework
7. **Requires confirmation** - Shows plan before executing (safety first!)

## Installation

```bash
pip install -r requirements.txt
```

Or install in development mode:

```bash
pip install -e .
```

## Quick Start

### Example 1: Basic Autonomous Request

```python
from orchestrator import AutonomousOrchestrator
from orchestrator.models import Boundary, BoundaryType

# Create orchestrator
orch = AutonomousOrchestrator()

# Set boundaries
orch.add_boundary(Boundary(
    type=BoundaryType.BUDGET,
    description="Total budget",
    value=100.0,
    category="general"
))

# Process request
request = "Help me set up my online business infrastructure"
result = orch.process_autonomous_request(request)

# Result will ask clarifying questions since framework is empty
if result['status'] == 'needs_clarification':
    for q in result['clarification_questions']:
        print(q['question'])
```

### Example 2: With Complete User Framework

```python
from orchestrator import AutonomousOrchestrator
from orchestrator.models import Boundary, BoundaryType

# Create orchestrator
orch = AutonomousOrchestrator()

# Build user framework (normally gathered from Google Docs/Gemini)
orch.update_user_framework(
    goals=["Launch AI security company", "Establish professional presence"],
    values=["Security first", "Privacy", "Cost efficiency"],
    intent="Set up foundational infrastructure for AI security startup"
)

# Set specific boundaries
orch.add_boundary(Boundary(
    type=BoundaryType.BUDGET,
    description="Domain and email budget",
    value=15.0,
    category="domain"
))

orch.add_boundary(Boundary(
    type=BoundaryType.BUDGET,
    description="AI platform monthly cost",
    value=50.0,
    category="platform"
))

# Now it can act confidently!
request = """
Research and purchase a domain for my AI security company, 
set up email (< $15 total), and find the best secure AI 
platform with encryption (< $50/month)
"""

result = orch.process_autonomous_request(request)

if result['status'] == 'completed':
    print("✓ Plan ready for execution")
    for task in result['execution_results']['tasks']:
        print(f"  - {task['name']}: {task['description']}")
```

See `example_real_world.py` and `example_with_framework.py` for complete working examples.

## Architecture

### System Components

```
AutonomousOrchestrator
├── UserFramework (goals, values, intent, mental model)
├── BoundaryChecker (budget, ethical, temporal, scope)
├── KnowledgeGapIdentifier (what's missing?)
├── TaskExecutor (decompose and execute)
├── ContextAggregator (Google Workspace + Gemini)
└── ServiceRegistry (domain, email, AI platforms)
```

### Decision Flow

```
High-level Request
      ↓
Gather Context (Google Docs, Gemini history)
      ↓
Identify Knowledge Gaps → Generate Clarifying Questions
      ↓                           ↓
Framework Complete?        Answer Questions
      ↓ Yes                      ↓
Decompose into Tasks ←──────────┘
      ↓
Check Each Task Against Boundaries
      ↓
Calculate Confidence Level
      ↓
High Confidence? → Execute (with confirmation)
Low/Medium → Ask for approval
```

## Core Concepts

### User Framework

The orchestrator builds a holistic understanding through:

- **Goals**: What you want to achieve (e.g., "Launch startup", "Cut costs")
- **Values**: Your principles (e.g., "Privacy first", "Quality over speed")
- **Intent**: Specific purpose of current request
- **Mental Model**: Your preferences and patterns
- **Context**: Domain knowledge and situation

### Boundaries (with Categories!)

Constraints with optional categories for precise matching:

```python
Boundary(
    type=BoundaryType.BUDGET,
    value=50.0,
    category="platform"  # Only applies to platform-related costs
)
```

Types:
- **BUDGET**: Financial limits (can have categories)
- **ETHICAL**: Moral guidelines (e.g., "privacy_required")
- **TEMPORAL**: Time constraints
- **SCOPE**: Allowed operation domains

### Knowledge Gaps

Explicit tracking of unknowns:

```python
KnowledgeGap(
    area="budget",
    description="No budget specified for domain",
    priority="high",
    required_for_action=True  # Must resolve before acting
)
```

### Confidence Levels

Every decision includes confidence:

- **HIGH**: Complete framework + all boundaries met + no critical gaps
- **MEDIUM**: Partial framework or minor uncertainties
- **LOW**: Significant gaps or boundary violations

## Service Integrations

### Available Integrations

1. **Domain Registrars** - Search, check availability, purchase domains
2. **Email Providers** - Create work email accounts
3. **AI Platform Researcher** - Compare platforms by security, features, pricing

### Adding New Services

```python
from orchestrator.services import ServiceIntegration

class MyService(ServiceIntegration):
    def authenticate(self, credentials):
        # Auth logic
        pass
    
    def execute_action(self, action, parameters):
        # Execute logic
        pass

# Register
orch.service_registry.register_service("my_service", MyService())
```

## Context Gathering

### Google Workspace Integration

```python
from orchestrator.context import GoogleWorkspaceContextProvider

provider = GoogleWorkspaceContextProvider(credentials_path="creds.json")
orch.context_aggregator.add_provider("google_workspace", provider)

# Automatically extracts:
# - Project concepts from documents
# - Goals from folder contents
# - Collaboration patterns
```

### Gemini Integration

```python
from orchestrator.context import GeminiContextProvider

provider = GeminiContextProvider(api_key="YOUR_API_KEY")
orch.context_aggregator.add_provider("gemini", provider)

# Extracts from conversation history:
# - Stated preferences
# - Project history
# - Interaction patterns
```

## Running Examples

```bash
# Basic usage - shows clarification questions
python example_real_world.py

# Complete workflow - shows autonomous execution
python example_with_framework.py

# Original examples
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

1. **Safety First**: Simulation mode by default, explicit confirmation for real actions
2. **Transparency**: Always explain decisions and confidence levels
3. **Never Assume**: Ask questions upfront rather than guess
4. **User-Centric**: Build deep understanding of user mental model
5. **Proactive**: Anticipate issues before they arise
6. **Bounded**: Respect all defined constraints absolutely
7. **Iterative**: Continuously refine understanding through interaction

## Enabling Real Execution

**IMPORTANT**: Current implementation runs in **simulation mode** for safety.

To enable real execution:

1. **Set up authentication**:
   ```python
   orch.setup_context_providers(
       google_credentials="path/to/creds.json",
       gemini_api_key="YOUR_API_KEY"
   )
   ```

2. **Configure payment methods** for domain/email services

3. **Enable service API access**:
   ```python
   # Example: Domain registrar
   registrar = orch.service_registry.get_service("domain_registrar")
   registrar.authenticate({"api_key": "YOUR_API_KEY"})
   ```

4. **Review and confirm** each execution plan before proceeding

## Use Cases

### Startup Infrastructure Setup
- Domain research and registration
- Professional email accounts
- Development platform selection
- All within budget constraints

### Research and Analysis
- Compare service providers
- Evaluate options against criteria
- Make recommendations based on values

### Autonomous Task Management
- Break down complex requests
- Execute multi-step workflows
- Handle dependencies automatically

### Decision Support
- Identify ambiguities in requirements
- Ask targeted clarifying questions
- Build confidence through understanding

## Philosophy

This orchestrator embodies the principle that AI should:

- **Ask before assuming**: Clarify ambiguities upfront
- **Understand holistically**: Build complete mental models
- **Act confidently only when justified**: Know when certainty is sufficient
- **Respect boundaries**: Honor user constraints absolutely
- **Be transparent**: Explain reasoning and confidence levels
- **Prioritize safety**: Simulate before executing

The goal is **confident, autonomous action grounded in solid understanding of user values and intent**.

## Contributing

Contributions are welcome! Please ensure:

1. Tests pass: `pytest tests/`
2. Code follows existing style
3. Documentation is updated
4. Changes are minimal and focused

## License

MIT License - See LICENSE file for details