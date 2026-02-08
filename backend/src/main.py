import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# ── database (must be imported before models) ────────────────
from src.database.db import init_db                          # noqa: E402

# ── import every table model so SQLModel.metadata knows them ─
from src.models.user import User                             # noqa: F401
from src.models.conversation import Conversation             # noqa: F401
from src.models.message import Message                       # noqa: F401
from src.models.task import Task                             # noqa: F401

# ── routers ──────────────────────────────────────────────────
from src.api.v1 import auth, tasks, chat, conversations, messages

# ── config & error handlers ──────────────────────────────────
from src.core.config import settings
from src.core.error_handlers import (
    TaskNotFoundError,
    ValidationError,
    DatabaseError,
    task_not_found_handler,
    validation_error_handler,
    database_error_handler,
    general_exception_handler,
)

# ── logging ──────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ── lifespan ─────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Creating database tables …")
    init_db()
    logger.info("Application ready")
    yield
    logger.info("Shutting down …")


# ── app ──────────────────────────────────────────────────────
app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    version=settings.app_version,
    lifespan=lifespan,
)


# ── middleware ───────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"],
)


# ── error handlers ───────────────────────────────────────────
app.add_exception_handler(TaskNotFoundError, task_not_found_handler)
app.add_exception_handler(ValidationError, validation_error_handler)
app.add_exception_handler(DatabaseError, database_error_handler)
app.add_exception_handler(500, general_exception_handler)


# ── routers ──────────────────────────────────────────────────
# Auth / User
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])

# Conversations
app.include_router(conversations.router, prefix="/api", tags=["conversations"])

# Messages
app.include_router(messages.router, prefix="/api", tags=["messages"])

# Chat (AI chatbot endpoint)
app.include_router(chat.router, prefix="/api", tags=["chat"])

# Tasks (CRUD)
app.include_router(tasks.router, prefix="/api/todos", tags=["tasks"])


# ── health ───────────────────────────────────────────────────
@app.get("/")
def read_root():
    return {"message": "Todo Chatbot API", "status": "running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# ── entry-point ──────────────────────────────────────────────
if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
