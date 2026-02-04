from typing import List, Optional
from sqlmodel import Session, select
from src.models.task import Task, TaskCreate, TaskUpdate, TaskPublic
from src.core.error_handlers import TaskNotFoundError, DatabaseError
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class TaskService:
    @staticmethod
    def create_task(session: Session, task_create: TaskCreate) -> TaskPublic:
        """Create a new task"""
        try:
            logger.info(f"Creating task for user {task_create.user_id}: {task_create.title}")

            # Create task instance - populate timestamps manually
            current_time = datetime.now()
            task_data = task_create.model_dump()
            task_data['created_at'] = current_time
            task_data['updated_at'] = current_time

            task = Task(**task_data)

            # Add to session and commit
            session.add(task)
            session.commit()
            session.refresh(task)

            logger.info(f"Task created successfully with ID {task.id}")

            # Convert to public schema
            task_dict = {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "user_id": task.user_id,
                "created_at": task.created_at,
                "updated_at": task.updated_at
            }
            return TaskPublic(**task_dict)
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to create task: {str(e)}")
            raise DatabaseError(f"Failed to create task: {str(e)}")

    @staticmethod
    def get_task_by_id(session: Session, task_id: int, user_id: int) -> TaskPublic:
        """Get a task by ID for a specific user"""
        try:
            logger.info(f"Retrieving task {task_id} for user {user_id}")

            # Query for the task belonging to the user
            statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            task = session.exec(statement).first()

            if not task:
                logger.warning(f"Task {task_id} not found for user {user_id}")
                raise TaskNotFoundError(task_id)

            logger.info(f"Task {task_id} retrieved successfully for user {user_id}")

            # Convert to public schema
            task_dict = {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "user_id": task.user_id,
                "created_at": task.created_at,
                "updated_at": task.updated_at
            }
            return TaskPublic(**task_dict)
        except TaskNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Failed to retrieve task {task_id}: {str(e)}")
            raise DatabaseError(f"Failed to retrieve task: {str(e)}")

    @staticmethod
    def get_tasks_by_user(
        session: Session,
        user_id: int,
        completed: Optional[bool] = None,
        limit: Optional[int] = 50,
        offset: Optional[int] = 0
    ) -> tuple[List[TaskPublic], int]:
        """Get all tasks for a user with optional filters"""
        try:
            logger.info(f"Retrieving tasks for user {user_id}, completed={completed}, limit={limit}, offset={offset}")

            # Build query with user filter
            query = select(Task).where(Task.user_id == user_id)

            # Apply completion filter if specified
            if completed is not None:
                query = query.where(Task.completed == completed)

            # Get total count
            count_query = select(Task.id).where(Task.user_id == user_id)
            if completed is not None:
                count_query = count_query.where(Task.completed == completed)
            total = len(session.exec(count_query).all())

            # Apply pagination and execute
            tasks = session.exec(query.offset(offset).limit(limit)).all()

            # Convert to public schema
            task_list = []
            for task in tasks:
                task_public = TaskPublic(**{
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "user_id": task.user_id,
                    "created_at": task.created_at,
                    "updated_at": task.updated_at
                })
                task_list.append(task_public)

            logger.info(f"Retrieved {len(task_list)} tasks for user {user_id} (total: {total})")

            return task_list, total
        except Exception as e:
            logger.error(f"Failed to retrieve tasks for user {user_id}: {str(e)}")
            raise DatabaseError(f"Failed to retrieve tasks: {str(e)}")

    @staticmethod
    def update_task(session: Session, task_id: int, user_id: int, task_update: TaskUpdate) -> TaskPublic:
        """Update a task"""
        try:
            logger.info(f"Updating task {task_id} for user {user_id}")

            # Get the existing task
            statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            task = session.exec(statement).first()

            if not task:
                logger.warning(f"Task {task_id} not found for user {user_id}")
                raise TaskNotFoundError(task_id)

            # Update only the fields that are provided
            update_data = task_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(task, field, value)

            # Update the updated_at timestamp
            task.updated_at = datetime.now()

            # Commit changes
            session.add(task)
            session.commit()
            session.refresh(task)

            logger.info(f"Task {task_id} updated successfully for user {user_id}")

            # Convert to public schema
            task_dict = {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "user_id": task.user_id,
                "created_at": task.created_at,
                "updated_at": task.updated_at
            }
            return TaskPublic(**task_dict)
        except TaskNotFoundError:
            raise
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to update task {task_id}: {str(e)}")
            raise DatabaseError(f"Failed to update task: {str(e)}")

    @staticmethod
    def delete_task(session: Session, task_id: int, user_id: int) -> bool:
        """Delete a task"""
        try:
            logger.info(f"Deleting task {task_id} for user {user_id}")

            # Get the existing task
            statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            task = session.exec(statement).first()

            if not task:
                logger.warning(f"Task {task_id} not found for user {user_id}")
                raise TaskNotFoundError(task_id)

            # Delete the task
            session.delete(task)
            session.commit()

            logger.info(f"Task {task_id} deleted successfully for user {user_id}")

            return True
        except TaskNotFoundError:
            raise
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to delete task {task_id}: {str(e)}")
            raise DatabaseError(f"Failed to delete task: {str(e)}")

    @staticmethod
    def toggle_task_completion(session: Session, task_id: int, user_id: int, completed: bool) -> TaskPublic:
        """Toggle the completion status of a task"""
        try:
            logger.info(f"Updating completion status of task {task_id} for user {user_id} to {completed}")

            # Get the existing task
            statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            task = session.exec(statement).first()

            if not task:
                logger.warning(f"Task {task_id} not found for user {user_id}")
                raise TaskNotFoundError(task_id)

            # Update the completion status
            task.completed = completed
            task.updated_at = datetime.now()

            # Commit changes
            session.add(task)
            session.commit()
            session.refresh(task)

            logger.info(f"Task {task_id} completion status updated successfully for user {user_id}")

            # Convert to public schema
            task_dict = {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "user_id": task.user_id,
                "created_at": task.created_at,
                "updated_at": task.updated_at
            }
            return TaskPublic(**task_dict)
        except TaskNotFoundError:
            raise
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to update task completion for task {task_id}: {str(e)}")
            raise DatabaseError(f"Failed to update task completion: {str(e)}")