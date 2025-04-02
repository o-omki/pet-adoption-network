from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from typing import List, Dict, Any, Optional
from app.api.auth import get_current_user
from app.schemas.pet import PetCreate, PetUpdate, PetResponse
from app.schemas.user import UserResponse
from app.services.pet import PetService

router = APIRouter(tags=["pets"])


@router.post("", response_model=PetResponse, status_code=status.HTTP_201_CREATED)
async def create_pet(
    pet_data: PetCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Any:
    """
    Create a new pet listing.
    Any authenticated user can create pet listings.
    
    Args:
        pet_data: Pet data to create
        current_user: Current authenticated user
        
    Returns:
        PetResponse: Created pet data
    """
    try:
        pet = await PetService.create_pet(current_user["user_id"], pet_data)
        return pet.to_dict()
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create pet listing. Please check your information and try again."
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again later."
        )


@router.get("", response_model=List[PetResponse])
async def get_pets(
    pet_type_id: Optional[int] = Query(None, description="Filter by pet type"),
    breed_id: Optional[int] = Query(None, description="Filter by breed"),
    status: Optional[str] = Query(None, description="Filter by adoption status (available, pending, adopted)"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of pets to return"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
) -> Any:
    """
    Get a list of pets with optional filtering.
    
    This endpoint is publicly accessible and allows filtering pets by various criteria.
    
    Args:
        pet_type_id: Optional filter by pet type
        breed_id: Optional filter by breed
        status: Optional filter by adoption status
        limit: Maximum number of results to return
        offset: Offset for pagination
        
    Returns:
        List[PetResponse]: List of pets matching the filters
    """
    filters = {}
    if pet_type_id is not None:
        filters["pet_type_id"] = pet_type_id
    if breed_id is not None:
        filters["breed_id"] = breed_id
    if status is not None:
        filters["status"] = status
    
    pets = await PetService.get_pets(filters, limit, offset)
    return [pet.to_dict() for pet in pets]


@router.get("/{pet_id}", response_model=PetResponse)
async def get_pet(
    pet_id: str = Path(..., description="The ID of the pet to retrieve")
) -> Any:
    """
    Get a specific pet by ID.
    
    This endpoint is publicly accessible and retrieves detailed information about a specific pet.
    
    Args:
        pet_id: ID of the pet to retrieve
        
    Returns:
        PetResponse: Pet details
        
    Raises:
        HTTPException: If pet is not found
    """
    pet = await PetService.get_pet_by_id(pet_id)
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pet not found"
        )
    return pet.to_dict()


@router.put("/{pet_id}", response_model=PetResponse)
async def update_pet(
    pet_data: PetUpdate,
    pet_id: str = Path(..., description="The ID of the pet to update"),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Any:
    """
    Update a pet listing.
    
    Users can only update their own pet listings, except for admins who can update any pet listing.
    
    Args:
        pet_data: Updated pet data
        pet_id: ID of the pet to update
        current_user: Current authenticated user
        
    Returns:
        PetResponse: Updated pet details
        
    Raises:
        HTTPException: If update fails or user is not authorized
    """
    # Get the pet to check ownership
    pet = await PetService.get_pet_by_id(pet_id)
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pet not found"
        )
    
    # Check if user is owner or admin
    if pet.owner_id != current_user["user_id"] and current_user["role"] != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this pet listing"
        )
    
    # Update the pet
    updated_pet = await PetService.update_pet(pet_id, pet_data)
    if not updated_pet:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update pet listing"
        )
    
    return updated_pet.to_dict()


@router.delete("/{pet_id}", status_code=status.HTTP_200_OK)
async def delete_pet(
    pet_id: str = Path(..., description="The ID of the pet to delete"),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, str]:
    """
    Delete a pet listing.
    
    Users can only delete their own pet listings, except for admins who can delete any pet listing.
    
    Args:
        pet_id: ID of the pet to delete
        current_user: Current authenticated user
        
    Returns:
        Dict: Success message
        
    Raises:
        HTTPException: If deletion fails or user is not authorized
    """
    # Get the pet to check ownership
    pet = await PetService.get_pet_by_id(pet_id)
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pet not found"
        )
    
    # Check if user is owner or admin
    if pet.owner_id != current_user["user_id"] and current_user["role"] != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this pet listing"
        )
    
    # Delete the pet
    success = await PetService.delete_pet(pet_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete pet listing"
        )
    
    return {"message": "Pet listing deleted successfully"}