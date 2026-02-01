"""
Enhanced Autonomous Orchestrator with task execution capabilities
"""

from typing import Dict, Any, List, Optional
from .orchestrator import SwarmOrchestrator
from .executor import TaskExecutor, Task
from .context import ContextAggregator, GoogleWorkspaceContextProvider, GeminiContextProvider
from .services import ServiceRegistry, DomainRegistrar, EmailProvider, AIPlatformResearcher
from .models import Boundary, BoundaryType, ConfidenceLevel


class AutonomousOrchestrator(SwarmOrchestrator):
    """
    Enhanced orchestrator with autonomous execution capabilities
    
    Extends SwarmOrchestrator to add:
    - Context gathering from multiple sources
    - Service integrations for real-world actions
    - Task decomposition and execution
    - Autonomous workflow management
    """
    
    def __init__(self):
        super().__init__()
        self.task_executor = TaskExecutor()
        self.context_aggregator = ContextAggregator()
        self.service_registry = ServiceRegistry()
        self._setup_default_services()
    
    def _setup_default_services(self):
        """Set up default service integrations"""
        # Register domain registrar
        self.service_registry.register_service(
            "domain_registrar",
            DomainRegistrar()
        )
        
        # Register email provider
        self.service_registry.register_service(
            "email_provider",
            EmailProvider()
        )
    
    def setup_context_providers(
        self,
        google_credentials: Optional[str] = None,
        gemini_api_key: Optional[str] = None
    ):
        """Set up context providers for gathering user information"""
        if google_credentials:
            google_provider = GoogleWorkspaceContextProvider(google_credentials)
            self.context_aggregator.add_provider("google_workspace", google_provider)
        
        if gemini_api_key:
            gemini_provider = GeminiContextProvider(gemini_api_key)
            self.context_aggregator.add_provider("gemini", gemini_provider)
    
    def gather_user_context(self, user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Gather comprehensive user context from all sources
        
        This builds the holistic understanding of user's goals, values, and intent
        """
        context = self.context_aggregator.gather_all_context(user_id)
        
        # Extract and update user framework
        goals = self.context_aggregator.extract_goals_from_context(context)
        values = self.context_aggregator.extract_values_from_context(context)
        
        if goals or values:
            self.update_user_framework(goals=goals, values=values)
        
        return context
    
    def decompose_request(self, request: str) -> List[Task]:
        """
        Decompose a high-level request into executable tasks
        
        This is the key to autonomous execution - breaking down complex
        requests into manageable steps.
        """
        tasks = []
        request_lower = request.lower()
        
        # Example decomposition for domain + email setup
        if "domain" in request_lower and "email" in request_lower:
            # Task 1: Research and purchase domain
            domain_task = self.task_executor.create_task(
                name="Acquire Domain",
                description="Research and purchase suitable domain",
                action="acquire_domain",
                parameters={
                    "requirements": self._extract_domain_requirements(request),
                    "max_cost": self._extract_budget_limit(request, "domain")
                }
            )
            
            # Task 2: Set up email account
            email_task = self.task_executor.create_task(
                name="Setup Email",
                description="Create work email account with purchased domain",
                action="setup_email",
                parameters={
                    "domain": "{{domain_from_previous_task}}",
                    "duration_years": 1
                }
            )
            
            # Email task depends on domain task
            domain_task.add_subtask(email_task)
            tasks.append(domain_task)
        
        # Example decomposition for AI platform research
        if "ai" in request_lower and "platform" in request_lower:
            ai_requirements = self._extract_ai_requirements(request)
            # Add max cost from budget extraction
            ai_requirements["max_monthly_cost"] = self._extract_budget_limit(request, "platform")
            
            ai_task = self.task_executor.create_task(
                name="Research AI Platform",
                description="Research and select best AI development platform",
                action="research_ai_platform",
                parameters={
                    "requirements": ai_requirements,
                    "max_monthly_cost": ai_requirements["max_monthly_cost"]
                }
            )
            tasks.append(ai_task)
        
        return tasks
    
    def _extract_domain_requirements(self, request: str) -> Dict[str, Any]:
        """Extract domain requirements from request"""
        # In production, use NLP to extract requirements
        return {
            "keywords": [],  # Would extract from user context
            "concepts": [],  # Would extract from Google Docs/Drive
            "min_duration_years": 1
        }
    
    def _extract_ai_requirements(self, request: str) -> Dict[str, Any]:
        """Extract AI platform requirements from request"""
        requirements = {
            "required_features": [],
            "security_level": "high",
            "encryption_required": False,
            "max_monthly_cost": 100.0  # Default
        }
        
        # Parse from request
        request_lower = request.lower()
        if "encrypt" in request_lower or "end-to-end" in request_lower or "end to end" in request_lower:
            requirements["encryption_required"] = True
        
        if "security" in request_lower:
            requirements["required_features"].append("advanced_security")
        
        if "agentic" in request_lower:
            requirements["required_features"].append("agentic_ai")
        
        return requirements
    
    def _extract_budget_limit(self, request: str, category: str) -> float:
        """Extract budget limit from request"""
        # Simple regex-based extraction (in production, use NLP)
        import re
        
        # Look for dollar amounts
        amounts = re.findall(r'\$(\d+(?:\.\d{2})?)', request)
        
        if category == "domain":
            # First budget limit mentioned
            return float(amounts[0]) if amounts else 15.0
        elif category == "platform":
            # Second budget limit or default
            return float(amounts[1]) if len(amounts) > 1 else 50.0
        
        return 100.0
    
    def process_autonomous_request(self, request: str) -> Dict[str, Any]:
        """
        Main entry point for autonomous request processing
        
        This orchestrates the complete workflow:
        1. Gather context
        2. Identify knowledge gaps
        3. Ask clarifying questions if needed
        4. Decompose into tasks
        5. Check boundaries for each task
        6. Execute tasks autonomously
        7. Return results with confidence scores
        """
        workflow = {
            "request": request,
            "status": "processing",
            "steps": []
        }
        
        # Step 1: Gather context
        workflow["steps"].append("Gathering user context...")
        context = self.gather_user_context()
        
        # Step 2: Identify knowledge gaps
        workflow["steps"].append("Identifying knowledge gaps...")
        gaps = self.identify_knowledge_gaps(request)
        
        # Step 3: Check if clarification needed
        critical_gaps = [g for g in gaps if g.required_for_action]
        
        if critical_gaps:
            workflow["status"] = "needs_clarification"
            workflow["gaps"] = [g.dict() for g in critical_gaps]
            workflow["questions"] = [
                q.dict() for q in self.generate_clarification_questions(critical_gaps)
            ]
            workflow["message"] = (
                "I need to understand your goals, values, and intent better "
                "before I can confidently act on your behalf."
            )
            return workflow
        
        # Step 4: Decompose into tasks
        workflow["steps"].append("Decomposing request into tasks...")
        tasks = self.decompose_request(request)
        
        # Step 5: Validate tasks against boundaries
        workflow["steps"].append("Checking boundaries for each task...")
        validated_tasks = []
        all_violations = []
        
        for task in tasks:
            # Check if task respects boundaries
            # Extract estimated cost more carefully
            params = task.parameters
            estimated_cost = params.get("max_cost", params.get("max_monthly_cost", 0))
            
            # Determine category based on action
            category = ""
            if "domain" in task.action:
                category = "domain"
            elif "email" in task.action:
                category = "email"
            elif "ai" in task.action or "platform" in task.action:
                category = "platform"
            
            action_details = {
                "cost": estimated_cost,
                "duration": params.get("duration", 0),
                "scope": task.action,
                "category": category
            }
            
            within_boundaries, violations = self.check_boundaries(
                task.action,
                action_details
            )
            
            if within_boundaries:
                validated_tasks.append(task)
            else:
                all_violations.extend(violations)
        
        # Only fail if there are actual violations
        if all_violations:
            workflow["boundary_violations"] = all_violations
            workflow["status"] = "boundary_violation"
            return workflow
        
        # Step 6: Check if we can act confidently
        if not self.can_act_confidently():
            workflow["status"] = "low_confidence"
            workflow["message"] = (
                "I don't have enough information about your preferences to act "
                "confidently. Please provide more context about your goals and values."
            )
            return workflow
        
        # Step 7: Add tasks to executor
        workflow["steps"].append(f"Preparing to execute {len(validated_tasks)} tasks...")
        for task in validated_tasks:
            self.task_executor.add_task(task)
        
        # Step 8: Execute tasks (in simulation mode)
        workflow["steps"].append("Executing tasks (simulation mode)...")
        execution_results = self._simulate_execution(validated_tasks)
        
        workflow["status"] = "completed"
        workflow["execution_results"] = execution_results
        workflow["confidence"] = "high" if self.can_act_confidently() else "medium"
        
        return workflow
    
    def _simulate_execution(self, tasks: List[Task]) -> Dict[str, Any]:
        """
        Simulate task execution (placeholder for real execution)
        
        In production, this would actually execute the tasks.
        For safety, this simulation shows what WOULD happen.
        """
        results = {
            "total_tasks": len(tasks),
            "simulation_mode": True,
            "tasks": []
        }
        
        for task in tasks:
            task_result = {
                "name": task.name,
                "description": task.description,
                "action": task.action,
                "parameters": task.parameters,
                "would_execute": True,
                "estimated_outcome": self._estimate_task_outcome(task)
            }
            results["tasks"].append(task_result)
        
        return results
    
    def _estimate_task_outcome(self, task: Task) -> Dict[str, Any]:
        """Estimate what would happen if task were executed"""
        if task.action == "acquire_domain":
            return {
                "action": "Search and purchase domain",
                "steps": [
                    "Research available domains matching your project concepts",
                    "Filter by budget constraint",
                    "Select best match",
                    "Purchase for minimum 1 year"
                ],
                "estimated_cost": task.parameters.get("max_cost", 15.0),
                "note": "Actual execution requires payment method configuration"
            }
        
        elif task.action == "setup_email":
            return {
                "action": "Create work email account",
                "steps": [
                    "Configure DNS for domain",
                    "Create email account",
                    "Set up forwarding and security"
                ],
                "estimated_cost": 6.0,  # Per month typically
                "note": "Requires domain ownership verification"
            }
        
        elif task.action == "research_ai_platform":
            researcher = self.service_registry.ai_researcher
            platforms = researcher.research_platforms(task.parameters.get("requirements", {}))
            
            return {
                "action": "Research and select AI platform",
                "top_matches": platforms[:3] if platforms else [],
                "recommendation": platforms[0]["name"] if platforms else "No match found",
                "note": "Review recommendations before account creation"
            }
        
        return {"status": "unknown_task"}
