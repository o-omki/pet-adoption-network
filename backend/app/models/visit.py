from enum import Enum
from typing import Optional, Dict, Any, List
from datetime import datetime


class VisitStatus(str, Enum):
    """Enum for visit scheduling status."""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class VisitSchedule:
    """Visit schedule model representing a scheduled visit in the system."""
    
    def __init__(
        self,
        visit_id: str,
        pet_id: str,
        adopter_id: str,
        scheduled_date: datetime,
        status: VisitStatus,
        created_at: datetime,
        updated_at: datetime,
        message: Optional[str] = None
    ):
        self.visit_id = visit_id
        self.pet_id = pet_id
        self.adopter_id = adopter_id
        self.scheduled_date = scheduled_date
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
        self.message = message
    
    @classmethod
    def from_supabase(cls, data: Dict[str, Any]) -> 'VisitSchedule':
        """
        Create a VisitSchedule instance from Supabase data.
        
        Args:
            data: Visit schedule data from Supabase
            
        Returns:
            VisitSchedule: A VisitSchedule instance
        """
        return cls(
            visit_id=data.get("id"),
            pet_id=data.get("pet_id"),
            adopter_id=data.get("adopter_id"),
            scheduled_date=datetime.fromisoformat(data.get("scheduled_date").replace("Z", "+00:00")),
            status=data.get("status"),
            created_at=datetime.fromisoformat(data.get("created_at").replace("Z", "+00:00")),
            updated_at=datetime.fromisoformat(data.get("updated_at").replace("Z", "+00:00")),
            message=data.get("message")
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert VisitSchedule instance to dictionary.
        
        Returns:
            Dict: Visit schedule data as dictionary
        """
        return {
            "visit_id": self.visit_id,
            "pet_id": self.pet_id,
            "adopter_id": self.adopter_id,
            "scheduled_date": self.scheduled_date.isoformat(),
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "message": self.message
        }