from typing import Dict, List, Optional, Any
from app.db.supabase_client import supabase_manager
from app.models.adoption import AdoptionApplication, ApplicationStatus
from app.schemas.adoption import AdoptionApplicationCreate, AdoptionApplicationUpdate


class AdoptionService:
    """Service for handling adoption application operations."""
    
    @staticmethod
    async def create_application(adopter_id: str, application_data: AdoptionApplicationCreate) -> AdoptionApplication:
        """
        Create a new adoption application.
        
        Args:
            adopter_id: ID of the user submitting the application
            application_data: Application data to be created
            
        Returns:
            AdoptionApplication: The newly created application
            
        Raises:
            ValueError: If creation fails
        """
        try:
            # Prepare data for insertion
            application_dict = application_data.dict()
            application_dict["adopter_id"] = adopter_id
            application_dict["status"] = ApplicationStatus.SUBMITTED.value
            
            # Insert data into Supabase
            client = supabase_manager.get_client()
            response = client.table("adoption_applications").insert(application_dict).execute()
            
            # Check if insertion was successful
            if not response.data or len(response.data) == 0:
                raise ValueError("Failed to create adoption application")
            
            # Return created application
            application = AdoptionApplication.from_supabase(response.data[0])
            
            return application
            
        except Exception as e:
            raise
    
    @staticmethod
    async def get_applications(
        filters: Optional[Dict[str, Any]] = None, 
        limit: int = 100, 
        offset: int = 0
    ) -> List[AdoptionApplication]:
        """
        Get a list of adoption applications with optional filtering.
        
        Args:
            filters: Optional filters to apply
            limit: Maximum number of applications to return
            offset: Offset for pagination
            
        Returns:
            List[AdoptionApplication]: List of applications matching the filters
        """
        try:
            client = supabase_manager.get_client()
            query = client.table("adoption_applications").select("*")
            
            # Apply filters if provided
            if filters:
                for key, value in filters.items():
                    if key and value:
                        query = query.eq(key, value)
            
            # Apply pagination
            query = query.range(offset, offset + limit - 1).order("submitted_at", desc=True)
            
            # Execute query
            response = query.execute()
            
            # Convert response data to AdoptionApplication objects
            applications = [AdoptionApplication.from_supabase(item) for item in response.data]
            
            return applications
            
        except Exception as e:
            return []
    
    @staticmethod
    async def get_application_by_id(application_id: str) -> Optional[AdoptionApplication]:
        """
        Get an adoption application by its ID.
        
        Args:
            application_id: ID of the application to retrieve
            
        Returns:
            Optional[AdoptionApplication]: Application if found, None otherwise
        """
        try:
            client = supabase_manager.get_client()
            response = client.table("adoption_applications").select("*").eq("id", application_id).execute()
            
            if not response.data or len(response.data) == 0:
                return None
            
            application = AdoptionApplication.from_supabase(response.data[0])
            
            return application
            
        except Exception as e:
            return None
    
    @staticmethod
    async def update_application_status(application_id: str, update_data: AdoptionApplicationUpdate) -> Optional[AdoptionApplication]:
        """
        Update an adoption application's status.
        
        Args:
            application_id: ID of the application to update
            update_data: Data to update
            
        Returns:
            Optional[AdoptionApplication]: Updated application if successful, None otherwise
        """
        try:
            # Convert data to dict
            update_dict = update_data.dict()
            
            # Update application in Supabase
            client = supabase_manager.get_client()
            response = client.table("adoption_applications").update(update_dict).eq("id", application_id).execute()
            
            if not response.data or len(response.data) == 0:
                return None
            
            # Return updated application
            application = AdoptionApplication.from_supabase(response.data[0])
            
            return application
            
        except Exception as e:
            return None
    
    @staticmethod
    async def delete_application(application_id: str) -> bool:
        """
        Delete an adoption application.
        
        Args:
            application_id: ID of the application to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            client = supabase_manager.get_client()
            response = client.table("adoption_applications").delete().eq("id", application_id).execute()
            
            success = response.data is not None and len(response.data) > 0
            return success
            
        except Exception as e:
            return False