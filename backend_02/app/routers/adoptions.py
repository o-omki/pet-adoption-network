from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.auth import get_current_user
from app.services.adoption_service import AdoptionService
from app.schemas.adoption import (
    AdoptionApplicationCreate,
    AdoptionApplicationUpdate,
    AdoptionApplicationResponse
)

router = APIRouter()


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_adoption_application(
    application_data: AdoptionApplicationCreate,
    current_user: dict = Depends(get_current_user)
) -> Any:
    """
    Create a new adoption application.
    """
    # Check if user has adopter role
    user_role = current_user.get("role")
    if user_role != "adopter":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only users with role 'adopter' can submit adoption applications"
        )
    
    try:
        new_application = await AdoptionService.create_application(
            application_data, 
            current_user.get("user_id")
        )
        return {
            "message": "Adoption application submitted successfully",
            "application_id": new_application["application_id"]
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("", response_model=List[AdoptionApplicationResponse])
async def get_adoption_applications(
    current_user: dict = Depends(get_current_user)
) -> Any:
    """
    Get adoption applications for the authenticated user.
    
    For adopters, returns their submitted applications.
    For shelter/individual pet owners, returns applications for their pets.
    """
    user_id = current_user.get("user_id")
    user_role = current_user.get("role")
    
    if user_role == "adopter":
        # Get applications submitted by this adopter
        applications = await AdoptionService.get_applications_by_adopter(user_id)
    elif user_role in ["shelter", "individual"]:
        # Get applications for pets owned by this user
        applications = await AdoptionService.get_applications_for_pet_owner(user_id)
    else:
        # Admin can see all applications (not implemented here)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only adopters, shelters, and individual pet owners can access applications"
        )
    
    return applications


@router.get("/{application_id}", response_model=AdoptionApplicationResponse)
async def get_adoption_application(
    application_id: str,
    current_user: dict = Depends(get_current_user)
) -> Any:
    """
    Get a specific adoption application.
    """
    application = await AdoptionService.get_application_by_id(application_id)
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Adoption application not found"
        )
    
    user_id = current_user.get("user_id")
    user_role = current_user.get("role")
    
    # Check if user is authorized to view this application
    is_adopter = application["adopter_id"] == user_id
    is_pet_owner = await AdoptionService.is_pet_owner_for_application(application_id, user_id)
    is_admin = user_role == "admin"
    
    if not (is_adopter or is_pet_owner or is_admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this application"
        )
    
    return application


@router.put("/{application_id}", response_model=dict)
async def update_adoption_application(
    application_id: str,
    status_update: AdoptionApplicationUpdate,
    current_user: dict = Depends(get_current_user)
) -> Any:
    """
    Update the status of an adoption application.
    """
    # Get the application to verify it exists
    application = await AdoptionService.get_application_by_id(application_id)
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Adoption application not found"
        )
    
    # Check if user is authorized (must be pet owner or admin)
    is_pet_owner = await AdoptionService.is_pet_owner_for_application(application_id, current_user.get("user_id"))
    is_admin = current_user.get("role") == "admin"
    
    if not (is_pet_owner or is_admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this application"
        )
    
    try:
        updated_application = await AdoptionService.update_application_status(
            application_id, 
            status_update
        )
        return {
            "message": f"Adoption application status updated to {status_update.status}",
            "application_id": updated_application["application_id"]
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
