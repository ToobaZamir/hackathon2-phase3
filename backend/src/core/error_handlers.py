from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any
import logging

# Configure logging
logger = logging.getLogger(__name__)

class TaskNotFoundError(HTTPException):
    """Raised when a task is not found"""
    def __init__(self, task_id: int):
        super().__init__(
            status_code=404,
            detail=f"Task with id {task_id} not found"
        )

class ValidationError(Exception):
    """Raised when validation fails"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class DatabaseError(Exception):
    """Raised when database operations fail"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

# Error handlers for FastAPI
async def task_not_found_handler(request: Request, exc: TaskNotFoundError):
    """Handle TaskNotFoundError"""
    logger.error(f"Task not found: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": "TASK_NOT_FOUND",
                "message": exc.detail
            }
        }
    )

async def validation_error_handler(request: Request, exc: ValidationError):
    """Handle ValidationError"""
    logger.error(f"Validation error: {str(exc)}")
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": exc.message
            }
        }
    )

async def database_error_handler(request: Request, exc: DatabaseError):
    """Handle DatabaseError"""
    logger.error(f"Database error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "Internal server error occurred"
            }
        }
    )

async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle generic HTTP exceptions"""
    logger.error(f"HTTP exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": "HTTP_ERROR",
                "message": str(exc.detail)
            }
        }
    )

async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"General exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred"
            }
        }
    )