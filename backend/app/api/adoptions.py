from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from typing import List, Dict, Any, Optional
from app.api.auth import get_current_user
from app.schemas.adoption import AdoptionApplicationCreate, AdoptionApplicationUpdate, AdoptionApplicationResponse
from app.services.adoption import AdoptionService
from app.services.pet import PetService

router = APIRouter(tags=["adoptions"])


@router.post("", response_model=AdoptionApplicationResponse, status_code=status.HTTP_201_CREATED)
async def create_adoption_application(
    application_data: AdoptionApplicationCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Any:
    """
    Create a new adoption application.
    Any authenticated user can create adoption applications.
    
    Args:
        application_data: Application data to create
        current_user: Current authenticated user
        
    Returns:
        AdoptionApplicationResponse: Created application data
    """
    try:
        # First verify the pet exists
        pet = await PetService.get_pet_by_id(application_data.pet_id)
        if not pet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pet not found"
            )
        
        # Don't allow applying for own pet
        if pet.owner_id == current_user["user_id"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You cannot apply to adopt your own pet"
            )
        
        application = await AdoptionService.create_application(current_user["user_id"], application_data)
        return application.to_dict()
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create adoption application. Please try again."
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again later."
        )


@router.get("", response_model=List[AdoptionApplicationResponse])
async def get_adoption_applications(
    pet_id: Optional[str] = Query(None, description="Filter by pet ID"),
    status: Optional[str] = Query(None, description="Filter by application status"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of applications to return"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Any:
    """
    Get a list of adoption applications.
    Users can see:
    - Applications they submitted
    - Applications for pets they own
    
    Args:
        pet_id: Optional filter by pet ID
        status: Optional filter by application status
        limit: Maximum number of results to return
        offset: Offset for pagination
        current_user: Current authenticated user
        
    Returns:
        List[AdoptionApplicationResponse]: List of applications matching the filters
    """
    filters = {}
    
    if pet_id:
        # If pet_id filter is provided, verify user owns the pet
        pet = await PetService.get_pet_by_id(pet_id)
        if not pet:
            return []
            
        if pet.owner_id != current_user["user_id"]:
            # If user doesn't own the pet, only show their own applications
            filters["pet_id"] = pet_id
            filters["adopter_id"] = current_user["user_id"]
        else:
            # If user owns the pet, show all applications for it
            filters["pet_id"] = pet_id
    else:
        # No pet_id filter, show user's applications and applications for their pets
        pets = await PetService.get_pets({"owner_id": current_user["user_id"]})
        pet_ids = [pet.pet_id for pet in pets]
        
        if not pet_ids:
            # User has no pets, just show their applications
            filters["adopter_id"] = current_user["user_id"]
        else:
            # Show both user's applications and applications for their pets
            applications = []
            # Get applications where user is the adopter
            adopter_filters = {"adopter_id": current_user["user_id"]}
            if status:
                adopter_filters["status"] = status
            adopter_apps = await AdoptionService.get_applications(adopter_filters, limit, offset)
            applications.extend(adopter_apps)
            
            # Get applications for user's pets
            for pet_id in pet_ids:
                pet_filters = {"pet_id": pet_id}
                if status:
                    pet_filters["status"] = status
                pet_apps = await AdoptionService.get_applications(pet_filters, limit, offset)
                applications.extend(pet_apps)
            
            return [app.to_dict() for app in applications[:limit]]
    
    if status:
        filters["status"] = status
    
    applications = await AdoptionService.get_applications(filters, limit, offset)
    return [app.to_dict() for app in applications]


@router.get("/{application_id}", response_model=AdoptionApplicationResponse)
async def get_adoption_application(
    application_id: str = Path(..., description="The ID of the adoption application to retrieve"),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Any:
    """
    Get a specific adoption application by ID.
    Users can only view:
    - Applications they submitted
    - Applications for pets they own
    
    Args:
        application_id: ID of the application to retrieve
        current_user: Current authenticated user
        
    Returns:
        AdoptionApplicationResponse: Application details
    """
    application = await AdoptionService.get_application_by_id(application_id)
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Adoption application not found"
        )
    
    # Check if user has permission to view this application
    if current_user["user_id"] != application.adopter_id:
        # If user is not the adopter, check if they own the pet
        pet = await PetService.get_pet_by_id(application.pet_id)
        if not pet or pet.owner_id != current_user["user_id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to view this application"
            )
    
    return application.to_dict()


@router.put("/{application_id}", response_model=AdoptionApplicationResponse)
async def update_adoption_application(
    update_data: AdoptionApplicationUpdate,
    application_id: str = Path(..., description="The ID of the adoption application to update"),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Any:
    """
    Update the status of an adoption application.
    Only the pet owner can update application status.
    
    Args:
        update_data: Updated status for the application
        application_id: ID of the application to update
        current_user: Current authenticated user
        
    Returns:
        AdoptionApplicationResponse: Updated application details
    """
    # Get the application to check permissions
    application = await AdoptionService.get_application_by_id(application_id)
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Adoption application not found"
        )
    
    # Check if user owns the pet
    pet = await PetService.get_pet_by_id(application.pet_id)
    if not pet or pet.owner_id != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this application"
        )
    
    # Update the application
    updated_application = await AdoptionService.update_application_status(application_id, update_data)
    if not updated_application:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update adoption application"
        )
    
    # If application was approved, update pet status
    if update_data.status == "approved":
        await PetService.update_pet(
            pet_id=application.pet_id,
            update_data={
                "status": "adopted"
            }
        )
    
    return updated_application.to_dict()


@router.delete("/{application_id}", status_code=status.HTTP_200_OK)
async def delete_adoption_application(
    application_id: str = Path(..., description="The ID of the adoption application to delete"),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, str]:
    """
    Delete an adoption application.
    Users can only delete:
    - Their own applications
    - Applications for pets they own
    
    Args:
        application_id: ID of the application to delete
        current_user: Current authenticated user
        
    Returns:
        Dict: Success message
    """
    # Get the application to check permissions
    application = await AdoptionService.get_application_by_id(application_id)
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Adoption application not found"
        )
    
    # Check if user has permission to delete this application
    if current_user["user_id"] != application.adopter_id:
        # If user is not the adopter, check if they own the pet
        pet = await PetService.get_pet_by_id(application.pet_id)
        if not pet or pet.owner_id != current_user["user_id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to delete this application"
            )
    
    # Delete the application
    success = await AdoptionService.delete_application(application_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete adoption application"
        )
    
    return {"message": "Adoption application deleted successfully"}