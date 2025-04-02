from typing import Optional, Dict, Any
from datetime import datetime

class User:
    """User model representing a user in the system."""
    
    def __init__(
        self,
        user_id: str,
        username: str,
        email: str,
        created_at: datetime,
        is_active: bool = True,
        full_name: Optional[str] = None,
        phone_number: Optional[str] = None,
        address: Optional[str] = None,
        additional_info: Optional[Dict[str, Any]] = None
    ):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.created_at = created_at
        self.is_active = is_active
        self.full_name = full_name
        self.phone_number = phone_number
        self.address = address
        self.additional_info = additional_info or {}
    
    @classmethod
    def from_supabase(cls, supabase_user: Dict[str, Any]) -> 'User':
        """
        Create a User instance from Supabase user data.
        
        Args:
            supabase_user: User data from Supabase
            
        Returns:
            User: A User instance
        """
        # Map Supabase user structure to our User model
        user_metadata = supabase_user.get("user_metadata", {})
        
        return cls(
            user_id=supabase_user.get("id"),
            username=user_metadata.get("username", ""),
            email=supabase_user.get("email", ""),
            created_at=datetime.fromisoformat(supabase_user.get("created_at").replace("Z", "+00:00")),
            is_active=supabase_user.get("confirmed_at") is not None,
            full_name=user_metadata.get("full_name"),
            phone_number=user_metadata.get("phone_number"),
            address=user_metadata.get("address"),
            additional_info=user_metadata.get("additional_info", {})
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert User instance to dictionary.
        
        Returns:
            Dict: User data as dictionary
        """
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
            "is_active": self.is_active,
            "full_name": self.full_name,
            "phone_number": self.phone_number,
            "address": self.address,
            "additional_info": self.additional_info
        }