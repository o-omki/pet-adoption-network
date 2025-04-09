from typing import Dict, List, Optional, Any

from app.core.database import supabase_client
from app.core.auth import get_password_hash
from app.schemas.user import UserCreate, UserRole


class UserService:
    """
    Service for handling user-related database operations.
    """
    @staticmethod
    async def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a user by username.
        """
        result = supabase_client.table("users").select("*").eq("username", username).execute()
        if result.data:
            return result.data[0]
        return None
    @staticmethod
    async def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a user by email.
        """
        result = supabase_client.table("users").select("*").eq("email", email).execute()
        if result.data:
            return result.data[0]
        return None
    @staticmethod
    async def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a user by ID.
        """
        result = supabase_client.table("users").select("*").eq("user_id", user_id).execute()
        if result.data:
            return result.data[0]
        return None
    
    @staticmethod
    async def create_user(user: UserCreate) -> Dict[str, Any]:
        """
        Create a new user.
        
        Args:
            user: User data for creation.
            
        Returns:
            The created user data.
        """
        # Hash the password
        hashed_password = get_password_hash(user.password)
        
        # Create user in database
        user_data = {
            "username": user.username,
            "email": user.email,
            "password": hashed_password,
            "role": user.role
        }
        
        result = supabase_client.table("users").insert(user_data).execute()
        
        if not result.data:
            raise ValueError("Failed to create user")
        
        created_user = result.data[0]
        
        # Create user profile
        profile_data = {
            "user_id": created_user["user_id"],
            "additional_info": user.additional_info if user.additional_info else {}
        }
        
        profile_result = supabase_client.table("user_profiles").insert(profile_data).execute()
        
        return created_user
    
    @staticmethod
    async def get_user_profile(user_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a user's profile.
        """
        result = supabase_client.table("user_profiles").select("*").eq("user_id", user_id).execute()
        if result.data:
            return result.data[0]
        return None
    
    @staticmethod
    async def update_user_profile(user_id: str, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a user's profile.
        
        Args:
            user_id: ID of the user whose profile to update.
            profile_data: Profile data to update.
            
        Returns:
            The updated profile data.
        """
        # Check if profile exists
        profile = await UserService.get_user_profile(user_id)
        
        if profile:
            # Update existing profile
            result = supabase_client.table("user_profiles").update(profile_data).eq("user_id", user_id).execute()
        else:
            # Create new profile
            profile_data["user_id"] = user_id
            result = supabase_client.table("user_profiles").insert(profile_data).execute()
        
        if not result.data:
            raise ValueError("Failed to update user profile")
        
        return result.data[0]
