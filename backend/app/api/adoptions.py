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
    
    For adopters, this returns their own applications.
    For pet owners, this returns applications for their pets.
    For admins, this returns all applications.
    
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
        filters["pet_id"] = pet_id
    
    if status:
        filters["status"] = status
    
    if current_user["role"] == UserRole.ADOPTER:
        # Adopters can only see their own applications
        filters["adopter_id"] = current_user["user_id"]
    elif current_user["role"] == UserRole.SHELTER or current_user["role"] == UserRole.INDIVIDUAL:
        # Get the user's pets to filter applications for
        pets = await PetService.get_pets({"owner_id": current_user["user_id"]})
        if not pets:
            return []  # User has no pets, so return empty list
        
        # If pet_id was specified in filters, verify it belongs to the user
        if "pet_id" in filters:
            is_owner = any(pet.pet_id == filters["pet_id"] for pet in pets)
            if not is_owner:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You don't have permission to view applications for this pet"
                )
        else:
            # No specific pet_id was provided, so show applications for all user's pets
            # We can't do this easily with a single filter, so we'll get all applications
            # and filter in code (this is inefficient but works for demo purposes)
            pet_ids = [pet.pet_id for pet in pets]
            applications = []
            for pet_id in pet_ids:
                pet_filters = filters.copy()
                pet_filters["pet_id"] = pet_id
                pet_applications = await AdoptionService.get_applications(pet_filters, limit, offset)
                applications.extend(pet_applications)
            return [app.to_dict() for app in applications[:limit]]
    
    # For admins or the filtered case of pets owners
    applications = await AdoptionService.get_applications(filters, limit, offset)
    return [app.to_dict() for app in applications]


@router.get("/{application_id}", response_model=AdoptionApplicationResponse)
async def get_adoption_application(
    application_id: str = Path(..., description="The ID of the adoption application to retrieve"),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Any:
    """
    Get a specific adoption application by ID.
    
    Users can only view applications they submitted or that were submitted for their pets.
    Admins can view any application.
    
    Args:
        application_id: ID of the application to retrieve
        current_user: Current authenticated user
        
    Returns:
        AdoptionApplicationResponse: Application details
        
    Raises:
        HTTPException: If application is not found or user doesn't have permission
    """
    application = await AdoptionService.get_application_by_id(application_id)
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Adoption application not found"
        )
    
    # Check if user has permission to view this application
    if current_user["role"] == UserRole.ADMIN:
        pass  # Admins can view any application
    elif current_user["role"] == UserRole.ADOPTER and current_user["user_id"] == application.adopter_id:
        pass  # Adopters can view their own applications
    else:
        # For shelter/individual users, check if they own the pet
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
    
    Pet owners can update applications for their pets.
    Admins can update any application.
    
    Args:
        update_data: Updated status for the application
        application_id: ID of the application to update
        current_user: Current authenticated user
        
    Returns:
        AdoptionApplicationResponse: Updated application details
        
    Raises:
        HTTPException: If update fails or user doesn't have permission
    """
    # Get the application to check permissions
    application = await AdoptionService.get_application_by_id(application_id)
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Adoption application not found"
        )
    
    # Check if user has permission to update this application
    if current_user["role"] == UserRole.ADMIN:
        pass  # Admins can update any application
    else:
        # For shelter/individual users, check if they own the pet
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
        # Update pet status to "adopted"
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
    
    Adopters can delete their own applications.
    Pet owners can delete applications for their pets.
    Admins can delete any application.
    
    Args:
        application_id: ID of the application to delete
        current_user: Current authenticated user
        
    Returns:
        Dict: Success message
        
    Raises:
        HTTPException: If deletion fails or user doesn't have permission
    """
    # Get the application to check permissions
    application = await AdoptionService.get_application_by_id(application_id)
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Adoption application not found"
        )
    
    # Check if user has permission to delete this application
    if current_user["role"] == UserRole.ADMIN:
        pass  # Admins can delete any application
    elif current_user["role"] == UserRole.ADOPTER and current_user["user_id"] == application.adopter_id:
        pass  # Adopters can delete their own applications
    else:
        # For shelter/individual users, check if they own the pet
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