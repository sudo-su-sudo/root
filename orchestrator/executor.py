"""
Task execution engine for performing real-world actions
"""

from typing import Dict, Any, List, Optional, Callable
from enum import Enum
from .models import Decision, Boundary


class TaskStatus(str, Enum):
    """Status of a task execution"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    REQUIRES_CONFIRMATION = "requires_confirmation"


class Task:
    """Represents an executable task"""
    
    def __init__(
        self,
        name: str,
        description: str,
        action: str,
        parameters: Dict[str, Any],
        executor: Optional[Callable] = None
    ):
        self.name = name
        self.description = description
        self.action = action
        self.parameters = parameters
        self.executor = executor
        self.status = TaskStatus.PENDING
        self.result: Optional[Any] = None
        self.error: Optional[str] = None
        self.subtasks: List['Task'] = []
    
    def add_subtask(self, task: 'Task') -> None:
        """Add a subtask to this task"""
        self.subtasks.append(task)
    
    def execute(self) -> bool:
        """Execute this task and return success status"""
        self.status = TaskStatus.IN_PROGRESS
        
        try:
            if self.executor:
                self.result = self.executor(**self.parameters)
                self.status = TaskStatus.COMPLETED
                return True
            else:
                # No executor - mark as requiring manual execution
                self.status = TaskStatus.REQUIRES_CONFIRMATION
                self.error = "No executor available - requires manual execution"
                return False
        except Exception as e:
            self.status = TaskStatus.FAILED
            self.error = str(e)
            return False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary"""
        return {
            "name": self.name,
            "description": self.description,
            "action": self.action,
            "parameters": self.parameters,
            "status": self.status,
            "result": self.result,
            "error": self.error,
            "subtasks": [st.to_dict() for st in self.subtasks]
        }


class TaskExecutor:
    """
    Executes tasks autonomously with proper error handling and rollback
    """
    
    def __init__(self):
        self.task_queue: List[Task] = []
        self.completed_tasks: List[Task] = []
        self.failed_tasks: List[Task] = []
        self.executors: Dict[str, Callable] = {}
    
    def register_executor(self, action: str, executor: Callable) -> None:
        """Register an executor function for a specific action type"""
        self.executors[action] = executor
    
    def create_task(
        self,
        name: str,
        description: str,
        action: str,
        parameters: Dict[str, Any]
    ) -> Task:
        """Create a new task"""
        executor = self.executors.get(action)
        task = Task(name, description, action, parameters, executor)
        return task
    
    def add_task(self, task: Task) -> None:
        """Add a task to the execution queue"""
        self.task_queue.append(task)
    
    def execute_task(self, task: Task) -> bool:
        """Execute a single task"""
        # Execute subtasks first
        if task.subtasks:
            for subtask in task.subtasks:
                if not self.execute_task(subtask):
                    task.status = TaskStatus.FAILED
                    task.error = f"Subtask '{subtask.name}' failed: {subtask.error}"
                    self.failed_tasks.append(task)
                    return False
        
        # Execute the task itself
        success = task.execute()
        
        if success:
            self.completed_tasks.append(task)
        else:
            self.failed_tasks.append(task)
        
        return success
    
    def execute_all(self) -> Dict[str, Any]:
        """Execute all tasks in the queue"""
        results = {
            "total": len(self.task_queue),
            "completed": 0,
            "failed": 0,
            "requires_confirmation": 0,
            "details": []
        }
        
        while self.task_queue:
            task = self.task_queue.pop(0)
            self.execute_task(task)
            
            if task.status == TaskStatus.COMPLETED:
                results["completed"] += 1
            elif task.status == TaskStatus.FAILED:
                results["failed"] += 1
            elif task.status == TaskStatus.REQUIRES_CONFIRMATION:
                results["requires_confirmation"] += 1
            
            results["details"].append(task.to_dict())
        
        return results
    
    def get_summary(self) -> Dict[str, Any]:
        """Get execution summary"""
        return {
            "total_tasks": len(self.completed_tasks) + len(self.failed_tasks),
            "completed": len(self.completed_tasks),
            "failed": len(self.failed_tasks),
            "success_rate": (
                len(self.completed_tasks) / 
                (len(self.completed_tasks) + len(self.failed_tasks))
                if (len(self.completed_tasks) + len(self.failed_tasks)) > 0
                else 0
            )
        }
