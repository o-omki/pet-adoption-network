from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from typing import List, Dict, Any, Optional
from app.api.auth import get_current_user
from app.schemas.visit import VisitScheduleCreate, VisitScheduleUpdate, VisitScheduleResponse
from app.services.visit import VisitService
from app.services.pet import PetService

router = APIRouter(tags=["visits"])


@router.post("", response_model=VisitScheduleResponse, status_code=status.HTTP_201_CREATED)
async def create_visit_schedule(
    visit_data: VisitScheduleCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Any:
    """
    Create a new visit schedule request.
    Any authenticated user can create visit schedule requests.
    
    Args:
        visit_data: Visit schedule data to create
        current_user: Current authenticated user
        
    Returns:
        VisitScheduleResponse: Created visit schedule data
    """
    try:
        # First verify the pet exists
        pet = await PetService.get_pet_by_id(visit_data.pet_id)
        if not pet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pet not found"
            )
        
        # Don't allow scheduling visits for own pet
        if pet.owner_id == current_user["user_id"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You cannot schedule a visit for your own pet"
            )
        
        # Create the visit schedule
        visit = await VisitService.create_visit(current_user["user_id"], visit_data)
        return visit.to_dict()
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create visit schedule. Please try again."
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again later."
        )


@router.get("", response_model=List[VisitScheduleResponse])
async def get_visit_schedules(
    pet_id: Optional[str] = Query(None, description="Filter by pet ID"),
    status: Optional[str] = Query(None, description="Filter by visit status"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of visit schedules to return"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Any:
    """
    Get a list of visit schedules.
    Users can see:
    - Visits they scheduled
    - Visits for pets they own
    
    Args:
        pet_id: Optional filter by pet ID
        status: Optional filter by visit status
        limit: Maximum number of results to return
        offset: Offset for pagination
        current_user: Current authenticated user
        
    Returns:
        List[VisitScheduleResponse]: List of visit schedules matching the filters
    """
    filters = {}
    
    if pet_id:
        # If pet_id filter is provided, verify user owns the pet
        pet = await PetService.get_pet_by_id(pet_id)
        if not pet:
            return []
            
        if pet.owner_id != current_user["user_id"]:
            # If user doesn't own the pet, only show their own visits
            filters["pet_id"] = pet_id
            filters["adopter_id"] = current_user["user_id"]
        else:
            # If user owns the pet, show all visits for it
            filters["pet_id"] = pet_id
    else:
        # No pet_id filter, show user's visits and visits for their pets
        pets = await PetService.get_pets({"owner_id": current_user["user_id"]})
        pet_ids = [pet.pet_id for pet in pets]
        
        if not pet_ids:
            # User has no pets, just show their visits
            filters["adopter_id"] = current_user["user_id"]
        else:
            # Show both user's visits and visits for their pets
            visits = []
            # Get visits where user is the visitor
            visitor_filters = {"adopter_id": current_user["user_id"]}
            if status:
                visitor_filters["status"] = status
            visitor_visits = await VisitService.get_visits(visitor_filters, limit, offset)
            visits.extend(visitor_visits)
            
            # Get visits for user's pets
            for pet_id in pet_ids:
                pet_filters = {"pet_id": pet_id}
                if status:
                    pet_filters["status"] = status
                pet_visits = await VisitService.get_visits(pet_filters, limit, offset)
                visits.extend(pet_visits)
            
            return [visit.to_dict() for visit in visits[:limit]]
    
    if status:
        filters["status"] = status
    
    visits = await VisitService.get_visits(filters, limit, offset)
    return [visit.to_dict() for visit in visits]


@router.get("/{visit_id}", response_model=VisitScheduleResponse)
async def get_visit_schedule(
    visit_id: str = Path(..., description="The ID of the visit schedule to retrieve"),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Any:
    """
    Get a specific visit schedule by ID.
    Users can only view:
    - Visits they scheduled
    - Visits for pets they own
    
    Args:
        visit_id: ID of the visit schedule to retrieve
        current_user: Current authenticated user
        
    Returns:
        VisitScheduleResponse: Visit schedule details
    """
    visit = await VisitService.get_visit_by_id(visit_id)
    if not visit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Visit schedule not found"
        )
    
    # Check if user has permission to view this visit schedule
    if current_user["user_id"] != visit.adopter_id:
        # If user is not the visitor, check if they own the pet
        pet = await PetService.get_pet_by_id(visit.pet_id)
        if not pet or pet.owner_id != current_user["user_id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to view this visit schedule"
            )
    
    return visit.to_dict()


@router.put("/{visit_id}", response_model=VisitScheduleResponse)
async def update_visit_schedule(
    update_data: VisitScheduleUpdate,
    visit_id: str = Path(..., description="The ID of the visit schedule to update"),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Any:
    """
    Update the status of a visit schedule.
    - Pet owners can update visit status to any state
    - Visitors can only cancel their own visits
    
    Args:
        update_data: Updated status for the visit schedule
        visit_id: ID of the visit schedule to update
        current_user: Current authenticated user
        
    Returns:
        VisitScheduleResponse: Updated visit schedule details
    """
    # Get the visit schedule to check permissions
    visit = await VisitService.get_visit_by_id(visit_id)
    if not visit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Visit schedule not found"
        )
    
    # Get the pet to check ownership
    pet = await PetService.get_pet_by_id(visit.pet_id)
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pet not found"
        )
    
    # Check permissions
    if pet.owner_id == current_user["user_id"]:
        # Pet owner can update to any status
        pass
    elif visit.adopter_id == current_user["user_id"]:
        # Visitor can only cancel their own visits
        if update_data.status != "cancelled":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Visitors can only cancel their scheduled visits"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this visit schedule"
        )
    
    # Update the visit schedule
    updated_visit = await VisitService.update_visit_status(visit_id, update_data)
    if not updated_visit:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update visit schedule"
        )
    
    return updated_visit.to_dict()


@router.delete("/{visit_id}", status_code=status.HTTP_200_OK)
async def delete_visit_schedule(
    visit_id: str = Path(..., description="The ID of the visit schedule to delete"),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, str]:
    """
    Delete a visit schedule.
    Users can only delete:
    - Visits they scheduled
    - Visits for pets they own
    
    Args:
        visit_id: ID of the visit schedule to delete
        current_user: Current authenticated user
        
    Returns:
        Dict: Success message
    """
    # Get the visit schedule to check permissions
    visit = await VisitService.get_visit_by_id(visit_id)
    if not visit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Visit schedule not found"
        )
    
    # Check if user has permission to delete this visit schedule
    if current_user["user_id"] != visit.adopter_id:
        # If user is not the visitor, check if they own the pet
        pet = await PetService.get_pet_by_id(visit.pet_id)
        if not pet or pet.owner_id != current_user["user_id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to delete this visit schedule"
            )
    
    # Delete the visit schedule
    success = await VisitService.delete_visit(visit_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete visit schedule"
        )
    
    return {"message": "Visit schedule deleted successfully"}