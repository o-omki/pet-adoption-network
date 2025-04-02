from typing import Dict, List, Optional, Any
from datetime import datetime
from app.db.supabase_client import supabase_manager
from app.models.visit import VisitSchedule, VisitStatus
from app.schemas.visit import VisitScheduleCreate, VisitScheduleUpdate


class VisitService:
    """Service for handling visit scheduling operations."""
    
    @staticmethod
    async def create_visit(adopter_id: str, visit_data: VisitScheduleCreate) -> VisitSchedule:
        """
        Create a new visit schedule.
        
        Args:
            adopter_id: ID of the user scheduling the visit
            visit_data: Visit data to be created
            
        Returns:
            VisitSchedule: The newly created visit schedule
            
        Raises:
            ValueError: If creation fails
        """
        try:
            # Prepare data for insertion
            visit_dict = visit_data.dict()
            visit_dict["adopter_id"] = adopter_id
            visit_dict["status"] = VisitStatus.PENDING.value
            
            # Insert data into Supabase
            client = supabase_manager.get_client()
            response = client.table("visit_schedules").insert(visit_dict).execute()
            
            # Check if insertion was successful
            if not response.data or len(response.data) == 0:
                raise ValueError("Failed to create visit schedule")
            
            # Return created visit schedule
            visit = VisitSchedule.from_supabase(response.data[0])
            
            return visit
            
        except Exception as e:
            raise
    
    @staticmethod
    async def get_visits(
        filters: Optional[Dict[str, Any]] = None, 
        limit: int = 100, 
        offset: int = 0
    ) -> List[VisitSchedule]:
        """
        Get a list of visit schedules with optional filtering.
        
        Args:
            filters: Optional filters to apply
            limit: Maximum number of visits to return
            offset: Offset for pagination
            
        Returns:
            List[VisitSchedule]: List of visits matching the filters
        """
        try:
            client = supabase_manager.get_client()
            query = client.table("visit_schedules").select("*")
            
            # Apply filters if provided
            if filters:
                for key, value in filters.items():
                    if key and value:
                        query = query.eq(key, value)
            
            # Apply pagination
            query = query.range(offset, offset + limit - 1).order("scheduled_date", desc=False)
            
            # Execute query
            response = query.execute()
            
            # Convert response data to VisitSchedule objects
            visits = [VisitSchedule.from_supabase(item) for item in response.data]
            
            return visits
            
        except Exception as e:
            return []
    
    @staticmethod
    async def get_visit_by_id(visit_id: str) -> Optional[VisitSchedule]:
        """
        Get a visit schedule by its ID.
        
        Args:
            visit_id: ID of the visit to retrieve
            
        Returns:
            Optional[VisitSchedule]: Visit if found, None otherwise
        """
        try:
            client = supabase_manager.get_client()
            response = client.table("visit_schedules").select("*").eq("id", visit_id).execute()
            
            if not response.data or len(response.data) == 0:
                return None
            
            visit = VisitSchedule.from_supabase(response.data[0])
            
            return visit
            
        except Exception as e:
            return None
    
    @staticmethod
    async def update_visit_status(visit_id: str, update_data: VisitScheduleUpdate) -> Optional[VisitSchedule]:
        """
        Update a visit schedule's status.
        
        Args:
            visit_id: ID of the visit to update
            update_data: Data to update
            
        Returns:
            Optional[VisitSchedule]: Updated visit if successful, None otherwise
        """
        try:
            # Convert data to dict
            update_dict = update_data.dict()
            
            # Update visit in Supabase
            client = supabase_manager.get_client()
            response = client.table("visit_schedules").update(update_dict).eq("id", visit_id).execute()
            
            if not response.data or len(response.data) == 0:
                return None
            
            # Return updated visit
            visit = VisitSchedule.from_supabase(response.data[0])
            
            return visit
            
        except Exception as e:
            return None
    
    @staticmethod
    async def delete_visit(visit_id: str) -> bool:
        """
        Delete a visit schedule.
        
        Args:
            visit_id: ID of the visit to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            client = supabase_manager.get_client()
            response = client.table("visit_schedules").delete().eq("id", visit_id).execute()
            
            success = response.data is not None and len(response.data) > 0
            if success:
                pass
            else:
                pass
            
            return success
            
        except Exception as e:
            return False