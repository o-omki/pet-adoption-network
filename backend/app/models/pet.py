from enum import Enum
from typing import Optional, Dict, Any, List
from datetime import datetime


class PetStatus(str, Enum):
    """Enum for pet adoption status."""
    AVAILABLE = "available"
    PENDING = "pending"
    ADOPTED = "adopted"


class Pet:
    """Pet model representing a pet listing in the system."""
    
    def __init__(
        self,
        pet_id: str,
        name: str,
        owner_id: str,
        pet_type_id: int,
        breed_id: int,
        status: PetStatus,
        created_at: datetime,
        updated_at: datetime,
        age: Optional[int] = None,
        gender: Optional[str] = None,
        description: Optional[str] = None,
        image_url: Optional[str] = None
    ):
        self.pet_id = pet_id
        self.name = name
        self.owner_id = owner_id
        self.pet_type_id = pet_type_id
        self.breed_id = breed_id
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
        self.age = age
        self.gender = gender
        self.description = description
        self.image_url = image_url
    
    @classmethod
    def from_supabase(cls, data: Dict[str, Any]) -> 'Pet':
        """
        Create a Pet instance from Supabase data.
        
        Args:
            data: Pet data from Supabase
            
        Returns:
            Pet: A Pet instance
        """
        return cls(
            pet_id=data.get("id"),
            name=data.get("name"),
            owner_id=data.get("owner_id"),
            pet_type_id=data.get("pet_type_id"),
            breed_id=data.get("breed_id"),
            status=data.get("status"),
            created_at=datetime.fromisoformat(data.get("created_at").replace("Z", "+00:00")),
            updated_at=datetime.fromisoformat(data.get("updated_at").replace("Z", "+00:00")),
            age=data.get("age"),
            gender=data.get("gender"),
            description=data.get("description"),
            image_url=data.get("image_url")
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert Pet instance to dictionary.
        
        Returns:
            Dict: Pet data as dictionary
        """
        return {
            "pet_id": self.pet_id,
            "name": self.name,
            "owner_id": self.owner_id,
            "pet_type_id": self.pet_type_id,
            "breed_id": self.breed_id,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "age": self.age,
            "gender": self.gender,
            "description": self.description,
            "image_url": self.image_url
        }