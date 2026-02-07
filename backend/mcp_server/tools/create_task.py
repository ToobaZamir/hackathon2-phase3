"""MCP tool for creating tasks."""
from sqlmodel import Session
from typing import Optional, Dict, Any
from src.models.task import Task
from src.database.connection import engine


async def create_task(
    user_id: int,
    title: str,
    description: Optional[str] = None
) -> Dict[str, Any]:
    """
    Creates a new task for the user.

    Args:
        user_id: ID of the user creating the task
        title: Task title (1-255 chars)
        description: Optional task description

    Returns:
        Success: {"success": True, "task_id": int, "title": str, "created_at": str}
        Error: {"success": False, "error": str, "message": str}
    """
    try:
        # Validate inputs
        if not title or len(title.strip()) == 0:
            return {
                "success": False,
                "error": "validation_error",
                "message": "Task title cannot be empty"
            }

        if len(title) > 255:
            return {
                "success": False,
                "error": "validation_error",
                "message": "Task title must be 255 characters or less"
            }

        if description and len(description) > 1000:
            return {
                "success": False,
                "error": "validation_error",
                "message": "Task description must be 1000 characters or less"
            }

        # Create task
        with Session(engine) as session:
            task = Task(
                user_id=user_id,
                title=title.strip(),
                description=description.strip() if description else None,
                completed=False
            )
            session.add(task)
            session.commit()
            session.refresh(task)

            return {
                "success": True,
                "task_id": task.id,
                "title": task.title,
                "created_at": task.created_at.isoformat()
            }

    except Exception as e:
        return {
            "success": False,
            "error": "internal_error",
            "message": f"Could not create task: {str(e)}"
        }
