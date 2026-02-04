from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import List, Optional
from src.database.connection import get_session
from src.models.task import TaskCreate, TaskUpdate, TaskPatch
from src.services.task_service import TaskService
from src.schemas.task import TaskResponse, TaskCreateRequest, TaskUpdateRequest, TaskListResponse, TaskCompletionRequest, APIResponse, APIErrorResponse
from src.core.error_handlers import TaskNotFoundError
from src.core.auth import get_current_user
from src.models.user import User
from datetime import datetime

router = APIRouter()

@router.get("/tasks", response_model=TaskListResponse)
def get_tasks(
    completed: Optional[bool] = Query(None, description="Filter tasks by completion status"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of tasks to return"),
    offset: int = Query(0, ge=0, description="Number of tasks to skip"),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the authenticated user with optional filters
    """
    try:
        tasks, total = TaskService.get_tasks_by_user(
            session=session,
            user_id=current_user.id,
            completed=completed,
            limit=limit,
            offset=offset
        )

        # Convert to response format
        task_responses = []
        for task in tasks:
            task_response = TaskResponse(
                id=task.id,
                title=task.title,
                description=task.description,
                completed=task.completed,
                user_id=task.user_id,
                created_at=task.created_at,
                updated_at=task.updated_at
            )
            task_responses.append(task_response)

        return TaskListResponse(tasks=task_responses, total=total)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tasks", response_model=APIResponse)
def create_task(
    task_create: TaskCreateRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user
    """
    try:
        # Create task model from request, using the authenticated user's ID
        task_create_model = TaskCreate(
            title=task_create.title,
            description=task_create.description,
            completed=task_create.completed,
            user_id=current_user.id
        )

        created_task = TaskService.create_task(session, task_create_model)

        task_response = TaskResponse(
            id=created_task.id,
            title=created_task.title,
            description=created_task.description,
            completed=created_task.completed,
            user_id=created_task.user_id,
            created_at=created_task.created_at,
            updated_at=created_task.updated_at
        )

        return APIResponse(
            success=True,
            data={"task": task_response.dict()},
            message="Task created successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tasks/{id}", response_model=APIResponse)
def get_task(
    id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get a specific task by ID for the authenticated user
    """
    try:
        task = TaskService.get_task_by_id(session, id, current_user.id)

        task_response = TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            user_id=task.user_id,
            created_at=task.created_at,
            updated_at=task.updated_at
        )

        return APIResponse(
            success=True,
            data={"task": task_response.dict()}
        )
    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail=f"Task with id {id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/tasks/{id}", response_model=APIResponse)
def update_task(
    id: int,
    task_update: TaskUpdateRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update a specific task by ID for the authenticated user
    """
    try:
        # Create update model from request
        task_update_model = TaskUpdate(
            title=task_update.title,
            description=task_update.description,
            completed=task_update.completed
        )

        updated_task = TaskService.update_task(session, id, current_user.id, task_update_model)

        task_response = TaskResponse(
            id=updated_task.id,
            title=updated_task.title,
            description=updated_task.description,
            completed=updated_task.completed,
            user_id=updated_task.user_id,
            created_at=updated_task.created_at,
            updated_at=updated_task.updated_at
        )

        return APIResponse(
            success=True,
            data={"task": task_response.dict()},
            message="Task updated successfully"
        )
    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail=f"Task with id {id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/tasks/{id}", response_model=APIResponse)
def delete_task(
    id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a specific task by ID for the authenticated user
    """
    try:
        success = TaskService.delete_task(session, id, current_user.id)

        if success:
            return APIResponse(
                success=True,
                message="Task deleted successfully"
            )
        else:
            raise HTTPException(status_code=404, detail=f"Task with id {id} not found")
    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail=f"Task with id {id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/tasks/{id}/complete", response_model=APIResponse)
def toggle_task_completion(
    id: int,
    task_completion: TaskCompletionRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Toggle the completion status of a task for the authenticated user
    """
    try:
        updated_task = TaskService.toggle_task_completion(session, id, current_user.id, task_completion.completed)

        task_response = TaskResponse(
            id=updated_task.id,
            title=updated_task.title,
            description=updated_task.description,
            completed=updated_task.completed,
            user_id=updated_task.user_id,
            created_at=updated_task.created_at,
            updated_at=updated_task.updated_at
        )

        return APIResponse(
            success=True,
            data={"task": task_response.dict()},
            message="Task completion status updated"
        )
    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail=f"Task with id {id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health", response_model=APIResponse)
def task_health_check(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Health check endpoint to verify database connectivity for authenticated user
    """
    try:
        # Simple query to test database connectivity
        from sqlalchemy import text
        session.exec(text("SELECT 1"))

        return APIResponse(
            success=True,
            data={"database": "connected", "status": "healthy", "user_id": current_user.id},
            message="Task service and database are healthy"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")