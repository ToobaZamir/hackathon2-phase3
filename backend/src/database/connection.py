from sqlmodel import create_engine, Session
from sqlalchemy import event
from sqlalchemy.pool import QueuePool
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

# Create engine with connection pooling settings optimized for persistent storage
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,  # Increased pool size for better persistence
    max_overflow=20,
    pool_pre_ping=True,  # Verify connections before use for persistence
    pool_recycle=3600,   # Recycle connections every hour to maintain freshness
    pool_timeout=30,
    echo=False,  # Set to True for SQL query logging during development
    connect_args={
        "connect_timeout": 20,  # Timeout for establishing connections
    }
)

def get_session():
    """Get database session"""
    with Session(engine) as session:
        yield session

# Optional: Add connection event listeners for monitoring
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Set SQLite pragmas for better performance (only for SQLite)"""
    if 'sqlite' in str(engine.url):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()