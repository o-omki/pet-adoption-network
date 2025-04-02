from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


class ApplicationStatus(str, Enum):
    """Enum for adoption application status."""
    SUBMITTED = "submitted"
    APPROVED = "approved"
    REJECTED = "rejected"


class AdoptionApplicationBase(BaseModel):
    """Base schema for adoption application data with common fields."""
    pet_id: str
    message: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "pet_id": "123e4567-e89b-12d3-a456-426614174001",
                "message": "I would love to give this pet a loving home."
            }
        }


class AdoptionApplicationCreate(AdoptionApplicationBase):
    """Schema for creating a new adoption application."""
    
    class Config:
        schema_extra = {
            "example": {
                "pet_id": "123e4567-e89b-12d3-a456-426614174001",
                "message": "I would love to give this pet a loving home."
            }
        }


class AdoptionApplicationUpdate(BaseModel):
    """Schema for updating an existing adoption application."""
    status: ApplicationStatus
    
    class Config:
        schema_extra = {
            "example": {
                "status": "approved"
            }
        }


class AdoptionApplicationResponse(AdoptionApplicationBase):
    """Schema for adoption application response data."""
    application_id: str
    adopter_id: str
    status: ApplicationStatus
    submitted_at: datetime
    updated_at: datetime
    
    class Config:
        schema_extra = {
            "example": {
                "application_id": "123e4567-e89b-12d3-a456-426614174002",
                "pet_id": "123e4567-e89b-12d3-a456-426614174001",
                "adopter_id": "123e4567-e89b-12d3-a456-426614174000",
                "message": "I would love to give this pet a loving home.",
                "status": "submitted",
                "submitted_at": "2025-01-01T00:00:00",
                "updated_at": "2025-01-01T00:00:00"
            }
        }