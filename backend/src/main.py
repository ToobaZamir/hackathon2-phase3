from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
import logging


from src.api.v1 import tasks, auth, chat
from src.core.config import settings
from src.database.connection import engine
from src.core.error_handlers import (
    task_not_found_handler,
    validation_error_handler,
    database_error_handler,
    general_exception_handler,
    TaskNotFoundError,
    ValidationError,
    DatabaseError,
)

# ---------------- LOGGING ----------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------- LIFESPAN ----------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application starting up...")
    # Note: Database tables are created via Alembic migrations
    # Run: alembic upgrade head
    logger.info("Application ready")
    yield
    logger.info("Shutting down...")

# ---------------- APP ----------------
app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    version=settings.app_version,
    lifespan=lifespan,
)

# ---------------- MIDDLEWARE ----------------
# CORS configuration to allow frontend access
app.add_middleware (
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"],
)

# ---------------- ERROR HANDLERS ----------------
app.add_exception_handler(TaskNotFoundError, task_not_found_handler)
app.add_exception_handler(ValidationError, validation_error_handler)
app.add_exception_handler(DatabaseError, database_error_handler)
app.add_exception_handler(500, general_exception_handler)

# ---------------- ROUTES ----------------
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(tasks.router, prefix="/api/todos", tags=["tasks"])
app.include_router(chat.router, prefix="/api", tags=["chat"])  # Phase 3: Conversational interface

# ---------------- ROOT ----------------
@app.get("/")
def read_root():
    return {"message": "Todo Backend API", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
