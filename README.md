# Autonomous AI Swarm Orchestrator

A sophisticated AI orchestrator that **learns WHY you make decisions** and can act autonomously on your behalf. It prioritizes deep understanding of your reasoning over rigid transparency, using preference learning and meta-reasoning to build confidence in its decisions.

## 🌟 NEW: Mobile-Friendly Web Interface!

**Use the orchestrator from your phone's browser - no coding required!**

```bash
python3 web_app.py
# Then open http://localhost:5000 in your browser
```

- 📱 **Mobile-optimized** - Works perfectly on phones
- 💬 **Chat interface** - Natural conversation
- 📝 **Record decisions** - Simple forms
- 🔮 **Get predictions** - Based on learned patterns
- 💡 **View insights** - See what it learned

See [WEB_INTERFACE_GUIDE.md](WEB_INTERFACE_GUIDE.md) for complete instructions!

![Web Interface](https://github.com/user-attachments/assets/34879f84-a138-4c04-85ea-fe7ee4d42e55)

## Two Modes of Operation

### 1. Basic Orchestrator (Transparent & Rule-Based)
- Explicitly defined values and boundaries
- Clear rule checking
- Transparent decision logic
- Good when you want full visibility

### 2. Learning Orchestrator (NEW! - Deep Understanding)
- **Learns from your decisions** to understand your reasoning patterns
- **Meta-reasoning** about what it doesn't know
- **Predicts preferences** based on learned patterns
- **Identifies root causes** of uncertainty, not just symptoms
- Better when you want autonomous action with strategic check-ins

## Key Capabilities

### Preference Learning (NEW!)

- ✅ **Learns WHY You Decide**: Not just what you choose, but the reasoning behind it
- ✅ **Pattern Recognition**: Identifies your decision-making heuristics automatically
- ✅ **Preference Inference**: Predicts what you'd choose in new situations
- ✅ **Value Hierarchy Learning**: Discovers which values matter most from your choices
- ✅ **Tradeoff Understanding**: Learns how you balance competing factors

### Meta-Reasoning (NEW!)

- ✅ **Root Cause Analysis**: Identifies WHY it's uncertain, not just THAT it's uncertain
- ✅ **Gap Categorization**: 8 types of knowledge gaps with specific resolution strategies
- ✅ **Impact Assessment**: Understands how each gap affects decision-making
- ✅ **Strategic Recommendations**: Suggests what would most improve understanding
- ✅ **Confidence Decomposition**: Breaks down uncertainty into addressable components

### High-Level Progress Reports (NEW!)

- ✅ **Big Picture Updates**: Strategic direction, not implementation details
- ✅ **Alignment Checks**: Regular confirmation of shared understanding
- ✅ **Key Insights**: What the system has learned about you
- ✅ **Minimal Micromanagement**: Focuses on what matters to you

### Core Features (Enhanced)

- ✅ **Anticipates Ambiguities**: Proactively identifies gaps in understanding before taking action
- ✅ **Targeted Clarification**: Asks focused questions upfront to build a complete user mental model
- ✅ **Holistic User Framework**: Captures goals, values, intent, and preferences
- ✅ **Confident Decision Making**: Only acts when user values and intent are solidly understood
- ✅ **Boundary Enforcement**: Respects budget, ethical, temporal, and scope constraints
- ✅ **Knowledge Gap Identification**: Explicitly tracks what is unknown before proceeding
- ✅ **Confidence Scoring**: Transparent about certainty levels for each decision

### Autonomous Execution

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

### Example 1: Learning Orchestrator (Recommended)

```python
from orchestrator import LearningOrchestrator

# Create learning orchestrator
orch = LearningOrchestrator()

# Set initial framework (basic)
orch.update_user_framework(
    goals=["Build successful startup"],
    values=["Quality", "Security", "Efficiency"]
)

# Learn from your decisions
orch.record_user_decision(
    situation="Choose cloud infrastructure",
    chosen_option="Premium tier with 99.99% uptime ($800/month)",
    rejected_options=["Standard tier ($300/month)", "Cheap VPS ($50/month)"],
    reasoning="Reliability is worth the cost for critical systems"
)

orch.record_user_decision(
    situation="Hire engineer - budget vs quality",
    chosen_option="Offer $120K for excellent candidate",
    rejected_options=["Stay within $90K budget", "Keep searching"],
    reasoning="Quality of team matters more than strict budget adherence"
)

# After learning, it can make decisions autonomously
chosen, confidence, reasoning, needs_confirm = orch.make_autonomous_decision(
    "Choose database solution",
    [
        "Premium managed database ($500/month)",
        "Basic managed database ($100/month)",
        "Self-hosted ($minimal cost)"
    ]
)

print(f"Predicted: {chosen}")
print(f"Confidence: {int(confidence * 100)}%")
print(f"Reasoning: {reasoning}")

# Meta-reasoning: What doesn't it know?
explanation = orch.explain_uncertainty("Decide on marketing spend")
print(explanation)
# Shows: "Don't know how user trades off growth vs profitability"
#        "Root cause: ambiguous_tradeoff"
#        "Resolution: Ask about strategic priorities"

# High-level progress
progress = orch.get_progress_update("operational")
print(progress.summary)  # "Understanding level: 45% - Can make some decisions"
print(progress.alignment_check)  # "✓ Strong alignment on quality preferences"
```

### Example 2: Basic Autonomous Request

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

### Example 3: With Complete User Framework

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

## Learning & Meta-Reasoning (NEW!)

### Preference Learning

The `LearningOrchestrator` learns from your decisions to understand WHY you choose things:

```python
from orchestrator import LearningOrchestrator

orch = LearningOrchestrator()

# Record decisions with reasoning
orch.record_user_decision(
    situation="Infrastructure choice",
    chosen_option="Premium tier",
    rejected_options=["Budget tier", "Mid-range"],
    reasoning="Reliability is more important than cost for critical systems"
)

# System learns:
# - Pattern: "User prioritizes reliability over cost"
# - Hypothesis: "User prefers quality for critical systems"
# - Value weight: reliability = 0.8, cost = 0.4
```

**What it learns:**
- Decision patterns (e.g., "prefers quality over cost")
- Reasoning heuristics (e.g., "thorough when important, fast when routine")
- Value hierarchies (which values trump others)
- Tradeoff functions (how you balance competing factors)

### Meta-Reasoning

Goes beyond "I don't know" to "I don't know BECAUSE...":

```python
# Traditional gap: "Missing: user values"
# Meta-reasoning gap:
EnhancedKnowledgeGap(
    area="value_priority_ranking",
    description="Have 3 values but don't know relative priorities",
    root_cause=GapRootCause.MISSING_VALUE_PRIORITY,
    impact_on_decision="Cannot resolve conflicts when values compete",
    suggested_resolution="Ask user to rank values or observe value conflicts"
)
```

**8 Root Cause Types:**
1. `MISSING_VALUE_PRIORITY` - Don't know which value matters more
2. `MISSING_GOAL_CONTEXT` - Don't know why goal exists
3. `CONFLICTING_PATTERNS` - Past decisions contradict
4. `INSUFFICIENT_EXAMPLES` - Haven't seen this situation before
5. `AMBIGUOUS_TRADEOFF` - Don't know how to trade off X vs Y
6. `MISSING_CONSTRAINT_IMPORTANCE` - Don't know if boundary is flexible
7. `UNCLEAR_SUCCESS_METRIC` - Don't know what "good" looks like
8. `CONTEXT_DEPENDENCY` - Preference varies with context

### Framework Completeness

Quantitative measure of understanding:

```python
completeness = orch.analyze_understanding()

print(f"Overall: {completeness.overall_score}")  # 0-1 scale
print(f"Goal clarity: {completeness.dimension_scores['goal_clarity']}")
print(f"Value hierarchy: {completeness.dimension_scores['value_hierarchy']}")
print(f"Can act autonomously: {completeness.is_sufficient_for_autonomous_action()}")
```

**Dimensions:**
- **Goal Clarity**: How well goals are understood (based on decision consistency)
- **Value Hierarchy**: Understanding of value priorities (based on patterns)
- **Pattern Confidence**: Strength of identified patterns
- **Hypothesis Quality**: Confidence in preference hypotheses

### High-Level Progress Reports

Strategic updates, not implementation details:

```python
progress = orch.get_progress_update("operational")

print(progress.summary)
# "Understanding level: 65% - Can act confidently on operational decisions"

print(progress.alignment_check)
# "✓ Strong alignment - confident in understanding your preferences"

print(progress.key_insights)
# ["Learned: Quality > cost for critical systems",
#  "Pattern: Prefers thoroughness over speed",
#  "Hypothesis: Values team quality highly"]

print(progress.next_steps)
# ["Ready to execute decisions autonomously",
#  "Will check in on strategic changes"]
```

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
# NEW: Learning orchestrator with preference learning
python example_enhanced_learning.py

# Shows complete learning workflow:
# - Records decisions with reasoning
# - Learns patterns and hypotheses  
# - Makes autonomous predictions
# - Performs meta-reasoning about gaps
# - Provides high-level progress updates

# Learning orchestrator basics
python example_learning.py

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

### Learning Orchestrator Philosophy

1. **Deep Understanding Over Transparency**: Learns WHY you decide, not just what
2. **Strategic Alignment**: High-level check-ins, not micromanagement
3. **Meta-Reasoning**: Knows what it doesn't know and why
4. **Pattern-Based**: Infers from examples rather than requiring explicit rules
5. **Confident Autonomy**: Acts independently when understanding is solid
6. **Root Cause Focus**: Identifies exact gaps, not just symptoms

### General Principles

1. **Safety First**: Simulation mode by default, explicit confirmation for real actions
2. **Never Assume**: Ask questions upfront rather than guess
3. **User-Centric**: Build deep understanding of user mental model
4. **Proactive**: Anticipate issues before they arise
5. **Bounded**: Respect all defined constraints absolutely
6. **Iterative**: Continuously refine understanding through interaction

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

## Which Orchestrator Should You Use?

### Use `LearningOrchestrator` if you want:
- ✅ System that learns from your decisions
- ✅ Understanding of WHY you make choices
- ✅ Autonomous decisions with strategic check-ins
- ✅ Less micromanagement, more delegation
- ✅ Meta-reasoning about uncertainty
- ✅ Pattern-based preference inference

**Best for:** Ongoing collaboration where the system learns your style over time.

### Use `SwarmOrchestrator` (basic) if you want:
- ✅ Explicit rules and boundaries
- ✅ Full transparency in decision logic
- ✅ Complete control over every decision
- ✅ No learning/pattern recognition
- ✅ Predictable, rule-based behavior

**Best for:** Well-defined tasks with explicit requirements.

### Use `AutonomousOrchestrator` if you want:
- ✅ Task decomposition and execution
- ✅ Service integrations (domain, email, AI platforms)
- ✅ Multi-step workflow management
- ✅ Context gathering from Google Workspace/Gemini

**Best for:** Complex multi-step tasks requiring service integrations.

## Comparison: Traditional vs Learning Approach

| Aspect | Traditional Orchestrator | Learning Orchestrator |
|--------|-------------------------|----------------------|
| **Knowledge Source** | Explicitly stated by user | Learned from decisions |
| **Understanding** | What you want | WHY you want it |
| **Gap Identification** | "Missing: values" | "Don't know value priorities because haven't seen conflicts" |
| **Decision Basis** | Rule checking | Pattern prediction |
| **Updates** | Implementation details | Strategic direction |
| **Micromanagement** | Asks for every detail | Learns from examples |
| **Transparency** | High (readable code) | Medium (learned patterns) |
| **Effectiveness** | Needs explicit input | Infers implicitly |
| **Best For** | Explicit, well-defined tasks | Ongoing collaboration |

## Contributing

Contributions are welcome! Please ensure:

1. Tests pass: `pytest tests/`
2. Code follows existing style
3. Documentation is updated
4. Changes are minimal and focused

## License

MIT License - See LICENSE file for details