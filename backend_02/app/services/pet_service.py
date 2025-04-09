from typing import Dict, List, Optional, Any

from app.core.database import supabase_client
from app.schemas.pet import PetCreate, PetUpdate, PetStatus, PetFilter


class PetService:
    """
    Service for handling pet-related database operations.
    """
    
    @staticmethod
    async def create_pet(pet_data: PetCreate, owner_id: str) -> Dict[str, Any]:
        """
        Create a new pet listing.
        
        Args:
            pet_data: Pet data for creation.
            owner_id: ID of the user creating the pet listing.
            
        Returns:
            The created pet data.
        """
        # Create pet in database
        pet_dict = pet_data.dict()
        pet_dict["owner_id"] = owner_id
        pet_dict["status"] = PetStatus.AVAILABLE
        
        result = supabase_client.table("pets").insert(pet_dict).execute()
        
        if not result.data:
            raise ValueError("Failed to create pet listing")
        
        return result.data[0]
    
    @staticmethod
    async def get_pet_by_id(pet_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a pet by ID.
        
        Args:
            pet_id: ID of the pet to retrieve.
            
        Returns:
            Pet data or None if not found.
        """
        result = supabase_client.table("pets").select("*").eq("pet_id", pet_id).execute()
        if not result.data:
            return None
            
        pet = result.data[0]
        
        # Get pet type name
        pet_type_result = supabase_client.table("pet_types").select("*").eq("pet_type_id", pet["pet_type_id"]).execute()
        if pet_type_result.data:
            pet["pet_type_name"] = pet_type_result.data[0]["type_name"]
        
        # Get breed name if available
        if pet.get("breed_id"):
            breed_result = supabase_client.table("breeds").select("*").eq("breed_id", pet["breed_id"]).execute()
            if breed_result.data:
                pet["breed_name"] = breed_result.data[0]["breed_name"]
        
        # Get owner name
        owner_result = supabase_client.table("users").select("username").eq("user_id", pet["owner_id"]).execute()
        if owner_result.data:
            pet["owner_name"] = owner_result.data[0]["username"]
            
        return pet
    
    @staticmethod
    async def get_pets(filters: Optional[PetFilter] = None, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get pets with optional filtering.
        
        Args:
            filters: Optional filters to apply.
            skip: Number of records to skip (for pagination).
            limit: Maximum number of records to return.
            
        Returns:
            List of pets matching the criteria.
        """
        query = supabase_client.table("pets").select("*").range(skip, skip + limit - 1)
        
        # Apply filters if provided
        if filters:
            filter_dict = filters.dict(exclude_none=True)
            for key, value in filter_dict.items():
                # Handle special filters
                if key == "age_min":
                    query = query.gte("age", value)
                elif key == "age_max":
                    query = query.lte("age", value)
                else:
                    query = query.eq(key, value)
        
        result = query.execute()
        
        # Enhance pets with additional information
        pets = result.data
        if not pets:
            return []
            
        # Get pet types for all pets
        pet_type_ids = list(set(pet["pet_type_id"] for pet in pets if pet.get("pet_type_id")))
        if pet_type_ids:
            pet_types_result = supabase_client.table("pet_types").select("*").in_("pet_type_id", pet_type_ids).execute()
            pet_types = {pt["pet_type_id"]: pt["type_name"] for pt in pet_types_result.data} if pet_types_result.data else {}
            
            for pet in pets:
                if pet.get("pet_type_id") in pet_types:
                    pet["pet_type_name"] = pet_types[pet["pet_type_id"]]
        
        # Get breeds for all pets
        breed_ids = list(set(pet["breed_id"] for pet in pets if pet.get("breed_id")))
        if breed_ids:
            breeds_result = supabase_client.table("breeds").select("*").in_("breed_id", breed_ids).execute()
            breeds = {b["breed_id"]: b["breed_name"] for b in breeds_result.data} if breeds_result.data else {}
            
            for pet in pets:
                if pet.get("breed_id") in breeds:
                    pet["breed_name"] = breeds[pet["breed_id"]]
                    
        # Get owner names
        owner_ids = list(set(pet["owner_id"] for pet in pets if pet.get("owner_id")))
        if owner_ids:
            owners_result = supabase_client.table("users").select("user_id, username").in_("user_id", owner_ids).execute()
            owners = {o["user_id"]: o["username"] for o in owners_result.data} if owners_result.data else {}
            
            for pet in pets:
                if pet.get("owner_id") in owners:
                    pet["owner_name"] = owners[pet["owner_id"]]
        
        return pets
    
    @staticmethod
    async def update_pet(pet_id: str, pet_data: PetUpdate) -> Dict[str, Any]:
        """
        Update a pet listing.
        
        Args:
            pet_id: ID of the pet to update.
            pet_data: Updated pet data.
            
        Returns:
            The updated pet data.
        """
        update_data = pet_data.dict(exclude_none=True)
        
        result = supabase_client.table("pets").update(update_data).eq("pet_id", pet_id).execute()
        
        if not result.data:
            raise ValueError("Failed to update pet listing")
        
        return result.data[0]
    
    @staticmethod
    async def delete_pet(pet_id: str) -> bool:
        """
        Delete a pet listing.
        
        Args:
            pet_id: ID of the pet to delete.
            
        Returns:
            True if deletion was successful, False otherwise.
        """
        result = supabase_client.table("pets").delete().eq("pet_id", pet_id).execute()
        
        return bool(result.data)
    
    @staticmethod
    async def is_pet_owner(pet_id: str, user_id: str) -> bool:
        """
        Check if a user is the owner of a pet.
        
        Args:
            pet_id: ID of the pet.
            user_id: ID of the user.
            
        Returns:
            True if the user is the pet's owner, False otherwise.
        """
        result = supabase_client.table("pets").select("owner_id").eq("pet_id", pet_id).execute()
        
        if not result.data:
            return False
            
        return result.data[0]["owner_id"] == user_id
