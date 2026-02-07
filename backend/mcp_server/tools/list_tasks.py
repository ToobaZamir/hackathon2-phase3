"""MCP tool for listing tasks."""
from sqlmodel import Session, select
from typing import Optional, Dict, Any, List
from src.models.task import Task
from src.database.connection import engine


async def list_tasks(
    user_id: int,
    status: Optional[str] = "all",
    limit: Optional[int] = 50,
    offset: Optional[int] = 0
) -> Dict[str, Any]:
    """
    Retrieves tasks for the user with optional filtering.

    Args:
        user_id: ID of the user
        status: Filter by status (all/pending/completed)
        limit: Max tasks to return
        offset: Number of tasks to skip

    Returns:
        Success: {"success": True, "tasks": [...], "count": int}
        Error: {"success": False, "error": str, "message": str}
    """
    try:
        with Session(engine) as session:
            # Build query
            query = select(Task).where(Task.user_id == user_id)

            # Apply status filter
            if status == "pending":
                query = query.where(Task.completed == False)
            elif status == "completed":
                query = query.where(Task.completed == True)
            # "all" = no filter

            # Order by created_at descending (newest first)
            query = query.order_by(Task.created_at.desc())

            # Apply pagination
            query = query.offset(offset).limit(limit)

            # Execute query
            results = session.exec(query).all()

            # Format results
            tasks = [
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat()
                }
                for task in results
            ]

            return {
                "success": True,
                "tasks": tasks,
                "count": len(tasks),
                "status_filter": status
            }

    except Exception as e:
        return {
            "success": False,
            "error": "internal_error",
            "message": f"Could not retrieve tasks: {str(e)}"
        }
