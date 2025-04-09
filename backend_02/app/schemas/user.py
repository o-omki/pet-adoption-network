from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, Dict, Any
from enum import Enum
from datetime import datetime


class UserRole(str, Enum):
    """
    Enumeration of possible user roles.
    """
    ADOPTER = "adopter"
    INDIVIDUAL = "individual"
    SHELTER = "shelter"
    ADMIN = "admin"


class UserBase(BaseModel):
    """
    Base schema for user data.
    """
    username: str
    email: EmailStr


class UserCreate(UserBase):
    """
    Schema for creating a new user.
    """
    password: str
    role: UserRole
    additional_info: Optional[Dict[str, Any]] = Field(default_factory=dict)
    
    @validator("password")
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class UserLogin(BaseModel):
    """
    Schema for user login.
    """
    username: str
    password: str


class Token(BaseModel):
    """
    Schema for authentication token.
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Schema for token payload data.
    """
    user_id: Optional[str] = None


class UserInDB(UserBase):
    """
    Schema for user as stored in database.
    """
    user_id: str
    role: UserRole
    created_at: datetime

    class Config:
        orm_mode = True


class UserProfile(BaseModel):
    """
    Schema for user profile.
    """
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    additional_info: Dict[str, Any] = Field(default_factory=dict)
