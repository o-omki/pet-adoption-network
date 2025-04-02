from supabase import create_client, Client
from fastapi import HTTPException
from typing import Optional, Dict, Any, List

from app.core.config import settings

class SupabaseClient:
    """
    A singleton client for interacting with Supabase.
    This class encapsulates all database interactions.
    """
    _instance = None
    _client: Optional[Client] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SupabaseClient, cls).__new__(cls)
            cls._instance._initialize_client()
        return cls._instance

    def _initialize_client(self):
        """Initialize the Supabase client with credentials from settings."""
        try:
            self._client = create_client(
                settings.SUPABASE_URL,
                settings.SUPABASE_KEY
            )
            print("Supabase client initialized successfully")
        except Exception as e:
            print(f"Failed to initialize Supabase client: {str(e)}")
            raise

    @property
    def client(self) -> Client:
        """Get the Supabase client instance."""
        if self._client is None:
            self._initialize_client()
        return self._client

    # User operations
    async def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a user by their ID."""
        try:
            response = self.client.table('users').select('*').eq('user_id', user_id).execute()
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Error retrieving user by ID {user_id}: {str(e)}")
            raise HTTPException(status_code=500, detail="Database error")

    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Retrieve a user by their email address."""
        try:
            response = self.client.table('users').select('*').eq('email', email).execute()
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Error retrieving user by email {email}: {str(e)}")
            raise HTTPException(status_code=500, detail="Database error")

    async def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user."""
        try:
            response = self.client.table('users').insert(user_data).execute()
            if response.data and len(response.data) > 0:
                return response.data[0]
            raise HTTPException(status_code=500, detail="Failed to create user")
        except Exception as e:
            print(f"Error creating user: {str(e)}")
            raise HTTPException(status_code=500, detail="Database error")

    # Pet operations
    async def get_pets(self, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Retrieve pets with optional filtering."""
        try:
            query = self.client.table('pets').select('*')
            
            if filters:
                for key, value in filters.items():
                    if value is not None:
                        query = query.eq(key, value)
            
            response = query.execute()
            return response.data or []
        except Exception as e:
            print(f"Error retrieving pets: {str(e)}")
            raise HTTPException(status_code=500, detail="Database error")

    async def get_pet_by_id(self, pet_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a pet by its ID."""
        try:
            response = self.client.table('pets').select('*').eq('pet_id', pet_id).execute()
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Error retrieving pet by ID {pet_id}: {str(e)}")
            raise HTTPException(status_code=500, detail="Database error")

    async def create_pet(self, pet_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new pet listing."""
        try:
            response = self.client.table('pets').insert(pet_data).execute()
            if response.data and len(response.data) > 0:
                return response.data[0]
            raise HTTPException(status_code=500, detail="Failed to create pet listing")
        except Exception as e:
            print(f"Error creating pet: {str(e)}")
            raise HTTPException(status_code=500, detail="Database error")

    async def update_pet(self, pet_id: str, pet_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing pet listing."""
        try:
            response = self.client.table('pets').update(pet_data).eq('pet_id', pet_id).execute()
            if response.data and len(response.data) > 0:
                return response.data[0]
            raise HTTPException(status_code=404, detail="Pet not found")
        except Exception as e:
            print(f"Error updating pet {pet_id}: {str(e)}")
            raise HTTPException(status_code=500, detail="Database error")

    async def delete_pet(self, pet_id: str) -> bool:
        """Delete a pet listing."""
        try:
            response = self.client.table('pets').delete().eq('pet_id', pet_id).execute()
            return True
        except Exception as e:
            print(f"Error deleting pet {pet_id}: {str(e)}")
            raise HTTPException(status_code=500, detail="Database error")

# Create a singleton instance of SupabaseClient
supabase_manager = SupabaseClient()