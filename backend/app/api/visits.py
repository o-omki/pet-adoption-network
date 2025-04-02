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
    
    For adopters, this returns their own visit schedules.
    For pet owners, this returns visit schedules for their pets.
    For admins, this returns all visit schedules.
    
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
    
    # Apply pet_id filter if provided
    if pet_id:
        filters["pet_id"] = pet_id
    
    # Apply status filter if provided
    if status:
        filters["status"] = status
    
    # Apply role-based filters
    if current_user["role"] == UserRole.ADOPTER:
        # Adopters can only see their own visit schedules
        filters["adopter_id"] = current_user["user_id"]
    elif current_user["role"] == UserRole.SHELTER or current_user["role"] == UserRole.INDIVIDUAL:
        # Get the user's pets to filter visit schedules for
        pets = await PetService.get_pets({"owner_id": current_user["user_id"]})
        if not pets:
            return []  # User has no pets, so return empty list
        
        # If pet_id was specified in filters, verify it belongs to the user
        if "pet_id" in filters:
            is_owner = any(pet.pet_id == filters["pet_id"] for pet in pets)
            if not is_owner:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You don't have permission to view visit schedules for this pet"
                )
        else:
            # No specific pet_id was provided, so show visit schedules for all user's pets
            # We can't do this easily with a single filter, so we'll get all visits
            # and filter in code (this is inefficient but works for demo purposes)
            pet_ids = [pet.pet_id for pet in pets]
            visits = []
            for pet_id in pet_ids:
                pet_filters = filters.copy()
                pet_filters["pet_id"] = pet_id
                pet_visits = await VisitService.get_visits(pet_filters, limit, offset)
                visits.extend(pet_visits)
            return [visit.to_dict() for visit in visits[:limit]]
    
    # For admins or the filtered case of pets owners
    visits = await VisitService.get_visits(filters, limit, offset)
    return [visit.to_dict() for visit in visits]


@router.get("/{visit_id}", response_model=VisitScheduleResponse)
async def get_visit_schedule(
    visit_id: str = Path(..., description="The ID of the visit schedule to retrieve"),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Any:
    """
    Get a specific visit schedule by ID.
    
    Users can only view visit schedules they submitted or that were submitted for their pets.
    Admins can view any visit schedule.
    
    Args:
        visit_id: ID of the visit schedule to retrieve
        current_user: Current authenticated user
        
    Returns:
        VisitScheduleResponse: Visit schedule details
        
    Raises:
        HTTPException: If visit schedule is not found or user doesn't have permission
    """
    visit = await VisitService.get_visit_by_id(visit_id)
    if not visit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Visit schedule not found"
        )
    
    # Check if user has permission to view this visit schedule
    if current_user["role"] == UserRole.ADMIN:
        pass  # Admins can view any visit schedule
    elif current_user["role"] == UserRole.ADOPTER and current_user["user_id"] == visit.adopter_id:
        pass  # Adopters can view their own visit schedules
    else:
        # For shelter/individual users, check if they own the pet
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
    
    Pet owners can update visit schedules for their pets (confirm, complete).
    Adopters can update their own visit schedules (cancel).
    Admins can update any visit schedule.
    
    Args:
        update_data: Updated status for the visit schedule
        visit_id: ID of the visit schedule to update
        current_user: Current authenticated user
        
    Returns:
        VisitScheduleResponse: Updated visit schedule details
        
    Raises:
        HTTPException: If update fails or user doesn't have permission
    """
    # Get the visit schedule to check permissions
    visit = await VisitService.get_visit_by_id(visit_id)
    if not visit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Visit schedule not found"
        )
    
    # Check if user has permission to update this visit schedule
    if current_user["role"] == UserRole.ADMIN:
        pass  # Admins can update any visit schedule
    elif current_user["role"] == UserRole.ADOPTER and current_user["user_id"] == visit.adopter_id:
        # Adopters can only cancel their own visit schedules
        if update_data.status != "cancelled":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Adopters can only cancel their visit schedules"
            )
    else:
        # For shelter/individual users, check if they own the pet
        pet = await PetService.get_pet_by_id(visit.pet_id)
        if not pet or pet.owner_id != current_user["user_id"]:
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
    
    Adopters can delete their own visit schedules.
    Pet owners can delete visit schedules for their pets.
    Admins can delete any visit schedule.
    
    Args:
        visit_id: ID of the visit schedule to delete
        current_user: Current authenticated user
        
    Returns:
        Dict: Success message
        
    Raises:
        HTTPException: If deletion fails or user doesn't have permission
    """
    # Get the visit schedule to check permissions
    visit = await VisitService.get_visit_by_id(visit_id)
    if not visit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Visit schedule not found"
        )
    
    # Check if user has permission to delete this visit schedule
    if current_user["role"] == UserRole.ADMIN:
        pass  # Admins can delete any visit schedule
    elif current_user["role"] == UserRole.ADOPTER and current_user["user_id"] == visit.adopter_id:
        pass  # Adopters can delete their own visit schedules
    else:
        # For shelter/individual users, check if they own the pet
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