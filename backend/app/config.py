import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://notes_user:notes_password@localhost:5432/notes_db"
    
    # API
    api_title: str = "Notes API"
    api_version: str = "1.0.0"
    api_description: str = "API for managing notes with categories"
    
    # CORS
    allowed_origins: list[str] = ["http://localhost:8501", "http://localhost:3000"]
    
    # Environment
    environment: str = "development"
    debug: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Create global settings instance
settings = Settings()