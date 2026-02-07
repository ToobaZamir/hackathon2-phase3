"""MCP tool for deleting tasks."""
from sqlmodel import Session, select
from typing import Dict, Any
from backend.src.models.task import Task
from backend.src.database.connection import engine


async def delete_task(
    user_id: int,
    task_id: int
) -> Dict[str, Any]:
    """
    Permanently deletes a task.

    Args:
        user_id: ID of the user (for authorization)
        task_id: ID of the task to delete

    Returns:
        Success: {"success": True, "task_id": int, "title": str, "deleted": True}
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

            # Store task info before deletion
            task_title = task.title
            task_id_value = task.id

            # Delete task
            session.delete(task)
            session.commit()

            return {
                "success": True,
                "task_id": task_id_value,
                "title": task_title,
                "deleted": True
            }

    except Exception as e:
        return {
            "success": False,
            "error": "internal_error",
            "message": f"Could not delete task: {str(e)}"
        }
