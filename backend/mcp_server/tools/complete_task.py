"""MCP tool for completing tasks."""
from sqlmodel import Session, select
from typing import Dict, Any
from backend.src.models.task import Task
from backend.src.database.connection import engine


async def complete_task(
    user_id: int,
    task_id: int
) -> Dict[str, Any]:
    """
    Marks a task as completed.

    Args:
        user_id: ID of the user (for authorization)
        task_id: ID of the task to complete

    Returns:
        Success: {"success": True, "task_id": int, "title": str, "completed": True}
        Error: {"success": False, "error": str, "message": str}
    """
    try:
        with Session(engine) as session:
            # Find task with user authorization
            statement = select(Task).where(
                Task.id == task_id,
                Task.user_id == user_id
            )
            task = session.exec(statement).first()

            if not task:
                return {
                    "success": False,
                    "error": "not_found",
                    "message": f"Task with ID {task_id} not found or you don't have permission to access it"
                }

            # Check if already completed
            if task.completed:
                return {
                    "success": True,
                    "task_id": task.id,
                    "title": task.title,
                    "completed": True,
                    "message": "Task was already completed"
                }

            # Mark as completed
            task.completed = True
            session.add(task)
            session.commit()
            session.refresh(task)

            return {
                "success": True,
                "task_id": task.id,
                "title": task.title,
                "completed": True,
                "updated_at": task.updated_at.isoformat()
            }

    except Exception as e:
        return {
            "success": False,
            "error": "internal_error",
            "message": f"Could not complete task: {str(e)}"
        }
