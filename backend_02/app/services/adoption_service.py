from typing import Dict, List, Optional, Any

from app.core.database import supabase
from app.schemas.adoption import AdoptionApplicationCreate, AdoptionApplicationUpdate, AdoptionStatus
from app.services.pet_service import PetService


class AdoptionService:
    """
    Service for handling adoption application-related database operations.
    """
    
    @staticmethod
    async def create_application(application_data: AdoptionApplicationCreate, adopter_id: str) -> Dict[str, Any]:
        """
        Create a new adoption application.
        
        Args:
            application_data: Application data for creation.
            adopter_id: ID of the user applying for adoption.
            
        Returns:
            The created application data.
        """
        # Create application in database
        application_dict = application_data.dict()
        application_dict["adopter_id"] = adopter_id
        application_dict["status"] = AdoptionStatus.SUBMITTED
        
        result = supabase.table("adoption_applications").insert(application_dict).execute()
        
        if not result.data:
            raise ValueError("Failed to create adoption application")
        
        # Update pet status to pending
        supabase.table("pets").update({"status": "pending"}).eq("pet_id", application_data.pet_id).execute()
        
        return result.data[0]
    
    @staticmethod
    async def get_application_by_id(application_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve an application by ID.
        
        Args:
            application_id: ID of the application to retrieve.
            
        Returns:
            Application data or None if not found.
        """
        result = supabase.table("adoption_applications").select("*").eq("application_id", application_id).execute()
        if not result.data:
            return None
            
        application = result.data[0]
        
        # Get pet name
        pet_result = supabase.table("pets").select("name").eq("pet_id", application["pet_id"]).execute()
        if pet_result.data:
            application["pet_name"] = pet_result.data[0]["name"]
        
        # Get adopter name
        adopter_result = supabase.table("users").select("username").eq("user_id", application["adopter_id"]).execute()
        if adopter_result.data:
            application["adopter_name"] = adopter_result.data[0]["username"]
            
        return application
    
    @staticmethod
    async def get_applications_by_adopter(adopter_id: str) -> List[Dict[str, Any]]:
        """
        Get all applications submitted by a specific adopter.
        
        Args:
            adopter_id: ID of the adopter.
            
        Returns:
            List of adoption applications for the adopter.
        """
        result = supabase.table("adoption_applications").select("*").eq("adopter_id", adopter_id).execute()
        
        if not result.data:
            return []
            
        applications = result.data
        
        # Get pet names
        pet_ids = [app["pet_id"] for app in applications]
        pets_result = supabase.table("pets").select("pet_id, name").in_("pet_id", pet_ids).execute()
        
        pet_names = {}
        if pets_result.data:
            pet_names = {pet["pet_id"]: pet["name"] for pet in pets_result.data}
        
        # Add pet names to applications
        for app in applications:
            app["pet_name"] = pet_names.get(app["pet_id"], "Unknown")
            app["adopter_name"] = "Self"  # Since we're querying by adopter ID
            
        return applications
    
    @staticmethod
    async def get_applications_for_pet_owner(owner_id: str) -> List[Dict[str, Any]]:
        """
        Get all applications for pets owned by a specific user.
        
        Args:
            owner_id: ID of the pet owner.
            
        Returns:
            List of adoption applications for the owner's pets.
        """
        # First, get all pets owned by this user
        pets_result = supabase.table("pets").select("pet_id").eq("owner_id", owner_id).execute()
        
        if not pets_result.data:
            return []
            
        pet_ids = [pet["pet_id"] for pet in pets_result.data]
        
        # Get all applications for these pets
        applications_result = supabase.table("adoption_applications").select("*").in_("pet_id", pet_ids).execute()
        
        if not applications_result.data:
            return []
            
        applications = applications_result.data
        
        # Get pet names
        pets_result = supabase.table("pets").select("pet_id, name").in_("pet_id", pet_ids).execute()
        
        pet_names = {}
        if pets_result.data:
            pet_names = {pet["pet_id"]: pet["name"] for pet in pets_result.data}
        
        # Get adopter names
        adopter_ids = [app["adopter_id"] for app in applications]
        adopters_result = supabase.table("users").select("user_id, username").in_("user_id", adopter_ids).execute()
        
        adopter_names = {}
        if adopters_result.data:
            adopter_names = {adopter["user_id"]: adopter["username"] for adopter in adopters_result.data}
        
        # Add pet and adopter names to applications
        for app in applications:
            app["pet_name"] = pet_names.get(app["pet_id"], "Unknown")
            app["adopter_name"] = adopter_names.get(app["adopter_id"], "Unknown")
            
        return applications
    
    @staticmethod
    async def update_application_status(application_id: str, status_update: AdoptionApplicationUpdate) -> Dict[str, Any]:
        """
        Update an adoption application status.
        
        Args:
            application_id: ID of the application to update.
            status_update: New status data.
            
        Returns:
            The updated application data.
        """
        # Get the application to verify it exists
        application_result = supabase.table("adoption_applications").select("*").eq("application_id", application_id).execute()
        
        if not application_result.data:
            raise ValueError("Adoption application not found")
            
        application = application_result.data[0]
        
        # Update the application status
        update_data = {"status": status_update.status}
        result = supabase.table("adoption_applications").update(update_data).eq("application_id", application_id).execute()
        
        if not result.data:
            raise ValueError("Failed to update application status")
        
        # If approved, update pet status to adopted
        if status_update.status == AdoptionStatus.APPROVED:
            supabase.table("pets").update({"status": "adopted"}).eq("pet_id", application["pet_id"]).execute()
            
            # Reject all other applications for this pet
            supabase.table("adoption_applications").update({"status": "rejected"}) \
                .eq("pet_id", application["pet_id"]) \
                .neq("application_id", application_id) \
                .execute()
                
        return result.data[0]
    
    @staticmethod
    async def is_pet_owner_for_application(application_id: str, user_id: str) -> bool:
        """
        Check if a user is the owner of the pet in an application.
        
        Args:
            application_id: ID of the application.
            user_id: ID of the user.
            
        Returns:
            True if the user is the pet owner, False otherwise.
        """
        # Get the application
        application_result = supabase.table("adoption_applications").select("pet_id").eq("application_id", application_id).execute()
        
        if not application_result.data:
            return False
            
        pet_id = application_result.data[0]["pet_id"]
        
        # Check if user is the owner of this pet
        return await PetService.is_pet_owner(pet_id, user_id)
