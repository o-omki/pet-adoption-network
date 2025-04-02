from enum import Enum
from typing import Optional, Dict, Any, List
from datetime import datetime


class ApplicationStatus(str, Enum):
    """Enum for adoption application status."""
    SUBMITTED = "submitted"
    APPROVED = "approved"
    REJECTED = "rejected"


class AdoptionApplication:
    """Adoption application model representing an adoption request in the system."""
    
    def __init__(
        self,
        application_id: str,
        pet_id: str,
        adopter_id: str,
        status: ApplicationStatus,
        submitted_at: datetime,
        updated_at: datetime,
        message: Optional[str] = None
    ):
        self.application_id = application_id
        self.pet_id = pet_id
        self.adopter_id = adopter_id
        self.status = status
        self.submitted_at = submitted_at
        self.updated_at = updated_at
        self.message = message
    
    @classmethod
    def from_supabase(cls, data: Dict[str, Any]) -> 'AdoptionApplication':
        """
        Create an AdoptionApplication instance from Supabase data.
        
        Args:
            data: Application data from Supabase
            
        Returns:
            AdoptionApplication: An AdoptionApplication instance
        """
        return cls(
            application_id=data.get("id"),
            pet_id=data.get("pet_id"),
            adopter_id=data.get("adopter_id"),
            status=data.get("status"),
            submitted_at=datetime.fromisoformat(data.get("submitted_at").replace("Z", "+00:00")),
            updated_at=datetime.fromisoformat(data.get("updated_at").replace("Z", "+00:00")),
            message=data.get("message")
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert AdoptionApplication instance to dictionary.
        
        Returns:
            Dict: Application data as dictionary
        """
        return {
            "application_id": self.application_id,
            "pet_id": self.pet_id,
            "adopter_id": self.adopter_id,
            "status": self.status,
            "submitted_at": self.submitted_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "message": self.message
        }