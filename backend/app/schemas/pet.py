from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


class PetStatus(str, Enum):
    """Enum for pet adoption status."""
    AVAILABLE = "available"
    PENDING = "pending"
    ADOPTED = "adopted"


class PetBase(BaseModel):
    """Base schema for pet data with common fields."""
    name: str = Field(..., min_length=1, max_length=100)
    pet_type_id: int
    breed_id: int
    age: Optional[int] = None
    gender: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Max",
                "pet_type_id": 1,  # Dog
                "breed_id": 1,     # Labrador Retriever
                "age": 3,
                "gender": "Male",
                "description": "Friendly, energetic Labrador who loves to play fetch.",
                "image_url": "https://example.com/images/max.jpg"
            }
        }


class PetCreate(PetBase):
    """Schema for creating a new pet listing."""
    status: PetStatus = Field(default=PetStatus.AVAILABLE)
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Max",
                "pet_type_id": 1,
                "breed_id": 1,
                "age": 3,
                "gender": "Male",
                "description": "Friendly, energetic Labrador who loves to play fetch.",
                "image_url": "https://example.com/images/max.jpg",
                "status": "available"
            }
        }


class PetUpdate(BaseModel):
    """Schema for updating an existing pet listing."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    pet_type_id: Optional[int] = None
    breed_id: Optional[int] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    status: Optional[PetStatus] = None
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Max Jr.",
                "description": "Updated description for Max.",
                "status": "pending"
            }
        }


class PetResponse(PetBase):
    """Schema for pet response data."""
    pet_id: str
    owner_id: str
    status: PetStatus
    created_at: datetime
    updated_at: datetime
    
    class Config:
        schema_extra = {
            "example": {
                "pet_id": "123e4567-e89b-12d3-a456-426614174001",
                "name": "Max",
                "owner_id": "123e4567-e89b-12d3-a456-426614174000",
                "pet_type_id": 1,
                "breed_id": 1,
                "age": 3,
                "gender": "Male",
                "description": "Friendly, energetic Labrador who loves to play fetch.",
                "image_url": "https://example.com/images/max.jpg",
                "status": "available",
                "created_at": "2025-01-01T00:00:00",
                "updated_at": "2025-01-01T00:00:00"
            }
        }