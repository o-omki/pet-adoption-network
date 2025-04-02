from typing import Dict, List, Optional, Any
from app.db.supabase_client import supabase_manager
from app.models.pet import Pet, PetStatus
from app.schemas.pet import PetCreate, PetUpdate


class PetService:
    """Service for handling pet-related operations."""
    
    @staticmethod
    async def create_pet(owner_id: str, pet_data: PetCreate) -> Pet:
        """
        Create a new pet listing.
        
        Args:
            owner_id: ID of the user creating the pet listing
            pet_data: Pet data to be created
            
        Returns:
            Pet: The newly created pet
            
        Raises:
            ValueError: If creation fails
        """
        try:
            # Prepare data for insertion
            pet_dict = pet_data.dict()
            pet_dict["owner_id"] = owner_id
            
            # Insert data into Supabase
            client = supabase_manager.get_client()
            response = client.table("pets").insert(pet_dict).execute()
            
            # Check if insertion was successful
            if not response.data or len(response.data) == 0:
                raise ValueError("Failed to create pet")
            
            # Return created pet
            pet = Pet.from_supabase(response.data[0])
            
            return pet
            
        except Exception as e:
            raise
    
    @staticmethod
    async def get_pets(filters: Optional[Dict[str, Any]] = None, limit: int = 100, offset: int = 0) -> List[Pet]:
        """
        Get a list of pets with optional filtering.
        
        Args:
            filters: Optional filters to apply
            limit: Maximum number of pets to return
            offset: Offset for pagination
            
        Returns:
            List[Pet]: List of pets matching the filters
        """
        try:
            client = supabase_manager.get_client()
            query = client.table("pets").select("*")
            
            # Apply filters if provided
            if filters:
                for key, value in filters.items():
                    if key and value:
                        query = query.eq(key, value)
            
            # Apply pagination
            query = query.range(offset, offset + limit - 1)
            
            # Execute query
            response = query.execute()
            
            # Convert response data to Pet objects
            pets = [Pet.from_supabase(item) for item in response.data]
            
            return pets
            
        except Exception as e:
            return []
    
    @staticmethod
    async def get_pet_by_id(pet_id: str) -> Optional[Pet]:
        """
        Get a pet by its ID.
        
        Args:
            pet_id: ID of the pet to retrieve
            
        Returns:
            Optional[Pet]: Pet if found, None otherwise
        """
        try:
            client = supabase_manager.get_client()
            response = client.table("pets").select("*").eq("id", pet_id).execute()
            
            if not response.data or len(response.data) == 0:
                return None
            
            pet = Pet.from_supabase(response.data[0])
            
            return pet
            
        except Exception as e:
            return None
    
    @staticmethod
    async def update_pet(pet_id: str, update_data: PetUpdate) -> Optional[Pet]:
        """
        Update a pet's information.
        
        Args:
            pet_id: ID of the pet to update
            update_data: Data to update
            
        Returns:
            Optional[Pet]: Updated pet if successful, None otherwise
        """
        try:
            # Convert data to dict and remove None values
            update_dict = {k: v for k, v in update_data.dict().items() if v is not None}
            
            if not update_dict:
                return await PetService.get_pet_by_id(pet_id)
            
            # Update pet in Supabase
            client = supabase_manager.get_client()
            response = client.table("pets").update(update_dict).eq("id", pet_id).execute()
            
            if not response.data or len(response.data) == 0:
                return None
            
            # Return updated pet
            pet = Pet.from_supabase(response.data[0])
            
            return pet
            
        except Exception as e:
            return None
    
    @staticmethod
    async def delete_pet(pet_id: str) -> bool:
        """
        Delete a pet listing.
        
        Args:
            pet_id: ID of the pet to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            client = supabase_manager.get_client()
            response = client.table("pets").delete().eq("id", pet_id).execute()
            
            success = response.data is not None and len(response.data) > 0
            if success:
                pass
            else:
                pass
            
            return success
            
        except Exception as e:
            return False