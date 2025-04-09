from pydantic import BaseModel
from typing import Optional
from enum import Enum
from datetime import datetime


class AdoptionStatus(str, Enum):
    """
    Enumeration of possible adoption application statuses.
    """
    SUBMITTED = "submitted"
    APPROVED = "approved"
    REJECTED = "rejected"


class AdoptionApplicationBase(BaseModel):
    """
    Base schema for adoption application data.
    """
    pet_id: str
    message: Optional[str] = None


class AdoptionApplicationCreate(AdoptionApplicationBase):
    """
    Schema for creating a new adoption application.
    """
    pass


class AdoptionApplicationUpdate(BaseModel):
    """
    Schema for updating an adoption application status.
    """
    status: AdoptionStatus


class AdoptionApplicationInDB(AdoptionApplicationBase):
    """
    Schema for adoption application as stored in database.
    """
    application_id: str
    adopter_id: str
    status: AdoptionStatus
    submitted_at: datetime

    class Config:
        orm_mode = True


class AdoptionApplicationResponse(AdoptionApplicationInDB):
    """
    Schema for adoption application response with additional data.
    """
    pet_name: Optional[str] = None
    adopter_name: Optional[str] = None
    
    class Config:
        orm_mode = True
