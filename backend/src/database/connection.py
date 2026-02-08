"""Backward-compatible re-export.

Every module that does ``from src.database.connection import get_session``
(auth, tasks, chat, messages) keeps working.  The single source of truth
is now ``src.database.db``.
"""
from src.database.db import engine, get_session, init_db

__all__ = ["engine", "get_session", "init_db"]
