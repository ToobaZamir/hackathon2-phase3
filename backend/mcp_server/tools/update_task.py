"""MCP tool for updating tasks."""
from sqlmodel import Session, select
from typing import Optional, Dict, Any
from src.models.task import Task
from src.database.connection import engine


async def update_task(
    user_id: int,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    completed: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Updates an existing task's fields.

    Args:
        user_id: ID of the user (for authorization)
        task_id: ID of the task to update
        title: New task title (optional)
        description: New task description (optional)
        completed: New completion status (optional)

    Returns:
        Success: {"success": True, "task_id": int, "title": str, "updated_fields": [...]}
        Error: {"success": False, "error": str, "message": str}
    """
    try:
        # Validate at least one field is provided
        if title is None and description is None and completed is None:
            return {
                "success": False,
                "error": "validation_error",
                "message": "At least one field (title, description, or completed) must be provided"
            }

        # Validate title if provided
        if title is not None:
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

        # Validate description if provided
        if description is not None and len(description) > 1000:
            return {
                "success": False,
                "error": "validation_error",
                "message": "Task description must be 1000 characters or less"
            }

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

            # Update fields
            updated_fields = []

            if title is not None:
                task.title = title.strip()
                updated_fields.append("title")

            if description is not None:
                task.description = description.strip() if description else None
                updated_fields.append("description")

            if completed is not None:
                task.completed = completed
                updated_fields.append("completed")

            # Commit changes
            session.add(task)
            session.commit()
            session.refresh(task)

            return {
                "success": True,
                "task_id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "updated_fields": updated_fields,
                "updated_at": task.updated_at.isoformat()
            }

    except Exception as e:
        return {
            "success": False,
            "error": "internal_error",
            "message": f"Could not update task: {str(e)}"
        }
