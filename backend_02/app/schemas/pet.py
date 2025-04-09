from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, List
from enum import Enum
from datetime import datetime


class PetStatus(str, Enum):
    """
    Enumeration of possible pet adoption statuses.
    """
    AVAILABLE = "available"
    PENDING = "pending"
    ADOPTED = "adopted"


class OwnerType(str, Enum):
    """
    Enumeration of possible pet owner types.
    """
    SHELTER = "shelter"
    INDIVIDUAL = "individual"


class PetBase(BaseModel):
    """
    Base schema for pet data.
    """
    name: str
    pet_type_id: str
    breed_id: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None


class PetCreate(PetBase):
    """
    Schema for creating a new pet listing.
    """
    owner_type: OwnerType
    
    @validator("age")
    def validate_age(cls, v):
        if v is not None and v < 0:
            raise ValueError("Age cannot be negative")
        return v


class PetUpdate(BaseModel):
    """
    Schema for updating a pet listing.
    """
    name: Optional[str] = None
    pet_type_id: Optional[str] = None
    breed_id: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    status: Optional[PetStatus] = None

    @validator("age")
    def validate_age(cls, v):
        if v is not None and v < 0:
            raise ValueError("Age cannot be negative")
        return v


class PetInDB(PetBase):
    """
    Schema for pet as stored in database.
    """
    pet_id: str
    owner_id: str
    owner_type: OwnerType
    status: PetStatus
    created_at: datetime

    class Config:
        orm_mode = True


class PetResponse(PetInDB):
    """
    Schema for pet response including additional data.
    """
    pet_type_name: Optional[str] = None
    breed_name: Optional[str] = None
    owner_name: Optional[str] = None
    
    class Config:
        orm_mode = True


class PetFilter(BaseModel):
    """
    Schema for filtering pets.
    """
    pet_type_id: Optional[str] = None
    breed_id: Optional[str] = None
    status: Optional[PetStatus] = None
    age_min: Optional[int] = None
    age_max: Optional[int] = None
    gender: Optional[str] = None
    owner_id: Optional[str] = None
