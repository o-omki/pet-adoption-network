from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


class VisitStatus(str, Enum):
    """Enum for visit scheduling status."""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class VisitScheduleBase(BaseModel):
    """Base schema for visit schedule data with common fields."""
    pet_id: str
    scheduled_date: datetime
    message: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "pet_id": "123e4567-e89b-12d3-a456-426614174001",
                "scheduled_date": "2025-04-15T14:30:00Z",
                "message": "I'd like to meet this pet to see if we're a good match."
            }
        }


class VisitScheduleCreate(VisitScheduleBase):
    """Schema for creating a new visit schedule."""
    
    @validator('scheduled_date')
    def scheduled_date_must_be_future(cls, v):
        if v < datetime.now():
            raise ValueError('scheduled_date must be in the future')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "pet_id": "123e4567-e89b-12d3-a456-426614174001",
                "scheduled_date": "2025-04-15T14:30:00Z",
                "message": "I'd like to meet this pet to see if we're a good match."
            }
        }


class VisitScheduleUpdate(BaseModel):
    """Schema for updating an existing visit schedule."""
    status: VisitStatus
    
    class Config:
        schema_extra = {
            "example": {
                "status": "confirmed"
            }
        }


class VisitScheduleResponse(VisitScheduleBase):
    """Schema for visit schedule response data."""
    visit_id: str
    adopter_id: str
    status: VisitStatus
    created_at: datetime
    updated_at: datetime
    
    class Config:
        schema_extra = {
            "example": {
                "visit_id": "123e4567-e89b-12d3-a456-426614174002",
                "pet_id": "123e4567-e89b-12d3-a456-426614174001",
                "adopter_id": "123e4567-e89b-12d3-a456-426614174000",
                "scheduled_date": "2025-04-15T14:30:00Z",
                "message": "I'd like to meet this pet to see if we're a good match.",
                "status": "pending",
                "created_at": "2025-01-01T00:00:00Z",
                "updated_at": "2025-01-01T00:00:00Z"
            }
        }