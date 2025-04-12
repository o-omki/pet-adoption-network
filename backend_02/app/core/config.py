import os
from typing import Any, Dict, Optional

from pydantic import PostgresDsn, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Pet Adoption API"
    PROJECT_VERSION: str = "1.0.0"
    
    API_PREFIX: str = "/api/v1"
    
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Supabase configuration
    SUPABASE_URL: str
    SUPABASE_KEY: str
    
    class Config:
        # env_file = ".env"  # Uncomment this line to load environment variables from a .env file during local deployment
        case_sensitive = True


settings = Settings()
