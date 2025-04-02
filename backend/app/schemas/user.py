from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, Dict, Any, List
from enum import Enum
from datetime import datetime


class UserRole(str, Enum):
    """Enum for user roles in the system."""
    ADOPTER = "adopter"
    INDIVIDUAL = "individual"
    SHELTER = "shelter"
    ADMIN = "admin"


class UserBase(BaseModel):
    """Base user schema with common fields."""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    
    class Config:
        schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "john@example.com"
            }
        }


class UserCreate(UserBase):
    """Schema for user registration."""
    password: str = Field(..., min_length=8)
    role: UserRole = Field(default=UserRole.ADOPTER)
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    additional_info: Optional[Dict[str, Any]] = Field(default_factory=dict)
    
    class Config:
        schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "john@example.com",
                "password": "securepassword",
                "role": "adopter",
                "full_name": "John Doe",
                "phone_number": "+1234567890",
                "address": "123 Main St, New York, NY 10001",
                "additional_info": {
                    "bio": "Pet lover seeking a new companion"
                }
            }
        }


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str
    
    class Config:
        schema_extra = {
            "example": {
                "email": "john@example.com",
                "password": "securepassword"
            }
        }


class UserUpdate(BaseModel):
    """Schema for updating user information."""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    additional_info: Optional[Dict[str, Any]] = None
    
    class Config:
        schema_extra = {
            "example": {
                "username": "johndoe_updated",
                "full_name": "John Doe Jr.",
                "phone_number": "+1987654321",
                "address": "456 Oak St, Los Angeles, CA 90001",
                "additional_info": {
                    "bio": "Pet lover and volunteer at local shelter"
                }
            }
        }


class UserResponse(UserBase):
    """Schema for user response data."""
    user_id: str
    role: UserRole
    created_at: datetime
    is_active: bool
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    additional_info: Optional[Dict[str, Any]] = None
    
    class Config:
        schema_extra = {
            "example": {
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "username": "johndoe",
                "email": "john@example.com",
                "role": "adopter",
                "created_at": "2023-01-01T00:00:00",
                "is_active": True,
                "full_name": "John Doe",
                "phone_number": "+1234567890",
                "address": "123 Main St, New York, NY 10001",
                "additional_info": {
                    "bio": "Pet lover seeking a new companion"
                }
            }
        }


class Token(BaseModel):
    """Schema for authentication token response."""
    access_token: str
    token_type: str = "bearer"
    
    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }


class TokenData(BaseModel):
    """Schema for decoded token data."""
    user_id: Optional[str] = None
    email: Optional[str] = None
    role: Optional[UserRole] = None