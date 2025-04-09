from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.core.auth import get_current_user
from app.services.pet_service import PetService
from app.schemas.pet import PetCreate, PetUpdate, PetResponse, PetFilter, PetStatus

router = APIRouter()


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_pet(
    pet_data: PetCreate,
    current_user: dict = Depends(get_current_user)
) -> Any:
    """
    Create a new pet listing.
    """
    # Check if user role matches the owner type
    user_role = current_user.get("role")
    if (pet_data.owner_type == "shelter" and user_role != "shelter") or \
       (pet_data.owner_type == "individual" and user_role != "individual"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Only users with role '{pet_data.owner_type}' can create listings with owner_type '{pet_data.owner_type}'"
        )
    
    try:
        new_pet = await PetService.create_pet(pet_data, current_user.get("user_id"))
        return {
            "message": "Pet listing created successfully",
            "pet_id": new_pet["pet_id"]
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("", response_model=List[PetResponse])
async def get_pets(
    pet_type_id: Optional[str] = None,
    breed_id: Optional[str] = None,
    status: Optional[PetStatus] = None,
    age_min: Optional[int] = None,
    age_max: Optional[int] = None,
    gender: Optional[str] = None,
    owner_id: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100)
) -> Any:
    """
    Get all pet listings with optional filters.
    """
    filters = PetFilter(
        pet_type_id=pet_type_id,
        breed_id=breed_id,
        status=status,
        age_min=age_min,
        age_max=age_max,
        gender=gender,
        owner_id=owner_id
    )
    
    pets = await PetService.get_pets(filters, skip, limit)
    return pets


@router.get("/{pet_id}", response_model=PetResponse)
async def get_pet(
    pet_id: str
) -> Any:
    """
    Get a specific pet by ID.
    """
    pet = await PetService.get_pet_by_id(pet_id)
    
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pet not found"
        )
    
    return pet


@router.put("/{pet_id}", response_model=dict)
async def update_pet(
    pet_id: str,
    pet_update: PetUpdate,
    current_user: dict = Depends(get_current_user)
) -> Any:
    """
    Update a pet listing.
    """
    # Verify the pet exists
    pet = await PetService.get_pet_by_id(pet_id)
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pet not found"
        )
    
    # Check if user is the owner or admin
    is_owner = await PetService.is_pet_owner(pet_id, current_user.get("user_id"))
    is_admin = current_user.get("role") == "admin"
    
    if not (is_owner or is_admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to update this pet listing"
        )
    
    try:
        updated_pet = await PetService.update_pet(pet_id, pet_update)
        return {
            "message": "Pet listing updated successfully",
            "pet_id": updated_pet["pet_id"]
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.delete("/{pet_id}", response_model=dict)
async def delete_pet(
    pet_id: str,
    current_user: dict = Depends(get_current_user)
) -> Any:
    """
    Delete a pet listing.
    """
    # Verify the pet exists
    pet = await PetService.get_pet_by_id(pet_id)
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pet not found"
        )
    
    # Check if user is the owner or admin
    is_owner = await PetService.is_pet_owner(pet_id, current_user.get("user_id"))
    is_admin = current_user.get("role") == "admin"
    
    if not (is_owner or is_admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to delete this pet listing"
        )
    
    success = await PetService.delete_pet(pet_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete pet listing"
        )
    
    return {"message": "Pet listing deleted successfully"}
