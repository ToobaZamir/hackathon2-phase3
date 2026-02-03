from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    app_title: str = "Todo Backend API"
    app_description: str = "A RESTful API for managing todo tasks with persistent storage"
    app_version: str = "1.0.0"

    # Database settings
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")
    test_database_url: str = os.getenv("TEST_DATABASE_URL", "sqlite:///./test_todo_app.db")

    # Application settings
    secret_key: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # Environment settings
    environment: str = os.getenv("ENVIRONMENT", "development")
    debug: bool = os.getenv("DEBUG", "True").lower() == "true"

    class Config:
        env_file = ".env"

settings = Settings()