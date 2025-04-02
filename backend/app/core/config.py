from typing import List, Dict, Any, Optional
from pydantic import AnyHttpUrl, validator, EmailStr
from pydantic_settings import BaseSettings
import os
from pathlib import Path
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application settings that loads from environment variables or .env file.

    This class uses Pydantic for environment variable validation and
    provides settings for different environments (dev, staging, prod).
    """

    # Base configuration
    APP_ENV: str = "dev"  # dev, stag, prod
    API_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Pet Adoption Network API"
    VERSION: str = "1.0.0"

    # CORS settings
    CORS_ORIGINS: List[AnyHttpUrl] = []

    # Database configuration
    SUPABASE_URL: str
    SUPABASE_KEY: str

    # JWT configuration
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # 1 hour

    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str) -> List[AnyHttpUrl]:
        """
        Validates and assembles CORS origins from a comma-separated string or list.

        Args:
            v: String or list of CORS origins

        Returns:
            List of validated AnyHttpUrl objects
        """
        if isinstance(v, str) and not v.startswith("["):
            return [origin.strip() for origin in v.split(",") if origin]
        elif isinstance(v, list):
            return v
        raise ValueError(
            "CORS_ORIGINS should be a comma-separated string or a list")

    class Config:
        """Pydantic configuration."""
        env_file = f".env.{os.getenv('APP_ENV', 'dev')}"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "allow"  # Allow extra fields from environment variables


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Returns:
        Settings: Application settings instance
    """
    return Settings()


# Create settings instance for direct access if needed
settings = get_settings()
